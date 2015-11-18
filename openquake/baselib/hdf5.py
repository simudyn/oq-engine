#  -*- coding: utf-8 -*-
#  vim: tabstop=4 shiftwidth=4 softtabstop=4

#  Copyright (c) 2015, GEM Foundation

#  OpenQuake is free software: you can redistribute it and/or modify it
#  under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  OpenQuake is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU Affero General Public License
#  along with OpenQuake.  If not, see <http://www.gnu.org/licenses/>.


class Hdf5Dataset(object):
    """
    Little wrapper around a one-dimensional HDF5 dataset.

    :param hdf5: a h5py.File object
    :param name: an hdf5 key string
    :param dtype: dtype of the dataset (usually composite)
    :param shape: shape of the dataset (if None, the dataset is extendable)
    :param compression: None or 'gzip' are recommended
    """
    @classmethod
    def create(cls, hdf5, name, dtype, shape=None, compression=None):
        if shape is None:  # extendable dataset
            dset = hdf5.create_dataset(
                name, (0,), dtype, chunks=True, maxshape=(None,))
            dset.attrs['nbytes'] = 0
        else:  # fixed-shape dataset
            dset = hdf5.create_dataset(name, shape, dtype)
        return cls(dset)

    def __init__(self, dset):
        self.dset = dset
        self.file = dset.file
        self.name = dset.name
        self.dtype = dset.dtype
        self.attrs = dset.attrs
        self.size = len(dset)

    def extend(self, array):
        """
        Extend the dataset with the given array, which must have
        the expected dtype. This method will give an error if used
        with a fixed-shape dataset.
        """
        newsize = self.size + len(array)
        self.dset.resize((newsize,))
        self.dset[self.size:newsize] = array
        self.size = newsize
        self.dset.attrs['nbytes'] += array.nbytes
