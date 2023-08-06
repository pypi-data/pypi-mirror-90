#!/usr/bin/python3

import os

import glob


def untrace(file):
    print('untracing file '+file)
    flag = ' #@!$ code automatic inserted by CodeTrace $!@#'
    lines = open(file).read().split('\n')
    lines = [l for l in lines if flag not in l]
    with open(file,'wt') as F:
        F.write('\n'.join(lines))
    print('done')
def trace(file):
    print('tracing file '+file)
    flag = ' #@!$ code automatic inserted by CodeTrace $!@#'


    lines = open(file).read().split('\n')
    for l in lines:
        if flag in l:
            print('file {} has been traced, skipping'.format(file))
            return

    path,_ = os.path.split(os.path.abspath(__file__))
    pre_code = open(path+'/code_insert.py').read().split('\n')
    pre_code = [c+flag for c in pre_code]

    new_lines = pre_code
    for l in lines:
        c = l.strip()
        if len(c)>4 and c[:4] == 'def ':
            offset = l.find('def ')
            new_l = ' '*offset+'@ct_probe'+flag+'\n'+l
            new_lines += [new_l]
        else:
            new_lines += [l]

    #os.system('cp '+file+' '+file+'.ctbk')
    with open(file,'wt') as F:
        F.write('\n'.join(new_lines))
    print('done')


import sys

if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv)!=3 or sys.argv[1] not in ['trace','untrace'] :
        print('codetrace [un]trace .  ==> (un)trace all py at current folder')
        print('codetrace [un]trace **  ==> (un)trace all py recursively')
        print('codetrace [un]trace subfolder/*  ==> (un)trace all py under subfolder recursively')


        exit(1)
    if len(sys.argv)>=2:
        pattern = sys.argv[2]
        if pattern[-1] != '/':
            pattern += '/'
    else:
        pattern = ''
    all_pys = glob.glob(pattern+'*.py',recursive=True)
    print('{} of python files listed'.format(len(all_pys)))
    for file in all_pys:
        if sys.argv[1] =='trace':
            trace(file)
        else:
            untrace(file)



