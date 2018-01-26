import time
import string

import random
import hashlib

from flask import Flask


def random_string():
    ISOTIMEFORMAT='%Y-%m-%d %X'
    TIMESTAMP = time.time()

    ALPHA1 = string.lowercase[0:26]
    ALPHA2 = string.uppercase[0:26]
    ALPHA3 = "!@#$%^&*()-=_+{}[];:',?"
    TIMESHA = hashlib.sha1(str(TIMESTAMP)).hexdigest()

    STR = ""
    SHA_STR1 = string.join(random.sample(TIMESHA,16)).replace(" ","")
    SHA_STR2 = string.join(random.sample(ALPHA1,16)).replace(" ","")
    SHA_STR3 =  string.join(random.sample(ALPHA2,16)).replace(" ","")
    SHA_STR4 =  string.join(random.sample(ALPHA3,16)).replace(" ","")

    LIST = [SHA_STR1,SHA_STR2,SHA_STR3,SHA_STR4]
    for j in range(1,5):
        index = random.randint(0,3)
        STR = STR+LIST[index]
    print("Now, we will generate 50 random strings:")
    result = ""
    for i in range(1,50):
        result = result + string.join(random.sample(STR,16)).replace(" ","") + '<br>'
    return result

app = Flask(__name__)
@app.route('/',methods=['GET'])
def show_result():
    return random_string();

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=30001)