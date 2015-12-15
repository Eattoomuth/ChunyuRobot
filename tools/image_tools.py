# -*- coding: utf-8 -*-

import Image
import ImageDraw
from tools import utils

__author__ = 'wgx'

LINE_WIDTH = 5
FILL_COLOR = '#FF0000'

test_source_path = '../assets/pngs/test.png'
test_output_path = '../assets/pngs/test_output.png'

DEFAULT_LENGTH = 200


def draw_line(draw, line_p):
    draw.line(line_p, fill=FILL_COLOR, width=LINE_WIDTH)


def draw_rec(image_path, out_put_path, point, x_len=DEFAULT_LENGTH, y_len=DEFAULT_LENGTH):
    """
    画一个以point为中心，边长为x和y的长方形
    :param image_path:  源图片路径
    :param point:   中心点，格式（x,y）
    :param x_len:   x边长
    :param y_len:   y边长
    """
    im = Image.open(image_path)
    draw = ImageDraw.Draw(im)

    half_x = x_len / 2
    half_y = y_len / 2

    # 处理边界超出图片范围的情况
    left_x = point[0] - half_x
    left_x = left_x > 0 and left_x or 0
    right_x = point[0] + half_x
    right_x = right_x < im.size[0] and right_x or im.size[0]
    top_y = point[1] - half_y
    top_y = top_y > 0 and top_y or 0
    bot_y = point[1] + half_y
    bot_y = bot_y < im.size[1] and bot_y or im.size[1]

    left_top_corner = (left_x, top_y)
    left_bot_corner = (left_x, bot_y)
    right_top_corner = (right_x, top_y)
    right_bot_corner = (right_x, bot_y)

    draw_line(draw, (left_top_corner, left_bot_corner))
    draw_line(draw, (left_top_corner, right_top_corner))
    draw_line(draw, (left_bot_corner, right_bot_corner))
    draw_line(draw, (right_top_corner, right_bot_corner))

    del draw

    im.save(out_put_path)


def draw_arrow(image_path, out_put_path, start, direct, length=DEFAULT_LENGTH):
    """
    画一个箭头，从start开始，略丑
    :param start:   起始位置
    :param direct:  方向
    :param length:  箭头长度
    """
    im = Image.open(image_path)
    draw = ImageDraw.Draw(im)

    x = start[0]
    y = start[1]

    ab_length = length / 5

    if direct == utils.DIRECTION_UP:
        # 处理边界
        y -= length
        y = (y >= 0 and y or 0)
        # 处理斜线
        x_a = x - ab_length
        y_a = y + ab_length
        x_b = x + ab_length
        y_b = y_a
    elif direct == utils.DIRECTION_DOWN:
        y += length
        y = (y <= im.size[1] and y or im.size[1])
        x_a = x - ab_length
        y_a = y - ab_length
        x_b = x + ab_length
        y_b = y_a
    elif direct == utils.DIRECTION_LEFT:
        x -= length
        x = (x >= 0 and x or 0)
        x_a = x + ab_length
        y_a = y - ab_length
        x_b = x_a
        y_b = y + ab_length
    else:
        x += length
        x = (x <= im.size[0] and x or im.size[0])
        x_a = x - ab_length
        y_a = y - ab_length
        x_b = x_a
        y_b = y + ab_length

    # 主干
    draw_line(draw, (start, (x, y)))
    # 两根斜线，取主干的五分之一，45度
    draw_line(draw, (x, y, x_a, y_a))
    draw_line(draw, (x, y, x_b, y_b))

    del draw

    im.save(out_put_path)


if __name__ == '__main__':
    # draw_rec(test_source_path, test_output_path, (1000, 1000), DIRECTION_UP)
    test_image = Image.open(test_source_path)
    draw = ImageDraw.Draw(test_image)








