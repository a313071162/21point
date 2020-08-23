# -*- encoding: utf-8 -*-


"""
@File    : games.py
@Time    : 2020/8/23 上午9:28
@Author  : dididididi
@Email   : 
@Software: PyCharm
"""

import random
import numpy as np

# 创建排堆
poker_name = ['♦10', '♦2', '♦3', '♦4', '♦5', '♦6', '♦7', '♦8', '♦9', '♦A', '♦J', '♦K', '♦Q',
              '♣10', '♣2', '♣3', '♣4', '♣5', '♣6', '♣7', '♣8', '♣9', '♣A', '♣J', '♣K', '♣Q',
              '♥10', '♥2', '♥3', '♥4', '♥5', '♥6', '♥7', '♥8', '♥9', '♥A', '♥J', '♥K', '♥Q',
              '♠10', '♠2', '♠3', '♠4', '♠5', '♠6', '♠7', '♠8', '♠9', '♠A', '♠J', '♠K', '♠Q']

# 设置分值
poker_value = {'♣A': 1, '♥A': 1, '♠A': 1, '♦A': 1,
               '♦10': 10, '♦2': 2, '♦3': 3, '♦4': 4, '♦5': 5, '♦6': 6, '♦7': 7, '♦8': 8, '♦9': 9, '♦J': 10, '♦K': 10,
               '♦Q': 10,
               '♣10': 10, '♣2': 2, '♣3': 3, '♣4': 4, '♣5': 5, '♣6': 6, '♣7': 7, '♣8': 8, '♣9': 9, '♣J': 10, '♣K': 10,
               '♣Q': 10,
               '♥10': 10, '♥2': 2, '♥3': 3, '♥4': 4, '♥5': 5, '♥6': 6, '♥7': 7, '♥8': 8, '♥9': 9, '♥J': 10, '♥K': 10,
               '♥Q': 10,
               '♠10': 10, '♠2': 2, '♠3': 3, '♠4': 4, '♠5': 5, '♠6': 6, '♠7': 7, '♠8': 8, '♠9': 9, '♠J': 10, '♠K': 10,
               '♠Q': 10}

# A的可能
Ace = {'♣A', '♥A', '♠A', '♦A'}


def dealing_poker(poker_database):
    """
    发牌，并删除排堆中的牌
    :param poker_database: 牌堆
    :return:
    """
    return poker_database.pop(random.randint(0, len(poker_database) - 1))


def count_score(hand_poker):
    """
    计算分数
    :param hand_poker: 手牌
    :return:
    """
    score = 0
    hava_ace = False
    for k in hand_poker:
        score = score + poker_value[k]
    # 由于A的特殊性，可以为1或者11，所以此处需要进行判断
    for i in hand_poker:
        if i in Ace:
            hava_ace = True
            break
        else:
            continue
    if hava_ace:
        if score + 10 <= 21:
            score = score + 10
    return score


def judgement(your_score, pc_score):
    """
    判断输赢
    :param your_score:
    :param pc_score:
    :return:
    """
    if your_score > 21 and pc_score > 21:
        print('DRAW')
        return np.array([0, 0])
    elif your_score > 21 and pc_score <= 21:
        print('YOU LOSE')
        return np.array([0, 1])
    elif your_score <= 21 and pc_score > 21:
        print('YOU WIN')
        return np.array([1, 0])
    elif your_score <= 21 and pc_score <= 21:
        if your_score < pc_score:
            print('YOU LOSE')
            return np.array([0, 1])
        elif your_score > pc_score:
            print('YOU WIN')
            return np.array([1, 0])
        else:
            print('DRAW')
            return np.array([0, 0])


def hit_or_stand(poker_database):
    """
    判断是否继续要牌
    :return:
    """
    AskPoker = input('Would You Hit?(Y/N)>>:')
    if AskPoker.upper() == 'Y':
        return dealing_poker(poker_database)
    elif AskPoker.upper() == 'N':
        print("You stand")
        return False
    else:
        print('Wrong input, please input Y/y or N/n!>>')
        return hit_or_stand(poker_database)


def start_dealing(poker_database):
    """
    开局发两张牌
    :param poker_database:
    :return:
    """
    return [poker_database.pop(random.randint(0, len(poker_database) - 1)),
            poker_database.pop(random.randint(0, len(poker_database) - 1))]


def round():
    # 一共是使用几副牌
    poker_deck = 1
    # 最终生成的牌堆
    poker_database = poker_name * poker_deck
    # 总分的计分器
    total_score = np.array([0, 0])
    your_hand_poker = []
    pc_hand_poker = []

    you_get = start_dealing(poker_database)
    pc_get = start_dealing(poker_database)

    print(f'Your hand poker: {you_get[0]}, {you_get[1]}')
    print(f'PC hand poker: {pc_get[0]}, ?\n')

    # 将玩家和庄家的手牌放入数组中
    your_hand_poker.extend(you_get)
    pc_hand_poker.extend(pc_get)
    score = np.array([count_score(your_hand_poker), count_score(pc_hand_poker)])
    if score[0] == 21 or score[1] == 21:
        print('BlackJack')
        return judgement(score[0], score[1])
    else:
        while score[0] <= 21:
            new_poker = hit_or_stand(poker_database)
            if new_poker != False:
                your_hand_poker.append(new_poker)
                print(f'You Hand Poker:{your_hand_poker}')
                score[0] = count_score(your_hand_poker)
                if score[0] > 21:
                    print('You Bust')
                    print(f'PC\'s Hand Poker:{pc_hand_poker}')
                    return judgement(score[0], score[1])
                else:
                    continue
            elif new_poker == False:
                while score[1] < 17:
                    pc_hand_poker.append(dealing_poker(poker_database))
                    score[1] = count_score(pc_hand_poker)
                print(f'PC final hand poker:{pc_hand_poker}')
                return judgement(score[0], score[1])
                break
            else:
                continue
