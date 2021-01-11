# -*- coding:utf-8 -*-

def gender_detect(term, content_lines):
    '''
    brief: 基于概率的性别检测算法，
    params: term 小说术语，保证是一个人名
    params: content_lines 按行分割好的小说文本
    retrun: genre (male, famale, neutral)
    '''
    lines = content_lines
    sls = []
    keyword = term
    hecount = 0
    shecount = 0
    itcount = 0
    sums = 0
    sumcount = 0
    andhecount = 0
    andshecount = 0
    anditcount = 0
    sums = len(lines)
    for line in lines:
        if line.find("他") != -1:
            hecount = hecount + 1
        if line.find("她") != -1:
            shecount = shecount + 1
        if line.find("它") != -1:
            itcount = itcount + 1
        if line.find(keyword) != -1:
            sls.append(line)
            sumcount = sumcount + 1
            if line.find("他") != -1:
                andhecount = andhecount + 1
            if line.find("她") != -1:
                andshecount = andshecount + 1
            if line.find("它") != -1:
                anditcount = anditcount + 1
    if sumcount == 0 or sums == 0:
        return 'neutral'
    heandr = (andhecount/sumcount)/(hecount/sums)
    sheandr = (andshecount/sumcount)/(shecount/sums)
    itandr = (anditcount/sumcount)/(itcount/sums)
    # print("他\t她\t它\n")
    candis = ['male', 'female', 'neutral']
    arr = [heandr, sheandr, itandr]
    # print(arr)
    return candis[arr.index(max(arr))]


def read_novel_lines(filename):
    with open(filename, encoding='utf-8') as f:
        lines = f.readlines()
        return lines


if __name__ == "__main__":
    novel_path = 'data/qing_yu_nian.txt'
    names = [
        '五竹', '李治', '李云睿', '林若甫', '范若若',
        '范思辙', '费介', '林婉儿', '柳思思', '海棠朵朵',
        '司理理', '战豆豆', '范淑宁', '红豆饭', '王启年',
        '四顾剑', '苦荷', '叶流云', '洪四庠', '影子',
        '云之澜', '叶重', '叶完', '燕小乙', '太后',
        '宁才人', '李承乾', '太子', '大皇子', '北齐大公主',
        '和亲王', '和亲王妃', '王瞳儿', '玛索索', '淑贵妃',
        '李承泽', '叶灵儿', '皇后', '李弘成', '郭攸之',
        '郭保坤', '郭铮', '贺宗纬', '朱格', '言冰云'
    ]
    novel_lines = read_novel_lines(novel_path)
    gender_list = [gender_detect(name.strip(), novel_lines) for name in names]
    print(dict(zip(names, gender_list)))
