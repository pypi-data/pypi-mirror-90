import random
from mahjong.constants import EAST, SOUTH, WEST, NORTH, WINDS


def get_random_kaze_set():
    return EAST, random.choice(WINDS)


def get_is_or_not():
    return random.choice([True, False])


DISPLAY_WINDS_JP = {EAST: '東', SOUTH: '南', WEST: '西', NORTH: '北'}
