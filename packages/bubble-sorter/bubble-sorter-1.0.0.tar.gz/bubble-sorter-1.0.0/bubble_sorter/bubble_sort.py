def create_list(user_tup):
    global user_list
    user_list = list(user_tup)
    if '1' in user_list or '2' in user_list or '3' in user_list or '4' in user_list or '5' in user_list or '6' in user_list or '7' in user_list or '8' in user_list or '9' in user_list or '0' in user_list:
        user_list = [int(i) for i in user_list]
        print(user_list)
    global x
    x = len(user_list)
    x = x - 1
    return user_list, x

def swap_vals(lst, val1, pos1, val2, pos2):
    lst.remove(val2)
    lst.insert(pos1, val2)
    lst.remove(val1)
    lst.insert(pos2, val1)
    return lst

def check_order(lst, length):
    check = []
    for n in range(length):
        if lst[n] <= lst[n+1]:
            check.append(1)
        else:
            check.append(0)
    if 0 in check:
        return True
    else:
        return False
    
def sort(*array):
    create_list(array)
    lst = user_list
    while check_order(lst, len(lst) - 1):
        for n in range(x):
            if lst[n] > lst[n+1]:
                swap_vals(lst, lst[n], n, lst[n+1], n+1)
    return lst            
