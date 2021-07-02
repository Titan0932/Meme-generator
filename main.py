from flask import Flask,render_template,url_for,request,redirect
import json,random
import requests



CLIENT_ID = "OXvNI_nPlU1P7A"
CLIENT_SECRET = "HSM-CE06KHiwwbAfmlAfGDH8OqgyJw"
REDIRECT_URI = "http://localhost"



app=Flask(__name__)

app.config['SECRET_KEY']="5C201B"

with open('password.txt','r') as f:
    passw=''
    e_passw=f.read().split()
   
    for i in e_passw:
        passw+=chr(int(i))

    


auth = requests.auth.HTTPBasicAuth(CLIENT_ID,CLIENT_SECRET) 

data={

    'grant_type':'password',
    'username':'Titan0932',
    'password':passw
}

headers={'User-Agent':'MyAPI/0.0.1',
        'Authorization':'bearer 439051664176-6TTLkQ0CekMdqwej7NdLlQgXwcEyNA'
        }

res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)
TOKEN = res.json()['access_token']


headers['Authorization']=f'bearer {TOKEN}'


sub_reddits=['AdviceAnimals','MemeEconomy','ComedyCemetery','memes','dankmemes','PrequelMemes','terriblefacebookmemes']


sub_r=random.randint(0,6)

res=requests.get(f'https://oauth.reddit.com/r/{sub_reddits[sub_r]}/hot', headers=headers)
api_data=res.json()

'''
with open('static/data/dankmemes-api.json','w') as f:
    json.dump(res.json(),f,indent=4)
'''



messages=['lol!!!', 'lmao!!!', "hahaha!","rofl!!!","OMG!lol","ohhhh!","Dayum Son!"]
counter=0

def find_meme():
    global memes,message,counter

    
    u_post=api_data['data']['children']
    position=random.randint(1,len(u_post)-1)
    

    memes={'User': u_post[position]['data']['name'],
            'title': u_post[position]['data']['title'],
            'UpVotes': u_post[position]['data']['ups'],
            'DownVotes': u_post[position]['data']['downs'],
            'image':u_post[position]['data']['url_overridden_by_dest']
            }

    message=messages[random.randint(0,6)]
    if counter==1: 
        counter=0
    else:
        counter+=1   #this is used to change the layout colour each time the button is pressed


@app.route('/',methods=["POST","GET"])
def main():
    global memes,counter
    
    find_meme()
    if request.method=='POST':
        return redirect(url_for('main'))
    return render_template("home.html",memes=memes, message=message,counter=counter)
    


if __name__ == '__main__':
	app.run(debug=True)
  