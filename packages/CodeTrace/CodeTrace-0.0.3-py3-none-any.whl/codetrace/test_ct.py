import os
import time                                                                                                               
def get_file_name():
    try:
        return os.path.abspath(__file__)
    except:
        return ''
def get_class_name(fun):
    fun_name = fun.__name__
    obj = '{}'.format(fun)
    if '.' in obj:
        class_name = obj.split('.')[0].split()[-1]
    else:
        class_name = ''
    return class_name,fun_name                                                                                                                            
def measure_time(func):                                                                                                   
    def wrapper(*arg,**kwargs):       
        class_name,fun_name = get_class_name(func)
        
        print('--CodeTrace--:  {:12} | {:12} | {:12} \t| Start'.format(get_file_name(),class_name,fun_name))                                           
        t = time.time()    
        res = func(*arg,**kwargs)
        print('--CodeTrace--:  {:12} | {:12} | {:12} \t| End {:.5} (S)'.format(get_file_name(),class_name,fun_name,time.time()-t))                                           
        return res                                                                                                          
    return wrapper                                                                                                          
                                                                                                                          
@measure_time                                                                                                             
def myFunction(n,t=1):                                                                                                        
    time.sleep(n+t)                                                                                                           
                                                                                                                          
if __name__ == "__main__":                                                                                                
    myFunction(1)   
    
class myclass:
    @measure_time
    def __init__(self,):
        self.myfun()
        return
        #print('init')
    @measure_time
    def myfun(self,):
        return
        #print('myfun')
a = myclass()
a.myfun()

        
