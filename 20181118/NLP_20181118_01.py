import re
import requests
source='https://baike.baidu.com/'

# 给线索获得列表
def get_list(clue,key,table_scopes):
    if not clue: print('找不到相关信息')
    url=source+'item/'+clue
    headers = {"User-Agent" : "User-Agent:Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"}
    content = requests.get(url, headers=headers).content.decode('utf8')
    list=[]
    for table_scope in table_scopes:
        table_start, table_end = table_scope.split('|')
        if table_start not in content: continue
        table = re.findall(r""+table_start+"(.+?)"+table_end,content, re.S)[0]
        #print(table)
        #list=[]
        for l in re.findall(r'>(\w+)'+key+'<',table):
            list.append(l+key)
            if len(list)>1 and list[-1]==list[-2]: list.pop(-1)
        if list: break
    if list==[]: print('找不到信息')
    #print(list)
    #print(len(list))
    return list

# 列表转换图形
def graph(city,rule_line,rule_station):
    graph={}
    lines = get_list(city+rule_line.split('///')[0],rule_line.split('///')[1],rule_line.split('///')[2].split('//'))
    for line in lines:
        stations = get_list(line,rule_station.split('///')[0],rule_station.split('///')[1].split('//'))
        for s in range(len(stations)):
            if stations[s] not in graph: graph[stations[s]]=set()
            if s==0: graph[stations[s]].add(stations[1])
            elif s==len(stations)-1: graph[stations[s]].add(stations[len(stations)-2])
            else:
                graph[stations[s]].add(stations[s-1])
                graph[stations[s]].add(stations[s+1])
        print('{}：{}'.format(line,stations))
    #print(graph)
    return graph
    #for key, value in graph.items():
        #print('{len} | {key}:{value}'.format(len=len(value), key = key, value = value))


def get_successors(froninter, graph):
    return graph[froninter]

def is_goal(node):
    return node==destination

def search_destination(graph, start,is_goal,strategy_func):
    if start not in graph:
        print('起点站不在线路中！')
        return
    pathes = [[start]] #用来储存多条路线的列表，每条路线本身均是一个列表
    seen = set() #访问过的站点记录在see集合里
    chosen_pathes = []
    while pathes: #只要存在尚未访问完成的线路，即最后一站不在seen里，则循环print('pathes before pop are: {}'.format(pathes))
        path = pathes.pop(0) #取出一条路线继续访问print('path is: {}'.format(path))
        frontier = path[-1] #从该条被取出的路线的最后一站开始继续访问print('frontier is: {}'.format(frontier))
        if frontier in seen: continue #如果最后一站是访问过的，则不再访问，跳出循环，也不将该路线放回列表，即放弃该路线
        for station in get_successors(frontier, graph): #历遍该站点连接的下一站点
            if station in path: continue  #如果连接的下一站点已经存在于该路线，则跳出循环，不记录此下一站点
            new_path = path + [station] #否则，如果连接的下一站点尚不存在于该路线，为新站点，则将此站点纳入该路线，作为最后一站print('new_path is: {}'.format(new_path))
            pathes.append(new_path) #并将延长后的路线放回路线列表中，稍后续继续访问print('pathes.append is: {}'.format(pathes))
            if is_goal(station): #如果发现的下一站已经达到目标，则直接返回该路线
                chosen_pathes.append(new_path) #储存所有达到目标的路线
                print('No. {} possible path is: {}'.format(len(chosen_pathes), new_path))
        seen.add(frontier) #访问站点完毕，循环结束，把该站点放入seenprint('seen is: {}'.format(seen))
    chosen_pathes = strategy_func(chosen_pathes)[0]
    print('Strategic chosen path is: {}'.format(chosen_pathes))
    if not chosen_pathes:
        print('终点不在线路中！')
        return
    #for p in chosen_pathes: print('possible path: {}'.format(p))
    #print('chosen_pathes is: {}'.format(chosen_pathes))
    return chosen_pathes

def get_path_distance(pathes):
    return len(pathes)
def sort_pathes(pathes, func):
    return sorted(pathes, key=func)
#def comprehensive_sort(pathes):
#    return sort_pathes(pathes, lambda p: (len(p) + get_path_distance(p)), beam=30)
def mini_change_station(pathes):
    return sort_pathes(pathes, lambda p: len(p))
def min_distance(pathes):
    return sort_pathes(pathes, lambda p:get_path_distance(p))
#def most_view(pathes):
#    return sor
#graph={'A':['B'],'B':['A','C','X'],'C':['B','D'],'D':['C','E'],'E':['D','X'],'X':['B','E']} #例子

rule_line='地铁///线///</span>运行时间|</span>//</span>运营时间|</span>//</span>运营线路|</span>'
rule_station='站///线车站列表|</table>//</span>车站列表|</table>//运营时刻表|</table>'
graph=graph('北京',rule_line,rule_station)
start='国家图书馆站'
destination='西单站'


search_destination(graph, start, is_goal,mini_change_station)
