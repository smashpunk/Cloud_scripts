import math
import commands
import os
import subprocess

WORK_PATH="/opt/WORK/Cloud_script/"
ANSIBLE_PATH ="/etc/ansible/hosts"
CMD="cat "+ANSIBLE_PATH+" | grep \"^\[\""
GROUP_LIST=subprocess.check_output([CMD],shell=True)
#print GROUP_LIST.split("\n")
#print GROUP_LIST.split("\n")[2]

def print_menu(list):
    menu = {}
    index=0
    NR = list.split("\n").__len__()-1
    myfile = open(WORK_PATH+'catalog', 'wb+')
## create menu from LIST
    for group in list.split("\n"):
        if index < NR:
            menu[index+1]=group
            index=index+1
## Add the final option "ALL"
    menu[index+1]="[ALL]"
    menu[index+2]="[Quit]"
## Print the menu
    key=menu.keys()
    key.sort()
    print("the List is:")
    for i in key:
        ## cut [ ] from the string
        print i, menu[i][1:-1]
    while True:
        selection=int(raw_input("Now, please select the group:"))
        if not selection:
            print("No selection made!The process will be abort...")
        if menu[selection] == '[Quit]':
            print "Will quit the process, now generate the catalog file..."
            myfile.close()
            break
        else:
            myfile.write(menu[selection][1:-1]+"\n")
            print("Nex round for selection")


## Call the function to generate the menu for ansible groups
lst=print_menu(GROUP_LIST)





