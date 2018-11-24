simple_grammar = """
sentence => noun_phrase verb_phrase
noun_phrase => Article Adj* noun
Adj* => null | Adj Adj*
verb_phrase => verb noun_phrase
Article => 一个 | 这个
noun => 女人 |  篮球 | 桌子 | 小猫
verb => 看着 |  坐在 | 听着 | 看见 
Adj => 蓝色的 |  好看的 | 小小的
"""


def rule(grammar=simple_grammar, sp='=>'):
    result={}
    for line in grammar.split('\n'):
        if not line: continue
        header,value=line.split(sp)
        result[header.strip()]=[v.split() for v in value.split('|')]
    # print(result)
    return result


import random


def generator(rule,header='sentence'):
    if header not in rule: return header
    choice=random.choice(rule[header])
    tokens=[generator(rule,c) for c in choice]
    return ''.join([t for t in tokens if t!='null'])


r=rule()
print(generator(r,'sentence'))
