#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'

from parsing_captcha import CaptchaParser
from glob import glob


def num_im(file):
    file = file.replace('examples\\', '')
    file = file.replace('.png', '')
    return int(file)


if __name__ == '__main__':
    parser = CaptchaParser()

    # glob сортирует файлы как строки, а мне хотелось бы, чтобы сортировалось
    # по номеру в файле
    files = sorted(glob('examples/*.png'), key=num_im)

    for file_name in files:
        phone = parser.run(file_name)
        print('"{}" -- {}'.format(phone, file_name))
