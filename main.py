#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'

# from phone_img_parser import PhoneImgParser
# from glob import glob
#
#
# def num_im(file):
#     file = file.replace('examples\\', '')
#     file = file.replace('.png', '')
#     return int(file)
#
#
# if __name__ == '__main__':
#     parser = PhoneImgParser()
#
#     # glob сортирует файлы как строки, а мне хотелось бы, чтобы сортировалось
#     # по номеру в файле
#     files = sorted(glob('examples/*.png'), key=num_im)
#
#     for file in files:
#         phone = parser.parse_from_file(file)
#         print('"{}" -- {}'.format(phone, file))

from PIL import Image


num = 2


im = Image.open('examples/{}.png'.format(num))
# print(im)
# print(im.histogram())
print({i: c for i, c in enumerate(im.histogram()) if c != 0})

im = im.convert('L')
w, h = im.size

BLACK_PXL = 0
WHITE_PXL = 255

for x in range(w):
    for y in range(h):
        pxl = im.getpixel((x, y))
        if pxl != BLACK_PXL and pxl != WHITE_PXL:
            im.putpixel((x, y), 255)

im.save('_{}.png'.format(num))
print()
# print(im.histogram())
print({i: c for i, c in enumerate(im.histogram()) if c != 0})


# for i in range(1, 6):
#     im = Image.open('examples/{}.png'.format(i)).convert('L')
#     # print(im)
#     # print(im.histogram())
#     print(Counter(im.histogram()))


