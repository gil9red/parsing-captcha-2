#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'

from phone_img_parser import PhoneImgParser
from glob import glob


def num_im(file):
    file = file.replace('examples\\', '')
    file = file.replace('.png', '')
    return int(file)


if __name__ == '__main__':
    parser = PhoneImgParser()

    # glob сортирует файлы как строки, а мне хотелось бы, чтобы сортировалось
    # по номеру в файле
    files = sorted(glob('examples/*.png'), key=num_im)

    for file in files:
        phone = parser.parse_from_file(file)
        print('"{}" -- {}'.format(phone, file))
