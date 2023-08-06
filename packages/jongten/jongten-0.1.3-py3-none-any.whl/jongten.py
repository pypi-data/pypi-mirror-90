from util import get_random_kaze_set, get_is_or_not
from questions import questions
import random
from mahjong.hand_calculating.hand import HandCalculator
from mahjong.tile import TilesConverter
from mahjong.hand_calculating.hand_config import HandConfig
from mahjong.constants import EAST
from util import DISPLAY_WINDS_JP
calculator = HandCalculator()


def main():
    hand = random.choice(questions)
    round_wind, player_wind = get_random_kaze_set()
    tiles = TilesConverter.string_to_136_array(
        man=hand.get_man(), pin=hand.get_pin(), sou=hand.get_sou())
    win_tile = TilesConverter.string_to_136_array(
        **hand.get_win_tile())[0]
    conf = {
        'is_tsumo': get_is_or_not(),
        'is_riichi': get_is_or_not(),
        'player_wind': player_wind,
        'round_wind': round_wind
    }
    config = HandConfig(**conf)
    result = calculator.estimate_hand_value(tiles, win_tile, config=config)

    question_caption = '\n'
    if config.is_tsumo:
        question_caption += f"ツモ:{hand.get_win_tile_figure()} "
    else:
        question_caption += f"ロン:{hand.get_win_tile_figure()} "

    if config.is_riichi:
        question_caption += 'リーチ有 '
    else:
        question_caption += 'リーチ無 '
    question_caption += f"場風: {DISPLAY_WINDS_JP[config.round_wind]} 自風: {DISPLAY_WINDS_JP[config.player_wind]}"

    print(hand.get_figure())
    print(question_caption)
    if config.is_tsumo and config.player_wind == EAST:
        child_answer = int(input('子の支払う点数: '))
        if child_answer == result.cost['main']:
            print('正解!!')
        else:
            print(f"不正解!! 正解は {result.cost['main']} オール")
    elif config.is_tsumo and config.player_wind != EAST:
        parent_answer = int(input('親の支払う点数: '))
        child_answer = int(input('子の支払う点数: '))
        if parent_answer == result.cost['main'] and child_answer == result.cost['additional']:
            print('正解!!')
        else:
            print(
                f"不正解!! 正解は 親: {result.cost['main']}, 子: {result.cost['additional']}")
    else:
        answer = int(input('放銃者の支払う点数: '))
        if answer == result.cost['main']:
            print('正解!!')
        else:
            print(f"不正解!! 正解は {result.cost['main']}")


if __name__ == "__main__":
    main()
