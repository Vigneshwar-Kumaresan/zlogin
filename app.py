import requests
import hashlib
import json
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)

@app.route('/')
def index():
  return render_template("index.html")

@app.route('/result',methods = ['POST', 'GET'])
def result():
  url = "https://www.zebull.in/rest/MobullService/api/customer/getAPIEncpkey"
  userid = request.form["userid"]
  api = request.form["api"]
  payload = "{\r\n  \"userId\": \"" + userid + "\"\r\n}"
  headers = {
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  res = (response.text.encode('utf8'))

  b = json.loads(res)

  en = b['encKey']

  str = userid +api+ en

  res = hashlib.sha256(str.encode())
  hash =res.hexdigest()
  url = "https://www.zebull.in/rest/MobullService/api/customer/getUserSID"

  payload =  "{\n  \"userId\":\""+userid+"\",\n  \"userData\":\""+hash+"\"\n}"
  headers = {
    'Content-Type': 'application/json'
  }

  resi = requests.request("POST", url, headers=headers, data=payload)
  sess = resi.text.encode('utf8')

  b = json.loads(sess)

  result = b['sessionID']

  return render_template("result.html", result=result)

if __name__ == '__main__':
    app.run()