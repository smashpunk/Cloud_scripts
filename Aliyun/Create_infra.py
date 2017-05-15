# -*- coding: UTF-8 -*-

import os
import json
from string import upper
from aliyunsdkcore import client
import aliyunsdkecs
from aliyunsdkecs.request.v20140526 import DescribeInstanceStatusRequest
from aliyunsdkecs.request.v20140526 import DescribeRegionsRequest
from aliyunsdkecs.request.v20140526 import CreateSecurityGroupRequest
from aliyunsdkecs.request.v20140526 import CreateVpcRequest
from aliyunsdkecs.request.v20140526 import CreateVSwitchRequest

from Infra_function import *

FILE_PATH="/opt/WORK/Cloud_scripts/Aliyun/"

## read AccessKeyID and AccessKeySecret from file
fr=open(FILE_PATH+'Access_Information','r')
content=fr.readlines()
## -1 mean remove "\n" from the element
accesskey_id=content[1][12:-1]
accesskey_secret=content[2][16:-1]
region_id_default=content[3][14:-1]
fr.close()

print("Do you want to create a new VPC?")
vpc_selection=upper(raw_input("Y/N:"))
if vpc_selection == "Y":
    vpc_name=raw_input("Please input new VPC's name which can NOT contain blankspace:")
    region_id=raw_input("Please select the region you want to use:")
    vpc_id=create_vpc(vpc_name,accesskey_id,accesskey_secret,region_id)
    print("Do you want to create switch for new VPC?")
    switch_selection=upper(raw_input("Y/N:"))
    if switch_selection == "Y":
        print("Below is the ZoneId in the region " + region_id)
        zone_id = show_zoneid(accesskey_id,accesskey_secret,region_id)
        create_swtich(zone_id,vpc_id,accesskey_id,accesskey_secret,region_id)
        sg_id = create_sg(vpc_id,accesskey_id,accesskey_secret,region_id)
        create_sg_policy(sg_id,accesskey_id,accesskey_secret,region_id)
elif vpc_selection == "N":
    menu={}
    menu[1]="create vSwitch"
    menu[2]="create safe_group"
    menu[3]="create safe_group policy"
    menu[4]="modify safe_group policy"
    menu[5]="QUIT"
    i=1
    for i in menu.keys():
        print i,menu[i]
    selection = int(raw_input("Please selection the action:"))
    if selection == 1:
        region_id=raw_input("Please select the region you want to use:")
        describe_vpc(accesskey_id,accesskey_secret,region_id)
        vpc_id=raw_input("Please paste VPC_ID at here:")
        zone_id = show_zoneid(accesskey_id, accesskey_secret, region_id)
        print("You have select zone: "+zone_id)
        create_swtich(zone_id, vpc_id, accesskey_id, accesskey_secret, region_id)
    elif selection == 2:
        region_id = raw_input("Please select the region you want to use:")
        describe_vpc(accesskey_id, accesskey_secret, region_id)
        vpc_id = raw_input("Please paste VPC_ID at here:")
        sg_id = create_sg(vpc_id, accesskey_id, accesskey_secret, region_id)
        create_sg_default_policy(sg_id,accesskey_id,accesskey_secret,region_id)
    elif selection == 3:
        region_id = raw_input("Please select the region you want to use:")
        describe_vpc(accesskey_id, accesskey_secret, region_id)
        vpc_id = raw_input("Please paste VPC_ID at here:")
        describe_sg(vpc_id,accesskey_id,accesskey_secret,region_id)
        sg_id=raw_input("Please select which safe group's policy you want to add:")
        describe_sg_policy(sg_id,accesskey_id,accesskey_secret,region_id)
        create_result=create_sg_policy(sg_id,accesskey_id,accesskey_secret,region_id)
        print create_result
    elif selection == 4:
        region_id = raw_input("Please select the region you want to use:")
        describe_vpc(accesskey_id, accesskey_secret, region_id)
        vpc_id = raw_input("Please paste VPC_ID at here:")
        describe_sg(vpc_id,accesskey_id, accesskey_secret, region_id)
        sg_id = raw_input("Please select which safe group's policy you want to modify:")
        describe_sg_policy(sg_id, accesskey_id, accesskey_secret, region_id)
        modify_sg_policy(sg_id,accesskey_id,accesskey_secret,region_id)
else:
    print("Your type is wrong! The network infra process will abort...")


##test scope








