# -*- coding: utf-8 -*-
"""
    @ description：

    @ date:
    @ author: achange
"""

import os
import _czifile as czifile
import numpy as np
from PIL import Image


class CziFile(object):
    """Zeiss CZI file object.

      Args:
        |  czi_filename (str): Filename of czifile to access.

      Kwargs:
        |  metafile_out (str): Filename of xml file to optionally export czi meta data to.
        |  use_pylibczi (bool): Set to false to use Christoph Gohlke's czifile reader instead of libCZI.
        |  verbose (bool): Print information and times during czi file access.

    .. note::

       Utilizes compiled wrapper to libCZI for accessing the CZI file.

    """
    def __init__(self, czi_file):
        self.czi_file = czi_file
        self.subblock_number = czifile.cnt_subblocks(czi_file)

        # todo: 设置subblock保存为图像时的  文件名规范
        self.fname_pattern = "subblock_{:0>" + str(len(str(self.subblock_number))) + "}.jpg"

        # whether to use czifile or pylibczi for reading the czi file.
        # Other library to read czifile : https://www.lfd.uci.edu/~gohlke/code/czifile.py.html

    def get_subblock_data(self, idx: int):
        """
            获取指定idx的subblock data: np.ndarray
        """
        if idx < 0:
            raise ValueError("index must be ≥ 0!")
        if idx > self.subblock_number - 1:
            raise ValueError("index out of range")

        *info, data = czifile.cziread_subblock(self.czi_file, idx)
        return info, data

    @staticmethod
    def save_subblock_data_to_jpg(info, data, file):
        """
            subblock数据保存为图像
        """
        height, width = info[1]
        data = data.reshape(height, width, 3)

        img_data = np.empty(shape=(height, width, 3), dtype=np.uint8)
        img_data[:, :, 0] = data[:, :, 2].reshape(height, width)
        img_data[:, :, 1] = data[:, :, 1].reshape(height, width)
        img_data[:, :, 2] = data[:, :, 0].reshape(height, width)

        Image.fromarray(img_data).save(file)

    def save_all_subblocks(self, save_dir, zoom=1.):
        for i in range(self.subblock_number):
            fname = self.fname_pattern.format(i+1)
            file = os.path.join(save_dir, fname)

            *info, t_zoom, data = czifile.cziread_subblock(self.czi_file, i)
            if t_zoom == zoom:
                self.save_subblock_data_to_jpg(info, data, file)

    def get_total_img(self):
        """将czi文件按照1:1展示为图像  返回图像的np.ndarray数据
        """
        pass

    # https://stackoverflow.com/questions/43554819/find-most-frequent-row-or-mode-of-a-matrix-of-vectors-python-numpy
    @staticmethod
    def _mode_rows(a):
        a = np.ascontiguousarray(a)
        void_dt = np.dtype((np.void, a.dtype.itemsize * np.prod(a.shape[1:])))
        _, ids, count = np.unique(a.view(void_dt).ravel(), return_index=1, return_counts=1)
        largest_count_id = ids[count.argmax()]
        most_frequent_row = a[largest_count_id]
        return most_frequent_row

    @staticmethod
    def _montage(images, coords, bg=0, mode_size_only=False):
        # TODO
        pass


if __name__ == '__main__':
    pass
