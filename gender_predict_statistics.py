# -*- coding:utf-8 -*-

import math
import pandas as pd

from collections import defaultdict
from sklearn.metrics import accuracy_score

# 读取数据
def load_data():
    data = pd.read_csv('data/data_set.txt', encoding='utf-8')
    data = data.dropna()

    data.loc[data['gender'] == 2, 'gender'] = 0

    # 划分训练集和测试集
    train = data.sample(frac=0.95, random_state=None, axis=0)
    test = data[~data.index.isin(train.index)]

    names_female = train[train['gender'] == 0]
    names_male = train[train['gender'] == 1]

    totals = {
        'f': len(names_female),
        'm': len(names_male)
    }

    return names_female, names_male, totals,train,test

# 计算频率
def cal_frequency(names_female, names_male, totals):
    # 计算在所有女生的名字当中，某个字出现的频率，相当于是计算 P(Xi|女生)
    frequency_list_f = defaultdict(int)
    for name in names_female['name']:
        for char in name:
            frequency_list_f[char] += 1. / totals['f']

    # 计算在所有男生的名字当中，某个字出现的频率，相当于是计算P(Xi|男生)
    frequency_list_m = defaultdict(int)
    for name in names_male['name']:
        for char in name:
            frequency_list_m[char] += 1. / totals['m']

    return frequency_list_f, frequency_list_m

# Laplace平滑
def laplace_smooth(char, frequency_list, total, alpha=1.0):
    count = frequency_list[char] * total
    distinct_chars = len(frequency_list)
    freq_smooth = (count + alpha) / (total + distinct_chars * alpha)
    return freq_smooth

def get_base(frequency_list_f,frequency_list_m,train):
    base_f = math.log(1 - train['gender'].mean())
    base_f += sum([math.log(1 - frequency_list_f[char]) for char in frequency_list_f])

    base_m = math.log(train['gender'].mean())
    base_m += sum([math.log(1 - frequency_list_m[char]) for char in frequency_list_m])

    bases = {'f': base_f, 'm': base_m}
    return bases

def get_log_prob(char, frequency_list, total):
    freq_smooth = laplace_smooth(char, frequency_list, total)
    return math.log(freq_smooth) - math.log(1 - freq_smooth)

def compute_log_prob(name, bases, totals, frequency_list_m, frequency_list_f):
    logprob_m = bases['m']
    logprob_f = bases['f']
    for char in name:
        logprob_m += get_log_prob(char, frequency_list_m, totals['m'])
        logprob_f += get_log_prob(char, frequency_list_f, totals['f'])
    return {'male': logprob_m, 'female': logprob_f}

def get_gender(log_probs):
    return log_probs['male'] > log_probs['female']

def get_result(bases, totals, frequency_list_m, frequency_list_f,test):
    result = []
    for name in test['name']:
        log_probs = compute_log_prob(name, bases, totals, frequency_list_m, frequency_list_f)
        gender = get_gender(log_probs)
        result.append(int(gender))
    test['predict'] = result
    print(test.tail(20))
    print(f"Accuracy: {accuracy_score(test['gender'],test['predict'])*1.}")
    return test

def main():
    names_female,names_male,totals,train,test = load_data()
    frequency_list_f, frequency_list_m = cal_frequency(names_female,names_male,totals)
    bases = get_base(frequency_list_f,frequency_list_m,train)
    result = get_result(bases, totals, frequency_list_m, frequency_list_f,test)
    result.to_csv('data/result.csv',index=False)

if __name__ == "__main__":
    main()