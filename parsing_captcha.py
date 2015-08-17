#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'ipetrash'


"""Скрипт разбирает капчи. Пример капч в папке test_captcha.

Алгоритм разбора не умеет разбирать буквы, которые по вертикали не имеет просветов.
Решением может быть улучшение алгоритма поиска просветов в функции border_letters или
добавлением масок "слипшихся" букв.
"""


from PIL import Image
import hashlib


BLACK_PXL = 0
WHITE_PXL = 255


def clear_captcha(im):
    """Функция очищает капчу от ненужного, оставляя только текст"""
    # Т.к. исходные капчи имеет всегда одинаковый цвет текста -- черный,
    # то очищение капчи будет таким простым

    w, h = im.size

    for x in range(w):
        for y in range(h):
            pxl = im.getpixel((x, y))

            # Все пиксели, отличающиеся от черного, закрашивают белым
            if pxl != BLACK_PXL:
                im.putpixel((x, y), WHITE_PXL)


def get_margins(im):
    """Функция для определения границ слова капчи"""

    w, h = im.size
    left, right, top, bottom = w, -1, h, -1

    for y in range(h):
        for x in range(w):
            pxl = im.getpixel((x, y))

            if pxl == BLACK_PXL:
                if left > x:
                    left = x

                if right < x:
                    right = x

                if top > y:
                    top = y

                if bottom < y:
                    bottom = y

    return left, right, top, bottom


def crop_captcha_text(im):
    """Функция вырезает из изображения текст капчи и возвращает его копию"""

    left, right, top, bottom = get_margins(im)
    return im.crop((left, top, right+1, bottom+1))


def border_letters(im):
    """Функция ищет просветы между буквами и возвращает координаты границ.
    Между двумя буквами вернется один и первый попавшийся просвет"""

    # Разделить на части
    w, h = im.size

    # Бывает, просвет между буквами больше одного пикселя
    # и чтобы у нас не набрались несколько координат просветов
    # между двумя буквами, а нам нужно только одну координату,
    # мы заводим флаг, который при нахождении просвета будет
    # возведен, а при встрече первого черного пикселя (дошли
    # до буквы) опущен
    multi_line = False

    lines = []

    # Ищем просветы между буквами
    for x in range(w):
        line = True

        for y in range(h):
            pxl = im.getpixel((x, y))

            # Если наткнулись на черный пиксель, значит
            # тут не просвета, выходим из цикла
            if pxl == BLACK_PXL:
                line = False
                multi_line = False
                break

        if line and not multi_line:
            multi_line = True
            lines.append(x)

    return lines


def get_letters_from_captcha(im):
    """Функция находит просветы между буквами капчи и вырезает буквы,
    предварительно обрезав вокруг каждой буквы фон, после функция
    вернет список изображений букв"""

    lines = border_letters(im)

    w, h = im.size

    # left -- просвет слева, для первой буквы будет равен 0
    left = 0
    top = 0
    bottom = h

    # Границей последней буквы будет ширина капчи
    lines.append(w)

    # Список для хранения букв капчи
    letters = []

    for line in lines:
        # right - просвет справа
        right = line

        # Вырезаем букву
        letter_im = im.crop((left, top, right, bottom))

        # Убираем белый фон вокруг буквы
        letter_im = crop_captcha_text(letter_im)

        letters.append(letter_im)

        # Для следующей буквы сдвигаем просвет слева
        # до просвета справа текущей буквы
        left = right

    return letters


def get_hash_mask_letter(letter_im):
    """Функция возвращает хеш маски изображения буквы."""

    str_bitarr = []
    w, h = letter_im.size

    for y in range(h):
        for x in range(w):
            pxl = letter_im.getpixel((x, y))

            # Если пиксель черный добавим в список '1', иначе '0'
            str_bitarr.append('1' if pxl == BLACK_PXL else '0')

    # Получим маску
    mask = ''.join(str_bitarr)

    # Подсчитаем хеш маски и будем по хешу определять буквы капчи
    hash = hashlib.new('md5')
    hash.update(mask.encode())
    hash_mask = hash.hexdigest()

    return hash_mask


import os
import string


class CaptchaParser:
    """Класс для парсинга капчи"""

    def __init__(self):
        self.letter_mask = {}
        self.mask_letter = {}

        for file in os.listdir('letters'):
            try:
                if '.png' in file:
                    name = file.replace('.png', '')
                    letter, mask = name.split('_')
                    self.letter_mask[letter] = mask
                    self.mask_letter[mask] = letter

            except ValueError as e:
                print('Обнаружен файл, имеющий нестандартное имя: {}, ошибка: {}'.format(file, e))

        all_letters = string.ascii_letters + string.digits
        for letter in self.letter_mask.keys():
            all_letters = all_letters.replace(letter, '')

        print('Не хватает {} букв: {}\n'.format(len(all_letters), list(all_letters)))

    def run(self, file):
        """Функция принимает путь к файлу капчи, парсит ее и возвращает распарсенную строку с текстом капчи."""

        im = Image.open(file).convert('L')

        # Очищение капчи
        clear_captcha(im)

        # Обрезание текста капчи
        im = crop_captcha_text(im)

        # Список букв капчи
        letters_captcha = get_letters_from_captcha(im)

        captcha_text = ''

        for im_letter in letters_captcha:
            # Получаем маску буквы капчи
            mask = get_hash_mask_letter(im_letter)
            letter = self.mask_letter.get(mask)

            if letter is None:
                full_file = 'letters/' + mask + '.png'
                print('Найдена новая буква mask={}, file={}. Сохраняю ее в {}. '
                      'Не забудь ее опознать!'.format(mask, file, full_file))
                im_letter.save(full_file)

                captcha_text += '-'
            else:
                captcha_text += letter

        return captcha_text
