from progress.bar import IncrementalBar
from stopwatch import Stopwatch
from progress.bar import IncrementalBar
import random
global opts
global bubble_sort_order
bubble_sort_order = 'asc'
global speed_test_check
speed_test_check = False
stopwatch = Stopwatch()
global number
number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
def create_list(user_tup):
    global user_list
    user_list = list(user_tup)
    if number in user_list:
        user_list = [int(i) for i in user_list]
        print(user_list)
    global x
    x = len(user_list)
    x = x - 1
    if x == 0:
        return str("Please input a list with more than one item")
    return user_list, x

def speed_test(no_of_vals, **opts):
    opts.setdefault('range', (0, 99))
    opts.setdefault('type', 'int')
    opts.setdefault('verbose', False)
    opts.setdefault('order', 'asc')                
    global speed_test_check
    speed_test_check = True
    global speed_test_tuple
    speed_test_list = []
    if opts['type'] == 'str':
        ext_dict = open("wordlist.txt", "r")
        dict_list = []
        with IncrementalBar('Loading English Dictionary...', max=10000) as bar:
            for line in ext_dict:
                line = line.strip()
                dict_list.append(line)
                bar.next()
            bar.finish()
        with IncrementalBar('Generating Random Values...', max=no_of_vals) as bar:        
            for n in range(no_of_vals):
                random_int = random.randint(0, 10000)
                speed_test_list.append(dict_list[random_int])
                bar.next()
            speed_test_tuple = tuple(speed_test_list)
        print("Sorting has started...")
        sort(*speed_test_tuple, order = opts['order'])
        speed_test_check = False
        if opts['verbose'] == True:
            print(record_time(time, y), "Sorted List: ", lst)
        else:
            print(record_time(time, y))
    else:
        with IncrementalBar('Generating Random Values...', max=no_of_vals) as bar:
            for n in range(no_of_vals):
                random_int = random.randint(opts['range'][0],opts['range'][1] )
                speed_test_list.append(random_int)
                bar.next()
            speed_test_tuple = tuple(speed_test_list)
        print("Sorting has started...")
        sort(*speed_test_tuple, order = opts['order'])
        speed_test_check = False
        if opts['verbose'] == True:
            print(record_time(time, y), "Sorted List: ", lst)
        else:
            print(record_time(time, y))
        
        
def swap_vals(lst, val1, pos1, val2, pos2):
    lst.remove(val2)
    lst.insert(pos1, val2)
    lst.remove(val1)
    lst.insert(pos2, val1)
    return lst

def check_order(lst, length, order):
    check = []
    if order == 'desc':
        for n in range(length):
            if lst[n] >= lst[n+1]:
                check.append(1)
            else:
                check.append(0)
        if 0 in check:
            return True
        else:
            return False
    else:
        for n in range(length):
            if lst[n] <= lst[n+1]:
                check.append(1)
            else:
                check.append(0)
        if 0 in check:
            return True
        else:
            return False        

def record_time(time_string, no_of_items):
    no_of_items = str(no_of_items)
    return str("Bubble Sorter sorted " + no_of_items + " items in " + time_string)


    
def sort(*array, **opts):
    opts.setdefault('order', 'asc')
    stopwatch.restart()
    if opts['order'] == 'desc':
        create_list(array)
        global lst
        lst = user_list
        while check_order(lst, len(lst) - 1, 'desc'):
            for n in range(x):
                if lst[n] < lst[n+1]:
                    swap_vals(lst, lst[n], n, lst[n+1], n+1)
        stopwatch.stop()
        global time, y
        time = str(stopwatch)
        y = x + 1
        return lst, record_time(time, y)
    else:
        create_list(array)
        lst = user_list
        while check_order(lst, len(lst) - 1, 'asc'):
            for n in range(x):
                if lst[n] > lst[n+1]:
                    swap_vals(lst, lst[n], n, lst[n+1], n+1)
        stopwatch.stop()
        time = str(stopwatch)
        y = x + 1
        return lst, record_time(time, y)

def rev_sort(*array):
    sort(*(array), order='desc')
    return lst, record_time(time, y)
