/* @(#)arf.hpp
 * @brief C++ arf interface
 *
 * Copyright (C) 2011-2013 C Daniel Meliza <dan||meliza.org>
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 */

#ifndef _ARF_HH
#define _ARF_HH 1

// don't include extra headers
#define BOOST_UUID_NO_TYPE_TRAITS
#include <boost/uuid/random_generator.hpp>
#include <boost/uuid/string_generator.hpp>
#include <boost/uuid/uuid_io.hpp>

#include "arf/types.hpp"
#include "arf/h5e.hpp"
#include "arf/h5f.hpp"
#include "arf/h5a.hpp"
#include "arf/h5t.hpp"
#include "arf/h5s.hpp"
#include "arf/h5d.hpp"
#include "arf/h5pt.hpp"

namespace arf {

/*
 * @namespace arf
 *
 * The classes in this namespace define a fairly simple C++ interface
 * for reading and writing ARF files. This consists of a thin wrapper
 * around a more generic HDF5 interface, which is in sub-namespaces of
 * arf. The arf interface simply takes care of setting required
 * attributes, and ensures that data are accessible through the Python
 * and other ARF interfaces.
 *
 * To some extent the HDF5 interface duplicates the existing C++
 * interface shipped with HDF5, but there are some issues compiling it
 * with other features, and quite frankly it's not the best C++
 * interface in the world. The resource model here is focused on
 * safety; objects own the underlying handle to the resources they
 * manage and call the appropriate cleanup function on destruction.
 * Consequently, many of the objects cannot be copied and do not have
 * public constructors.
 *
 */

/*
 * valgrind testing notes:
 *
 * hdf5 needs to be compiled with --enable-using-memchecker
 * boost::uuid causes a lot of uninitialized memory errors, but this is intentional
 *
 */

/**
 * @brief Represents an arf entry.
 *
 * A thin wrapper around h5g::group that creates necessary attributes
 * and provides more convenient dataset creation functions.
 */
class entry : public h5g::group {
public:
	typedef boost::shared_ptr<entry> ptr_type;

	/** Open an existing entry object */
	entry(h5a::node const & parent, std::string const & name)
		: h5g::group(parent, name) {
                if (has_attribute("uuid")) {
                        std::string s;
                        read_attribute("uuid",s);
                        _uuid = boost::uuids::string_generator()(s);
                }
        }

	/** Create a new entry object */
	template <typename Type>
	entry(h5a::node const & parent, std::string const & name,
	      std::vector<Type> const & timestamp)
		: h5g::group(parent, name, true),
                  _uuid(boost::uuids::random_generator()()) {
		write_attribute<boost::int64_t, Type>("timestamp", timestamp);
		write_attribute("uuid", boost::uuids::to_string(_uuid));
	}

	entry(h5a::node const & parent, std::string const & name,
              boost::int64_t tv_sec, boost::int64_t tv_usec=0)
		: h5g::group(parent, name, true),
                  _uuid(boost::uuids::random_generator()()) {
                boost::int64_t ts[2] = { tv_sec, tv_usec };
		write_attribute("timestamp", ts, 2);
		write_attribute("uuid", boost::uuids::to_string(_uuid));
	}

	/**
	 * Create a new dataset and add data to it.  Currently only 1D
	 * data is supported.
	 *
	 * @param name  the name of the dataset
	 * @param data  the data to store in the dataset
	 * @param units the units of the data
	 * @param datatype an integer code indicating the type of data
	 * @param replace if true, drop existing dataset; otherwise appends data
	 * @param compression integer code indicating compression ratio
	 */
	template <typename StorageType, typename MemType>
	h5d::dataset::ptr_type
	create_dataset(std::string const & name,
		       std::vector<MemType> const & data,
		       std::string const & units,
		       DataType datatype=UNDEFINED,
		       bool replace=false,
		       int compression=0) {
		if (contains(name) && replace)
			unlink(name);

		h5d::dataset::ptr_type ds = h5g::group::create_dataset(name, data, compression);
		ds->write_attribute("datatype",static_cast<int>(datatype));
		ds->write_attribute("units",units);
		return ds;
	}

	template <typename Type>
	h5d::dataset::ptr_type
	create_dataset(std::string const & name,
		       std::vector<Type> const & data,
		       std::string const & units,
		       DataType datatype,
		       bool replace=false,
		       int compression=0) {
		return create_dataset<Type,Type>(name,data,units,datatype,replace,compression);
	}

	/**
	 * Create a new packet table dataset. Packet table datasets
	 * are useful for writing a stream of data. No type conversion
	 * is supported, but the interface is extremely simple.
	 *
	 * @param name  the name of the dataset
	 * @param units the units of the data
	 * @param datatype an integer code indicating the type of data
	 * @param replace if true, drop existing dataset; otherwise appends data
	 * @param compression integer code indicating compression ratio
	 */
	template <typename StorageType>
	typename h5pt::packet_table::ptr_type
	create_packet_table(std::string const & name,
			    std::string const & units,
			    DataType datatype,
			    bool replace=false,
			    hsize_t chunk_size=1024,
			    int compression=0) {
                h5pt::packet_table::ptr_type pt =
                        h5g::group::create_packet_table<StorageType>(name, replace, chunk_size, compression);
		pt->write_attribute("datatype",static_cast<int>(datatype));
		pt->write_attribute("units",units);
		return pt;
	}

        boost::uuids::uuid const & uuid() const { return _uuid; }

private:
        boost::uuids::uuid _uuid;
};

/**
 * @brief Represents an arf file.
 *
 * A thin wrapper around h5f::file that creates necessary attributes
 * and provides a more convenient entry accessor
 */
class file : public h5f::file {

public:
	typedef boost::shared_ptr<file> ptr_type;

	/**
	 * Open or create an ARF file.  File access mode can be one
	 * of the following values:
	 * 'r' : read-only; file must exist
	 * 'a' : read-write access, creating file if necessary
	 * 'w' : read-write access; truncates file if it exists
	 *
	 * @param name  the path of the file to open/create
	 * @param mode  the mode to open the file
	 */
	file(std::string const & name, std::string const & mode)
		: h5f::file(name, mode) {
		// set root-level attributes
                // TODO check whether file exists and already has version information
		if (mode=="w" || mode=="a") {
                        write_attribute("arf_library_version", ARF_LIBRARY_VERSION);
                        write_attribute("arf_library", "c++");
			write_attribute("arf_version", ARF_VERSION);
		}
	}

};

}


#endif /* _ARF_H */
