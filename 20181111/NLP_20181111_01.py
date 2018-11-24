import pandas as pd
import re
import requests
from collections import Counter
from matplotlib.pyplot import yscale, xscale, title, plot
from matplotlib import pyplot as plt

filename = '80k_articles.txt'
all_content = open(filename, encoding="utf8").read()
print(len(all_content))
print(all_content[:200])

def tokenize(string):
    return ''.join(re.findall('[\w|\d]+', string))

ALL_CHARACTER=tokenize(all_content)
print(ALL_CHARACTER[:200])

# text = requests.get('https://movie.douban.com/').text
# print(text)

L = [1, 1, 2, 3, 4, 4, 4]
print(Counter(L))
all_character_counts = Counter(ALL_CHARACTER)
# print(all_character_counts.most_common()[:20])

M = all_character_counts.most_common()[0][1]
yscale('log'); xscale('log'); title('Frequency of n-th most frequent word and 1/n line.')
plot([c for (w, c) in all_character_counts.most_common()])
plot([M/i for i in range(1, len(all_character_counts)+1)])
# plt.show()

print(all_character_counts.get('的', 1))

def get_probability_from_counts(count):
    all_occurences = sum(count.values())
    def get_prob(item):
        return count[item] / all_occurences
    return get_prob

get_char_prob = get_probability_from_counts(all_character_counts)

def get_char_probability(char):
    all_occurences = sum(all_character_counts.values())
    return all_character_counts[char] / all_occurences

import time

def get_running_time(func, arg, times):
    start_time = time.time()
    for _ in range(times):
        func(arg)
    print('\t\t {} used time is {}'.format(func.__name__, time.time() - start_time))

print(get_running_time(get_char_probability, '神', 10000))
print(get_running_time(get_char_prob, '神', 10000))

from functools import reduce
from operator import mul, add

def prob_of_string(string):
    return reduce(mul, [get_char_prob(c) for c in string])

pair = """前天晚上吃晚饭的时候
前天晚上吃早饭的时候""".split('\n')

pair2 = """正是一个好看的小猫
真是一个好看的小猫""".split('\n')

pair3 = """我无言以对，简直
我简直无言以对""".split('\n')

pairs = [pair, pair2, pair3]

def get_probability_prefromance(language_model_func, pairs):
    for (p1, p2) in pairs:
        print('*'*18)
        print('\t\t {} with probability {}'.format(p1, language_model_func(tokenize(p1))))
        print('\t\t {} with probability {}'.format(p2, language_model_func(tokenize(p2))))

get_probability_prefromance(prob_of_string, pairs)


# 二元 2-Gram
gram_length = 2
# 把原本tokenize成单个字的列表构造成两个字的列表
two_gram_counts = Counter(ALL_CHARACTER[i:i+gram_length] for i in range(len(ALL_CHARACTER) - gram_length))

get_pair_prob = get_probability_from_counts(two_gram_counts)
