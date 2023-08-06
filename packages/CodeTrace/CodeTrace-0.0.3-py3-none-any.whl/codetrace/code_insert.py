from pdb import set_trace
import os
import time
def get_file_name():
    try:
        return os.path.abspath(__file__)
    except:
        return ''
def get_fun_line(name):
    lines = open(get_file_name()).read().split('\n')
    loc = [i for i,l in enumerate(lines) if 'def '+name+'(' in l and l.strip()[0]!='#']
    if len(loc)!=0:
        return loc[0]
    else:
        return -1
    
def get_class_name(fun):
    fun_name = fun.__name__
    obj = '{}'.format(fun)
    if '.' in obj:
        class_name = obj.split('.')[0].split()[-1]
    else:
        class_name = ''
    return class_name,fun_name
def ct_probe(func):
    def wrapper(*arg,**kwargs):
        class_name,fun_name = get_class_name(func)

        print('--CodeTrace--|{:32}:{}|{:12}|{:12}|Start'.format(get_file_name(),get_fun_line(fun_name),class_name,fun_name))
        t = time.time()
        res = func(*arg,**kwargs)
        print('--CodeTrace--|{:32}:{}|{:12}|{:12}|End {:.5} (S)'.format(get_file_name(),get_fun_line(fun_name),class_name,fun_name,time.time()-t))
        return res
    return wrapper
