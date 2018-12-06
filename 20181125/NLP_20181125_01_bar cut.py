from collections import defaultdict
from functools import lru_cache
from functools import wraps
def memo(func):
    cache = {}
    @wraps(func)
    def __wrap(*args, **kwargs):
        str_key = str(args) + str(kwargs)
        if str_key not in cache:
            result = func(*args, **kwargs)
            cache[str_key] = result
        return cache[str_key]
    return __wrap

prices = defaultdict(lambda : -float('inf')) #defaultdict定义字典类型，避免不曾存在的键报错。lambda设置默认的值。-float('inf')意思是？
for i, v in enumerate([1, 5, 8, 9, 10, 17, 17, 20, 24, 30]): #既返回索引又返回值
    prices[i+1] = v

solution = {}
@memo
def revenue(r):
    split, r_star = max([(0, prices[r])] + [(i, revenue(i) + revenue(r-i)) for i in range(1, r)], key=lambda x: x[1]) #lambda函数第一个参数需要处理的变量，第二个函数为指定处理的元素，lambda为匿名函数
    solution[r] = (split, r-split)
    return r_star
print(revenue(40))
print(solution)

def parse_solution(r, revenue_solution):
    left, right = revenue_solution[r]
    if left == 0: return [right]
    return [left] + parse_solution(right, revenue_solution)
print(parse_solution(32, solution))

