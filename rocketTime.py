#### libraries ###
import time

###### Global Var ########
start_time = 0


def start_timer():
    global start_time
    start_time = time.time()


def get_time():
    return time.time() - start_time
