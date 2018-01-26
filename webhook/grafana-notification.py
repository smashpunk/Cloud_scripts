from flask import Flask
from flask import request
import requests
import json
import os

app = Flask(__name__)

@app.route('/sms',methods=['GET'])
def sms_get():
    msg = request.args.get('msg')
    url = u'http://sdk.entinfo.cn:8061/webservice.asmx/mdsmssend?sn=SDK-WSS-010-10316&pwd=4598009CDB01DE04E43B84A65BBE9568&mobile=15150676721,15380779698,15951967563&content=%s\u3010\u5600\u54d2\u7269\u6d41\u3011&ext=&stime=&rrid=&msgfmt=' % msg
    requests.get(url)
    return 'OK'

@app.route('/sms',methods=['POST'])
def sms():
    data=json.loads(request.data)
    print data
    message = data['title']
    url = u'http://sdk.entinfo.cn:8061/webservice.asmx/mdsmssend?sn=SDK-WSS-010-10316&pwd=4598009CDB01DE04E43B84A65BBE9568&mobile=15150676721,15380779698,15951967563&content=%s\u3010\u5600\u54d2\u7269\u6d41\u3011&ext=&stime=&rrid=&msgfmt=' % message
    print url
    return requests.get(url).text

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=30000)