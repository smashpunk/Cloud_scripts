# -*- coding: UTF-8 -*-

from ECS import *

FILE_PATH="/opt/WORK/Cloud_script/Aliyun/"

## read AccessKeyID and AccessKeySecret from file
fr=open(FILE_PATH+'Access_Information','r')
content=fr.readlines()
## -1 mean remove "\n" from the element
accesskey_id=content[1][12:-1]
accesskey_secret=content[2][16:-1]
region_id_default=content[3][14:-1]
fr.close()

region_id=raw_input("Please select ECS's region:")
zone_id=show_zoneid(accesskey_id,accesskey_secret,region_id)
account=int(raw_input("How many ECS instance do you want to create?"))
index=1
while (index <= account):
    instance_id = create_instance(zone_id,accesskey_id,accesskey_secret,region_id)
    print("Pause 10s for instance be ready by Aliyun!")
    time.sleep(10)
    create_instance_ip(instance_id,accesskey_id,accesskey_secret,region_id)
    boot_instance(instance_id,accesskey_id,accesskey_secret,region_id)
    describe_instances('["'+instance_id+'"]',accesskey_id,accesskey_secret,region_id)
    index=index+1
print("ECS instances finished created, please double check!")


##test scope