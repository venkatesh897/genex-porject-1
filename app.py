from flask import Flask, render_template, jsonify
import json
import requests

app = Flask(__name__) # name for the Flask app (refer to output)

@app.route("/api/getOnCallUsers",  methods=['GET'])
def home():
    mydata = []
    result = requests.get('https://api.victorops.com/api-public/v1/oncall/current',
                headers= {
                    'X-VO-Api-Id': 'cc08d1f3',
                    'X-VO-Api-Key' : '5fc72382aa0c573884f4608b3c1f6dfd',
                    'Content-Type': 'application/json'
                })
    # print(result.content)
    # print(result.json())
    data  = result.json()
    for i in data['teamsOnCall']:
        tmp = i['team']['name']
        tmp2 = i['oncallNow'][0]['users'][0]['onCalluser']['username']
        tmp3 = phone(tmp2)
        fin = {
            'teamName': tmp,
            'userName': tmp2,
            'phone': tmp3
        }
        mydata.append(fin)
    return jsonify(mydata); 

@app.route("/")
def homePage():
    return render_template('index.html')


@app.route("/fetch")
def fetch():
    mydata = []
    result = requests.get('https://api.victorops.com/api-public/v1/oncall/current',
                headers= {
                    'X-VO-Api-Id': 'cc08d1f3',
                    'X-VO-Api-Key' : '5fc72382aa0c573884f4608b3c1f6dfd',
                    'Content-Type': 'application/json'
                })
    # print(result.content)
    # print(result.json())
    data  = result.json()
    for i in data['teamsOnCall']:
        tmp = i['team']['name']
        tmp2 = i['oncallNow'][0]['users'][0]['onCalluser']['username']
        tmp3 = phone(tmp2)
        fin = {
            'teamName': tmp,
            'userName': tmp2,
            'phone': tmp3
        }
        mydata.append(fin)
        # print(tmp3)
        print(mydata)
    return render_template("index.html", data=mydata); 

def phone(username):
    ph = requests.get("https://api.victorops.com/api-public/v1/user/"+username+"/contact-methods",
                    headers= {
                    'X-VO-Api-Id': 'cc08d1f3',
                    'X-VO-Api-Key' : '5fc72382aa0c573884f4608b3c1f6dfd',
                    'Content-Type': 'application/json'
                })
    phData = ph.json()
    # print(phData)
    phoneNum = phData['phones']['contactMethods'][0]['value']
    return phoneNum



# https://api.victorops.com/api-public/v1/user/${each.username}/contact-methods

# running the server
app.run(debug = True) # to allow for debugging and auto-reload

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True)
