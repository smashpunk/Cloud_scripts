# -*- coding: UTF-8 -*-

import os
import json
import time
from string import upper
from aliyunsdkcore import client

## create,start,stop,reoot
from aliyunsdkecs.request.v20140526 import CreateInstanceRequest
from aliyunsdkecs.request.v20140526 import StartInstanceRequest
from aliyunsdkecs.request.v20140526 import StopInstanceRequest
from aliyunsdkecs.request.v20140526 import RebootInstanceRequest
## assgin public IP to ECS
from aliyunsdkecs.request.v20140526 import AllocatePublicIpAddressRequest
## delete
from aliyunsdkecs.request.v20140526 import DeleteInstanceRequest
## qury ECS list, running status and type
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526 import DescribeInstanceStatusRequest
from aliyunsdkecs.request.v20140526 import DescribeVSwitchesRequest

from aliyunsdkecs.request.v20140526 import DescribeImagesRequest

from Infra_function import *

def describe_instance_type(accesskey_id,accesskey_secret,region_id="cn-hangzhou"):
    clt = client.AcsClient(accesskey_id, accesskey_secret, region_id)
    request=DescribeInstanceTypesRequest.DescribeInstanceTypesRequest()
    request.set_accept_format('json')
    result=clt.do_action_with_exception(request)
    js_str=json.loads(result)
    print "Type        " + "CPU(core)    " + "Memory(GB)    "
    for i in js_str["InstanceTypes"]["InstanceType"]:
        if i["InstanceTypeFamily"] in ["ecs.n1", "ecs.n2"]:
            print i["InstanceTypeId"],"\t    ",i["CpuCoreCount"],"\t    ",i["MemorySize"]
    return

def create_instance(zone_id,accesskey_id,accesskey_secret,region_id,image_ID):
    clt = client.AcsClient(accesskey_id, accesskey_secret, region_id)
    request=CreateInstanceRequest.CreateInstanceRequest()
    request.set_accept_format('json')
    request.set_ZoneId(zone_id)
    request.set_ImageId(image_ID)
    describe_instance_type(accesskey_id,accesskey_secret,region_id)
    intance_type=raw_input("Please select ECS instance type:")
    request.set_InstanceType(intance_type)
    instance_name=raw_input("Please input ECS instance name:")
    instance_description=raw_input("Please input ECS instance description:")
    print("Please seelction instance pay charge type:")
    instance_charge=raw_input("PrePaid/PostPaid:")
    if instance_charge not in ['PrePaid','PostPaid']:
        print("Instance pay charge type is wrong! "+instance_charge)
        instance_charge=raw_input("Please input correct pay charge type: PrePaid or PostPaid")
    elif instance_charge == "PrePaid":
        request.set_Period("1")
    sys_hdd_size = raw_input("Please input the system driver size,default is 400G:")
    print("Do you want to add a DATA DISK?")
    disk_choice = raw_input("y/n:")
    if disk_choice in ['y', 'Y']:
        data_hdd_size = raw_input("Please input the data driver size,default is 400G:")
    request.set_InstanceName(instance_name)
    request.set_Description(instance_description)
    request.set_InternetChargeType('PayByTraffic')
    request.set_InternetMaxBandwidthOut('100')
    request.set_InstanceChargeType(instance_charge)
    request.set_SystemDiskCategory('cloud_efficiency')
    request.set_SystemDiskSize(sys_hdd_size)
    request.set_DataDisks(({'DataDisk': '1'}, {'Size': data_hdd_size}, {'Category': 'cloud_efficiency'}))
    vpc_id=describe_switch(accesskey_id, accesskey_secret, region_id)
    switch_id=raw_input("Please select the vSwitch_ID:")
    request.set_VSwitchId(switch_id)
    describe_sg(vpc_id,accesskey_id,accesskey_secret,region_id)
    sg_id=raw_input("Please select ECS's safe group:")
    request.set_SecurityGroupId(sg_id)
    result = clt.do_action(request)
    print result
    js_str=json.loads(result)
    instance_id=js_str["InstanceId"]
    return instance_id

def create_instance_ip(instance_id,accesskey_id,accesskey_secret,region_id):
    clt = client.AcsClient(accesskey_id, accesskey_secret, region_id)
    request=AllocatePublicIpAddressRequest.AllocatePublicIpAddressRequest()
    request.set_accept_format('json')
    request.set_InstanceId(instance_id)
    result = clt.do_action_with_exception(request)
    js_str=json.loads(result)
    print result
    print ("The public IP assigned to the ECS is "+js_str["IpAddress"])
    return
def boot_instance(instance_id,accesskey_id,accesskey_secret,region_id):
    print("Wait 30s for ECS booting...")
    print("the instance ID is "+instance_id)
    time.sleep(30)
    clt = client.AcsClient(accesskey_id, accesskey_secret, region_id)
    request=StartInstanceRequest.StartInstanceRequest()
    request.set_accept_format('json')
    request.set_InstanceId(instance_id)
    result = clt.do_action_with_exception(request)
    print result
    return

def describe_instances(instance_id,accesskey_id, accesskey_secret, region_id):
    clt = client.AcsClient(accesskey_id, accesskey_secret, region_id)
    request=DescribeInstancesRequest.DescribeInstancesRequest()
    request.set_accept_format('json')
    request.set_InstanceIds(instance_id)
    result = clt.do_action_with_exception(request)
    js_str = json.loads(result)
    InstanceName=js_str["Instances"]["Instance"][0]["InstanceName"]
    PublicIpAddress=js_str["Instances"]["Instance"][0]["PublicIpAddress"]["IpAddress"][0]
##  temp disable inventory generate
#    generate_inventory(InstanceName,PublicIpAddress)
    return

def generate_inventory(InstanceName,PublicIpAddress):
    # write ansible inventory file
    myfile = open('/opt/WORK/Cloud_scripts/Ansible/inventory', 'a+')
    myfile.write("\n")
    myfile.write("["+InstanceName+"]" + "\n")
    myfile.write(PublicIpAddress + "\n")
    myfile.write("\n")
    myfile.close()
    myfile = open('/opt/WORK/Cloud_scripts/Ansible/prometheus_new_job', 'a+')
    myfile.write("  - job_name: \"" + InstanceName + "\"" + "\n")
    myfile.write("    static_configs:\n")
    myfile.write("      - targets: ['"+PublicIpAddress + ":9100']""\n")
    myfile.close()
    return



##test scope
