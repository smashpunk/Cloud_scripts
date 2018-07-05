# -*- coding: UTF-8 -*-

from ECS import *

#FILE_PATH="/opt/WORK/Cloud_scripts/Aliyun/"
FILE_PATH="C:\Users\Qu\Desktop\Cloud_Test\Cloud_scripts\Aliyun\/"
## read AccessKeyID and AccessKeySecret from file
fr=open(FILE_PATH+'Access_Information','r')
content=fr.readlines()
## -1 mean remove "\n" from the element
accesskey_id=content[1][12:-1]
accesskey_secret=content[2][16:-1]
region_id_default=content[3][14:-1]
fr.close()
region_info = {
    "青岛": "cn-qingdao",
    "北京": "cn-beijing",
    "杭州": "cn-hangzhou",
    "上海": "cn-shanghai",
    "深圳": "cn-shenzhen",
    "香港": "cn-hongkong",
    "新加坡": "ap-southeast-1",
    "悉尼": "ap-southeast-2",
    "东京": "ap-northeast-1",
    "硅谷": "us-west-1",
    "弗吉尼亚": "us-east-1",
    "法兰克福": "eu-central-1",
    "迪拜": "me-east-1"
}
print("Below is the region information, pls check at https://help.aliyun.com/document_detail/53289.html?spm=5176.product29991.6.587.WTfHZW&parentId=29991 ")
for region in region_info:
    print region + ":" + region_info[region]
print("The default region is 杭州: cn-hangzhou")

region_id=raw_input("Please select ECS's region:")
zone_id=show_zoneid(accesskey_id,accesskey_secret,region_id)
account=int(raw_input("How many ECS instance do you want to create?"))
index=1
AMI=raw_input("Please input the Image ID:")
while (index <= account):
    instance_id = create_instance(zone_id,accesskey_id,accesskey_secret,region_id,AMI)
    print("Pause 10s for instance be ready by Aliyun!")
    time.sleep(10)
    create_instance_ip(instance_id,accesskey_id,accesskey_secret,region_id)
    boot_instance(instance_id,accesskey_id,accesskey_secret,region_id)
    describe_instances('["'+instance_id+'"]',accesskey_id,accesskey_secret,region_id)
    index=index+1
print("ECS instances finished created, please double check!")


##test scope