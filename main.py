import requests
from flask import Flask
from flask import render_template
from flask import request


app = Flask(__name__)


def params(expiry_time, uid, openid, token, main, platform, createtime):
    data = f'''{{"expiry_time": {expiry_time},
    "uid": {uid},
    "open_id": "{openid}",
    "access_token": "{token}",
    "main_active_platform": {main},
    "platform": {platform},
    "create_time": {createtime},
    "scope": ["get_user_info", "get_friends", "payment"]}}'''
    return data
    
def getResponse(token):
    try:
        url = f"https://100067.connect.garena.com/oauth/token/inspect?token={token}"
        headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11; ASUS_Z01QD Build/PI)",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"}
        response = requests.get(url, headers=headers).json()
        if "open_id" in response:
            return  params(
            expiry_time=response["expiry_time"],
            uid=response["uid"],
            openid=response["open_id"],
            token=token,
            main=response["main_active_platform"],
            platform=response["platform"],
            createtime=response["create_time"])
        else:return "error from token or api !"
    except Exception as error:
        return "Error : ",str(error)

@app.route("/", methods=["GET"])
def dashboard():
    return render_template("index.html")
@app.route("/getdata", methods=["POST"])
def datauser():
     mytoken = request.form.get("token")
     data = getResponse(token=mytoken)
     return render_template("index.html", response=data)
     
     
if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)
