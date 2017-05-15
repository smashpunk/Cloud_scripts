import re
import requests
import os
from Infra_function import *

class Getmyip:
    def getip(self):
        try:
            myip = self.visit("http://www.ip138.com/ip2city.asp")
        except:
            try:
                myip = self.visit("http://whatismyipaddress.com/")
            except:
                try:
                    myip=self.visit("http://v4.ipv6-test.com/api/myip.php")
                except:
                    myip = "Pub IP not found!!!"
        return myip

    def visit(self,url):
        str=requests.get(url).text
        return re.search('\d+\.\d+\.\d+\.\d+',str).group(0)
    def ip_record(self,pub_ip):
        myfile = open('/opt/WORK/Cloud_scripts/pub_ip', 'w+')
        myfile.write(pub_ip)
        myfile.write("\n")
        myfile.close()
        return



getmyip = Getmyip()
pub_ip = getmyip.getip()
print pub_ip
#getmyip.ip_record(pub_ip)

# get origin pub IP
fr=open("/opt/WORK/Cloud_scripts/pub_ip",'r')
content=fr.readlines()
origin_ip = content[0]
print origin_ip
fr.close()

# get aliyun access information
FILE_PATH="/opt/WORK/Cloud_scripts/Aliyun/"
fr=open(FILE_PATH+'Access_Information','r')
content=fr.readlines()
## -1 mean remove "\n" from the element
accesskey_id=content[1][12:-1]
accesskey_secret=content[2][16:-1]
region_id_default=content[3][14:-1]
fr.close()

# set region to cn-hangzhou

if pub_ip != origin_ip:
    clt = client.AcsClient(accesskey_id, accesskey_secret, region_id_default)
    request=DescribeSecurityGroupsRequest.DescribeSecurityGroupsRequest()
    request.set_accept_format('json')
    result = clt.do_action(request)
    js_str=json.loads(result)
    for i in js_str["SecurityGroups"]["SecurityGroup"]:
        #print i["SecurityGroupId"],"\t",i["SecurityGroupName"],"\t",i["Description"],"\t",i["CreationTime"]
        sg_id=i["SecurityGroupId"]
        clt_policy = client.AcsClient(accesskey_id, accesskey_secret, region_id_default)
        request_policy = DescribeSecurityGroupAttributeRequest.DescribeSecurityGroupAttributeRequest()
        request_policy.set_accept_format('json')
        request_policy.set_SecurityGroupId(sg_id)
        result_policy = clt_policy.do_action(request_policy)
        js_str_policy = json.loads(result_policy)
        for i in js_str_policy["Permissions"]["Permission"]:
            if i["SourceCidrIp"]==origin_ip:
                print i["SourceCidrIp"], "\t", i["DestCidrIp"], "\t", i["Direction"], "\t", i["PortRange"], "\t", i["IpProtocol"], "\t", i["Policy"]
                print sg_id
                clt_remove = client.AcsClient(accesskey_id, accesskey_secret, region_id_default)
                request_remove = RevokeSecurityGroupRequest.RevokeSecurityGroupRequest()
                request_remove.set_accept_format('json')
                request_remove.set_SecurityGroupId(sg_id)
                request_remove.set_IpProtocol(i["IpProtocol"])
                request_remove.set_PortRange(i["PortRange"])
                request_remove.set_SourceCidrIp(i["SourceCidrIp"])
                result_remove = clt.do_action(request_remove)
                print result
                clt_add = client.AcsClient(accesskey_id, accesskey_secret, region_id)
                request_add = AuthorizeSecurityGroupRequest.AuthorizeSecurityGroupRequest()
                request_add.set_SecurityGroupId(sg_id)
                request_add.set_IpProtocol(i["IpProtocol"])
                request_add.set_PortRange(i["PortRange"])
                request_add.set_SourceCidrIp(i["SourceCidrIp"])
                request_add.set_Policy("accept")
                request_add.set_accept_format('json')
                request_add.set_Priority('10')
                result_add = clt.do_action(request)
                print result_add



##test scope

