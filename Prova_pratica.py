#! /usr/bin/python3
import os
import sys
import time
import json
import random
import datetime
import fileinput
import collections

ID = 0
n_line = 0
mod_line = None 
name_file = 'File.txt'
array_check = ["True", "False"]

err_0 = 'File empty'
id_3 = 'Max ID number is:'
row_2 = name_file + ' has row:'
err_1 = 'Not correct data insert'

def check_file():
    global ID
    global n_line
    if not os.path.exists(name_file):
        text_file = open(name_file,'w+')
        print ('')
        print ('New File.txt created')
    else:
        n_line = 0
        text_file = open(name_file,'r')
        for line in text_file:
            n_line += 1
            read_line = json.loads(line)
            if read_line['ID'] > ID:
                ID = read_line['ID']
            if n_line == 0 :
                ID = 0
                break            
    print ('')
    print (row_2, n_line)
    print (id_3, ID)
    text_file.close()

### Action
def choose_h():
    print (' h​ >>> mostra tutti le possibili action ') 
    print (' ls​ >>> mostra tutti i todos ordinati per data di inserimento decrescente ') 
    print (' a (params: title)​ >>> aggiunge un todo ')
    print (' e (params: id, title)​ >>> edita un todo ') 
    print (' d (params: id)​ >>> cancella un todo ') 
    print (' t (params: id)​ >>> fa il toggle del todo (done: true VS done: false) ') 
    print (' s (params: il termine da cercare)​ >>> cerca tra i todos e ritorna i todos contenenti il termine ricercato nel titolo ')
    print (' q >>> chiude il programma')

### ToDos list
def choose_ls():
    global n_line
    text_file = open(name_file,'r')
    for line in text_file:
        print (line, end = '')
    text_file.close()
    check_file()

### Add ToDo
def choose_a():
    global ID
    todo_dic = collections.OrderedDict()
    print('Add todo with Title with almost 5 letter: ', end = '')
    in_todo = input()
    if in_todo == '' or len(in_todo) < 5:     
        print(err_1)
        print('')
        choose_a()
    else:
        timenow = datetime.datetime.now()
        timestamp = (timenow.strftime('%d/' + '%m/' + '%Y ' + '%X '))
        ## array true false random (Check)
        check = random.randint(0,1)
        ID += 1
        todo_dic['ID'] = ID
        todo_dic['Title'] = in_todo
        todo_dic['Create Data'] = timestamp
        todo_dic['Done'] = array_check[check]
        json_todo_add = json.dumps(todo_dic)
        print ('New todo is: ', json_todo_add)
        with open(name_file, 'r') as old_file: old_data = old_file.read()
        with open(name_file, 'w') as new_file: new_file.write(json_todo_add + '\n' + old_data)
    choose_ls()

### Edit ToDo
def choose_e_t(todo_ID, new_Title):
    global n_line
    global mod_line
    str_todo_ID = '"ID": ' + todo_ID
    text_file = open(name_file,'r')
    for line in text_file:
        if str_todo_ID in line :
            print ('Todo chosen is: ', line, end = '')
            mod_line = json.loads(line)
    text_file.close()   
    write_mod = collections.OrderedDict()
    write_mod['ID'] = mod_line['ID']
    if not new_Title == '':
        write_mod['Title'] = new_Title
        write_mod['Create Data'] = mod_line['Create Data']
        write_mod['Done'] = mod_line['Done']
    else:
        write_mod['Title'] = mod_line['Title']
        write_mod['Create Data'] = mod_line['Create Data']
        if mod_line['Done'] == array_check[0]:
            write_mod['Done'] = array_check[1]
        else:
            write_mod['Done'] = array_check[0]
    json_todo_mod = json.dumps(write_mod) + '\n'
    print('Todo mod now is ', json_todo_mod)
    old_line = line
    for line in fileinput.input(name_file, inplace = 1):
        if str_todo_ID in line:
            line = line.replace(line, json_todo_mod)
        sys.stdout.write(line)
fileinput.close()
choose_ls()

### remove ToDo
def choose_d():
    global n_line
    global ID
    print('Insert todo ID you want delete: ',end = '')
    todo_remove = input()
    if todo_remove == '' or int(todo_remove) > int(ID) or int(todo_remove) == 0 :
        print (err_1)
        print('')
        choose_d()
    else :
        text_file = open(name_file,'r').readlines()
        with open(name_file, 'w') as write_file:
            for index,line in enumerate(text_file):
                n_line += 1
                read_line = json.loads(line)
                ID = read_line['ID']
                if int(ID) != int(todo_remove):
                    write_file.write(line)
    print('Todo delete')
    choose_ls()

### Quit
def choose_q():
    print ('|------|')
    print ('| Quit |')
    print ('|------|')
    print ('')
    exit()

def start():
    while True:    
        print('')
        print ('Choose a letter, press h for see all commands: ', end = '')
        choose = input()
        print('')
        if n_line == 0:
            if choose == 'ls' or choose == 'e' or choose == 'd':
                print (err_0)
                start()
            else: 
                if choose == 'h':
                    choose_h()
                else:
                    choose == 'a'
                    choose_a()
        else:
            if choose == 'h':
                choose_h()
            elif choose == 'ls':
                choose_ls()
            elif choose == 'a':
                choose_a()
            elif choose == 'e':
                while True:
                    print('Insert original ID you want change Title: ',end = '')
                    todo_ID = input()     
                    if todo_ID == '' or int(todo_ID) == 0 or int(todo_ID) > ID:
                        print (err_1)
                        print('')
                    else:
                        print('Insert new Title with almost 5 letter: ', end = '')
                        new_Title = input()
                        if new_Title == '' or len(new_Title) < 5:
                            print(err_1)
                        else:
                            choose_e_t(todo_ID, new_Title)
                            break
            elif choose == 'd':
                choose_d()
            elif choose == 't':
                while True:
                    print('Insert ID you want switch Done value: ',end = '')
                    todo_ID = input()
                    if todo_ID == '' or int(todo_ID) == 0 or int(todo_ID) > ID:
                        print (err_1)
                        print('')
                    else:
                        new_Title = ''
                        choose_e_t(todo_ID, new_Title)
                    break
            elif choose == 'q':
                choose_q()               
            else:
                print(err_1)
### Start
print(' ')
print ('|-------|')
print ('| Start |')
print ('|-------|')

check_file()
start() 