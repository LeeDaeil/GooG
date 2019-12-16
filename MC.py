import matplotlib.pyplot as plt
import random
import math


def fun(x):
    a, b = 1.5, 1
    return pow((-1/b)*math.log(1-x), (1/a))

def Fun(x):
    a, b = 1.5, 1
    return 1-math.exp(pow(-b * x, a))

get_rand_val = [random.random() for _ in range(400)]
get_x_from_rand_val = [fun(_) for _ in get_rand_val]
get_y_from_x_val = [Fun(_) for _ in get_x_from_rand_val]
plt.plot(get_x_from_rand_val, get_y_from_x_val)