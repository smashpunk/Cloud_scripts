# -*- coding: UTF-8 -*-
import os
import json
import math
from string import upper

from aliyunsdkcore import client

from aliyunsdkecs.request.v20140526 import DescribeInstanceStatusRequest
from aliyunsdkecs.request.v20140526 import DescribeRegionsRequest
from aliyunsdkecs.request.v20140526 import DescribeZonesRequest
from aliyunsdkecs.request.v20140526 import DescribeVpcsRequest
from aliyunsdkecs.request.v20140526 import DescribeSecurityGroupsRequest
from aliyunsdkecs.request.v20140526 import DescribeSecurityGroupAttributeRequest
from aliyunsdkecs.request.v20140526 import DescribeInstanceTypesRequest
from aliyunsdkecs.request.v20140526 import DescribeVSwitchesRequest

from aliyunsdkecs.request.v20140526 import CreateSecurityGroupRequest
from aliyunsdkecs.request.v20140526 import CreateVpcRequest
from aliyunsdkecs.request.v20140526 import CreateVSwitchRequest
from aliyunsdkecs.request.v20140526 import CreateSecurityGroupRequest
from aliyunsdkecs.request.v20140526 import AuthorizeSecurityGroupRequest
from aliyunsdkecs.request.v20140526 import CreateInstanceRequest
from aliyunsdkecs.request.v20140526 import RevokeSecurityGroupRequest



def create_vpc(vpc_name,accesskey_id,accesskey_secret,region_id="cn-hangzhou"):
    "create VPC"
    print("the target region is "+region_id)
    clt = client.AcsClient(accesskey_id, accesskey_secret, region_id)
    request=CreateVpcRequest.CreateVpcRequest()
    request.set_accept_format('json')
    request.set_VpcName(vpc_name)
    request.set_CidrBlock('10.64.0.0/16')
    request.set_Description(vpc_name)
    result=clt.do_action_with_exception(request)
    #print result
    js_str=json.loads(result)
    return js_str["VpcId"]

def describe_vpc(accesskey_id,accesskey_secret,region_id="cn-hangzhou"):
    print("the target region is " + region_id)
    clt=client.AcsClient(accesskey_id, accesskey_secret, region_id)
    request=DescribeVpcsRequest.DescribeVpcsRequest()
    request.set_accept_format('json')
    result = clt.do_action_with_exception(request)
    js_str=json.loads(result)
    print("the VPC list is is below, for your reference!")
    for i in js_str["Vpcs"]["Vpc"]:
        print i["VpcId"],"\t",i["VpcName"],"\t",i["Description"],"\t",i["RegionId"],"\t",i["CreationTime"]
    return

def create_swtich(zone_id,vpc_id,accesskey_id,accesskey_secret,region_id):
    switch_name=raw_input("Please input your switch name:")
    cidr_block=raw_input("Please input the Cidr block:")
    clt = client.AcsClient(accesskey_id, accesskey_secret, region_id)
    request=CreateVSwitchRequest.CreateVSwitchRequest()
    request.set_accept_format('json')
    request.set_VpcId(vpc_id)
    request.set_ZoneId(zone_id)
    request.set_CidrBlock(cidr_block)
    request.set_VSwitchName(switch_name)
    result = clt.do_action_with_exception(request)
    print result
    return

def describe_switch(accesskey_id,accesskey_secret,region_id):
    describe_vpc(accesskey_id,accesskey_secret,region_id)
    vpc_id=raw_input("Please select the correct VPC:")
    clt = client.AcsClient(accesskey_id, accesskey_secret, region_id)
    request=DescribeVSwitchesRequest.DescribeVSwitchesRequest()
    request.set_VpcId(vpc_id)
    request.set_accept_format('json')
    result = clt.do_action_with_exception(request)
    js_str=json.loads(result)
    for i in js_str["VSwitches"]["VSwitch"]:
        print i["VSwitchName"],i["VSwitchId"],i["CidrBlock"],i["ZoneId"]
    return vpc_id

def create_sg(vpc_id,accesskey_id,accesskey_secret,region_id):
    sg_name=raw_input("Please input your safe group name:")
    clt = client.AcsClient(accesskey_id, accesskey_secret, region_id)
    request = CreateSecurityGroupRequest.CreateSecurityGroupRequest()
    request.set_accept_format('json')
    request.set_SecurityGroupName(sg_name)
    print("Which kind of safe group do you prefer, Classic or VPC?")
    selection=upper(raw_input("(C)lassic/(V)PC:"))
    if selection == "C":
        result=clt.do_action_with_exception(request)
    elif selection == "V":
        request.set_VpcId(vpc_id)
        result=clt.do_action_with_exception(request)
    else:
        print("Please input C for classic Or V for vpc!")
    js_str=json.loads(result)
    sg_id= js_str["SecurityGroupId"]
    print("SafeGroup create succefully!")
    return sg_id

def describe_sg(vpc_id,accesskey_id,accesskey_secret,region_id):
    clt = client.AcsClient(accesskey_id, accesskey_secret, region_id)
    request= DescribeSecurityGroupsRequest.DescribeSecurityGroupsRequest()
    request.set_accept_format('json')
    request.set_VpcId(vpc_id)
    result = clt.do_action_with_exception(request)
    js_str=json.loads(result)
    for i in js_str["SecurityGroups"]["SecurityGroup"]:
        print i["SecurityGroupId"],"\t",i["SecurityGroupName"],"\t",i["Description"],"\t",i["CreationTime"]
    return

def create_sg_policy(sg_id,accesskey_id,accesskey_secret,region_id):
    print("Now, we will create safe group policy...")
    while True:
        clt = client.AcsClient(accesskey_id, accesskey_secret, region_id)
        request = AuthorizeSecurityGroupRequest.AuthorizeSecurityGroupRequest()
        request.set_SecurityGroupId(sg_id)
        ip_protocol=raw_input("Please select the protocol, the protocol can be tcp/udp/icmp/gre/all:")
        ## the protocol can be (tcp/uncp/icmp/gre/all)
        request.set_IpProtocol(ip_protocol)
        ## tcp/udcp, the port range can be 1~65535
        ## icmp, the port range is -1/-1
        ## gre, the port range is -1/-1
        ## if choose all, the port range is -1/-1
        port_range=raw_input("Please select port range:")
        request.set_PortRange(port_range)
        ## 0.0.0.0/0 means allow world-wide connection
        source_ip=raw_input("Please select the source IP segment:")
        request.set_SourceCidrIp(source_ip)
        ## Policy can be (accept/deny), the default is accpet
        policy=raw_input("Will this policy be accpet or deny:")
        if policy in ['accept','deny']:
            request.set_Policy(policy)
        request.set_accept_format('json')
        request.set_Priority('10')
        result = clt.do_action_with_exception(request)
        print("Do you want to create a new policy?")
        selection=upper(raw_input("Y/N:"))
        ## judge if the loop can be processed
        if selection == 'N':
            break
    return result

def modify_sg_policy(sg_id,accesskey_id,accesskey_secret,region_id):
    while True:
        print("Now, we will modify safe group ingress policy...")
        print("First, we need to REVOKE the policy...")
        ip_protocal=raw_input("Please select protocal:")
        port_range=raw_input("Please select port range:")
        source_cidr=raw_input("Please select source CiDr block:")
        clt = client.AcsClient(accesskey_id, accesskey_secret, region_id)
        request=RevokeSecurityGroupRequest.RevokeSecurityGroupRequest()
        request.set_accept_format('json')
        request.set_SecurityGroupId(sg_id)
        request.set_IpProtocol(ip_protocal)
        request.set_PortRange(port_range)
        request.set_SourceCidrIp(source_cidr)
        result=clt.do_action_with_exception(request)
        print result
        print("Do you want to create a new policy?")
        selection=upper(raw_input("Y/N:"))
        if selection== "Y":
            create_sg_policy(sg_id,accesskey_id,accesskey_secret,region_id)
        print("Do you want to modify another safe group policy?")
        choice=upper(raw_input("Y/N:"))
        if choice == "N":
            break
    return

def describe_sg_policy(sg_id,accesskey_id,accesskey_secret,region_id):
    print("Now, the region is " + region_id)
    clt = client.AcsClient(accesskey_id, accesskey_secret, region_id)
    request=DescribeSecurityGroupAttributeRequest.DescribeSecurityGroupAttributeRequest()
    request.set_accept_format('json')
    request.set_SecurityGroupId(sg_id)
    result = clt.do_action_with_exception(request)
    js_str=json.loads(result)
    print "SourceCidrIp    "+"DestCidrIp    "+"Direction    "+"PortRange    "+"IpProtocol    "+"Policy"
    for i in js_str["Permissions"]["Permission"]:
        print i["SourceCidrIp"],"\t",i["DestCidrIp"],"\t",i["Direction"],"\t",i["PortRange"],"\t",i["IpProtocol"],"\t",i["Policy"]
    return


def show_zoneid(accesskey_id,accesskey_secret,region_id):
    print("Now, the region is "+region_id)
    clt = client.AcsClient(accesskey_id, accesskey_secret, region_id)
    request=DescribeZonesRequest.DescribeZonesRequest()
    request.set_accept_format('json')
    result=clt.do_action_with_exception(request)
    menu = {}
    index = 0
    js_str = json.loads(result)
    for i in js_str["Zones"]["Zone"]:
        #print i["ZoneId"]
        menu[index]=i["ZoneId"]
        index = index+1
    key = menu.keys()
    key.sort()
    for k in key:
        print k,menu[k]
    print("NOTE: VPC resource only located at 北京可用区A/C、杭州可用区B/D/E、深圳可用区A/B、上海可用区A/B、亚太1可用区A、美西可用区1B、香港可用区B")
    while True:
        selection=int(raw_input("Please Select the ZoneId:"))
        if not isinstance(selection,int):
            print("Wrong type...")
        else:
            zone_id=menu[selection]
            break
    return zone_id

def create_sg_default_policy(sg_id,accesskey_id,accesskey_secret,region_id):
    clt = client.AcsClient(accesskey_id, accesskey_secret, region_id)
    request = AuthorizeSecurityGroupRequest.AuthorizeSecurityGroupRequest()
    request.set_accept_format('json')
    request.set_SecurityGroupId(sg_id)
    request.set_IpProtocol("all")
    request.set_PortRange("-1/-1")
    request.set_SourceCidrIp("116.62.17.198")
    request.set_Policy("accept")
    request.set_Priority('10')
    result = clt.do_action_with_exception(request)
    print "prometheus server has been added into new created SafeGroup!"
    print result

    clt = client.AcsClient(accesskey_id, accesskey_secret, region_id)
    request = AuthorizeSecurityGroupRequest.AuthorizeSecurityGroupRequest()
    request.set_accept_format('json')
    request.set_SecurityGroupId(sg_id)
    request.set_IpProtocol("tcp")
    request.set_PortRange("22/22")
    request.set_SourceCidrIp("222.45.44.102")
    request.set_Policy("accept")
    request.set_Priority('10')
    result = clt.do_action_with_exception_with_exception(request)
    print "DiDa Office Unicom IP segement has been added into new created SafeGroup!"
    print result

    clt = client.AcsClient(accesskey_id, accesskey_secret, region_id)
    request = AuthorizeSecurityGroupRequest.AuthorizeSecurityGroupRequest()
    request.set_accept_format('json')
    request.set_SecurityGroupId(sg_id)
    request.set_IpProtocol("all")
    request.set_PortRange("-1/-1")
    request.set_SourceCidrIp("222.190.106.80/28")
    request.set_Policy("accept")
    request.set_Priority('10')
    result = clt.do_action_with_exception_with_exception(request)
    print "DiDa Office IP telcome segement has been added into new created SafeGroup!"
    print result

    return

##test scope





