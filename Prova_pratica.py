#! /usr/bin/python3
import os
import sys
import time
import json
import random
import datetime
import fileinput
import collections

n_id = 0
n_line = 0
id_list = []
mod_line = None 
str_search = None
choose_letter = None
name_file = 'File.txt'
array_check = ["True", "False"]

err_0 = 'File empty'
id_3 = 'Max ID number is:'
row_2 = name_file + ' has row:'
err_1 = 'Not correct data insert'

### Check file and read it
def check_file():
    global n_id
    global n_line
    global id_list
    if not os.path.exists(name_file):
        text_file = open(name_file,'w+')
        print ('')
        print ('New File.txt created')
    else:
        n_id = 0
        n_line = 0
        id_list = []
        text_file = open(name_file,'r')
        for line in text_file:
            try:
                read_line = json.loads(line)
                id_list.append(read_line['ID'])
            except (ValueError):
                text_file.close()
                name_corruput_file = 'File_corrupt_' + str(datetime.datetime.now())
                os.rename(name_file,name_corruput_file)
                print('')
                print (name_file, ' is corrupt !!!')
                print('Corrupt file save as: ', name_corruput_file)
                os.remove(name_file)
                check_file()
            n_line += 1
            if read_line['ID'] > n_id:
                 n_id = read_line['ID']            
    print ('')
    print (row_2, n_line)
    print (id_3, n_id)
    print ('List ID :', id_list)
    text_file.close()
    start()

### Check keyboard input
def check_input(choose_letter):
    if choose_letter == 'e':
        print_text_input = 'Insert original ID you want change Title: '
    elif choose_letter == 'd':
        print_text_input = 'Insert todo ID you want delete: '
    elif choose_letter == 't':
        print_text_input = 'Insert the ID you want switch toggle: '
    else:
        print(err_1)
        start()
    while True:
        try:
            print(print_text_input, end = '')
            todo_id = int(input())     
            try:
                if id_list.count(todo_id):
                    break
                else: 
                    print (err_1)
            except ValueError :
                print (err_1)
        except ValueError :
            print (err_1)
    if choose_letter == 'e':
        print('Insert new Title with almost 5 letter: ', end = '')
        new_Title = input()
        if new_Title == '' or len(new_Title) < 5:
            print(err_1)
            choose_letter = 'e'
            check_input(choose_letter)
        else:
            choose_e_t(todo_id, new_Title)    
    elif choose_letter == 'd':
        todo_remove = todo_id
        choose_d(todo_remove)
    elif choose_letter == 't':
        new_Title = None
        choose_e_t(todo_id, new_Title)
          
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
def choose_ls_s(str_search):
    global n_line
    text_file = open(name_file,'r')
    flag = 0
    for line in text_file:
        if str_search == None:
            print (line, end = '') 
        elif str_search in line:
            print('Word find in ID: ')
            print(line, end = '')
            flag = 1
    if flag == 0 and not str_search == None:    
        print('Not word ', str_search, 'find to file ')
    text_file.close()
    check_file()

### Add ToDo
def choose_a():
    global n_id
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
        check = random.randint(0,1) ## array true false random (Check)
        n_id += 1
        todo_dic['ID'] = n_id
        todo_dic['Title'] = in_todo
        todo_dic['Create Data'] = timestamp
        todo_dic['Done'] = array_check[check]
        json_todo_add = json.dumps(todo_dic)
        print ('New todo is: ', json_todo_add)
        with open(name_file, 'r') as old_file: old_data = old_file.read()
        with open(name_file, 'w') as new_file: new_file.write(json_todo_add + '\n' + old_data)
        check_file()

### Edit ToDo or switch toggle
def choose_e_t(todo_id, new_Title):
    global n_line
    global mod_line
    str_todo_id = '"ID": ' + str(todo_id) + ','
    text_file = open(name_file,'r')
    n_line = 0
    for line in text_file:
        n_line += 1
        if str_todo_id in line :
            print ('Todo chosen is: ', line, end = '')
            json_line_mod = line
            mod_line = json.loads(line)
    text_file.close()   
    write_mod = collections.OrderedDict()
    write_mod['ID'] = mod_line['ID']
    if not new_Title == None:
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
    n_line = 0
    for line in fileinput.input(name_file, inplace = True): 
        if str_todo_id  in line:
            line = line.replace(json_line_mod, json_todo_mod)
        sys.stdout.write(line)
    print('ID to rewrite is ', str_todo_id) 
    check_file()

### remove ToDo
def choose_d(todo_id):
    global n_line
    global n_id
    text_file = open(name_file,'r').readlines()
    with open(name_file, 'w') as write_file:
        for index,line in enumerate(text_file):
            n_line += 1
            read_line = json.loads(line)
            n_id = read_line['ID']
            if int(n_id) != int(todo_id):
                write_file.write(line)
    print('Todo delete')
    check_file()

### Quit
def choose_q():
    print ('|------|')
    print ('| Quit |')
    print ('|------|')
    print ('')
    exit()

def start():
    global str_search
    global choose_letter
    while True:    
        print('')
        print ('Choose a letter, press h for see all commands: ', end = '')
        choose = input()
        print('')
        if n_line == 0:
            if choose == 'ls' or choose == 'e' or choose == 'd' or choose == 't' or choose == 's':
                print (err_0)
                start()
            else: 
                if choose == 'h':
                    choose_h()
                elif choose == 'a':
                    choose_a()
                elif choose == 'q':
                    choose_q()
                else:
                    print (err_1)
                    start()
        else:
            if choose == 'h':
                choose_h()
            elif choose == 'ls':
                str_search = None
                choose_ls_s(str_search)
            elif choose == 'a':
                choose_a()      
            elif choose == 'e' or choose == 'd' or choose == 't':
                choose_letter = choose
                check_input(choose_letter)
            elif choose == 's':
                while True:
                    print('Write the word to search: ', end = '')
                    str_search = input()
                    if str_search == '':
                       print (err_1)
                    else:  
                        break
                choose_ls_s(str_search)        
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