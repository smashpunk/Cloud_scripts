#!/usr/bin/env bash
ANSIBLE_PATH="/etc/ansible"
WORK_PATH="/opt/WORK/Cloud_script"
ServerInit(){
    echo "Server initialization will start..."
    os_type=`ansible $1 -m setup | grep ansible_os_family| awk '{print $2}' | sed 's/\"//g;$s/,//g'`
    if [ $os_type = "RedHat" ]
        then
            echo "Update Packages"
            ansible $1 -m shell -a "yum update -y"
            echo "Send JDK 8u112 to target servers, please wait..."
            ansible $1 -m copy -a "src=$WORK_PATH/Packages/jdk-8u112-linux-x64.rpm dest=/tmp/"
            echo "Start to install jdk 8u112 x64"
            ansible $1 -m shell -a "rpm -ivh /tmp/jdk-8u112-linux-x64.rpm"
        else
            echo "Currently, this script is only sutiable for RH, the initilzation will be aborted."
    fi
}

ServerNetCheck(){
    if [ $1 = "" ]
        then
            echo "No Server Group, the process will be break!"
            break
     else
         ansible $1 -m ping | grep pong
         echo $?
         if [ $? != 1 ]
             then
                 echo "The server can be ping..."
                 echo "Wait for 5s..."
                 sleep 5
                 ServerInit $1
         fi
    fi
}
## the ansible host configuration path

STR=`cat $ANSIBLE_PATH/hosts | grep "^\[" `
OPTION=()

## add host group into OPTION array
for NAME in $STR
do
 # echo $name
  OPTION+=($NAME)
done
## append "ALL" to OPTAION array
OPTION+=("[ALL]")
#echo ${OPTION[2]}
## count the number of elements
NR=${#OPTION[@]}
#echo $NR
#echo ${OPTION[@]}
## create the menu
PS3='Choose which group you want to run on:'
select opt in "${OPTION[@]}"
do
    echo "The Group you select is: "$opt
    echo "Now, wait for generate the envrionment..."
    GROUP=`echo $opt | cut -c 2-$[${#opt}-1]`
    break
done
ServerNetCheck $GROUP



