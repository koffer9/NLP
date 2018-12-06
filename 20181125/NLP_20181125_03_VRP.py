import random
import math
from functools import wraps
import matplotlib.pylab as plt
import time

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

def stations(s):
    station = []
    for i in range(s): station.append((random.randint(-100, 100),random.randint(-100, 100)))
    return station

def get_distance(spot1,spot2):
    return math.sqrt((spot1[0]-spot2[0])**2+(spot1[1]-spot2[1])**2)
def get_route_distance(station,start,end):
    distance=[]
    route=[start]+station+[end]
    for s in range(len(route)-1):
        distance.append(get_distance(route[s],route[s+1]))
    return sum(distance)

@memo
def get_route(station,start,end):
    if len(station)==1: return station
    route=station
    for i in range(len(station)):
        left_station=list(station)
        chosen_station=left_station.pop(i)
        route1=[chosen_station]+list(get_route(left_station,chosen_station,end))
        route2=list(get_route(left_station,start,chosen_station))+[chosen_station]
        route,distance=min([(route,get_route_distance(route,start,end)),(route1,get_route_distance(route1,start,end)),(route2,get_route_distance(route2,start,end))], key=lambda x: x[1])
    return route

def plot(station):
    x,y=[],[]
    for s in station:
        x.append(s[0])
        y.append(s[1])
    plt.scatter(x, y)
    plt.gca().plot([0]+x+[0], [0]+y+[0])
    plt.scatter(0, 0, c='r',s=50)
    plt.show()

start=(0,0)
end=(0,0)
station_number = 8
cars_number = 4
station=stations(station_number)
print(station)
print('Original distance is {}'.format(round(get_route_distance(station,start,end),2)))
t=time.time()
route=get_route(station,start,end)
print('It takes {}'.format(round(time.time()-t,2)))
print(route)
print('Optimized distance is {}'.format(round(get_route_distance(route,start,end),2)))
plot(station)
plot(route)
