from flask import Flask,render_template,request,redirect,Response
import os
import pyrebase
from werkzeug.utils import redirect
import bs4 
import random

app=Flask(__name__)


config={
    "apiKey": "AIzaSyCJ4LWGHgI1VifxIWHAwJsC1f0chUCCRmk",

    "authDomain": "how-we-code-c0076.firebaseapp.com",

    "databaseURL": "https://how-we-code-c0076-default-rtdb.firebaseio.com",

    "projectId": "how-we-code-c0076",

    "storageBucket": "how-we-code-c0076.appspot.com",

    "messagingSenderId": "1088248751326",

    "appId": "1:1088248751326:web:a54f183798e67090560e4f",

    "measurementId": "G-G75N9WF159"

}

firebase=pyrebase.initialize_app(config)
database=firebase.database()

def get_date(date):

    splitter=date.split("-")
    months=['','Jan','Feb','Mar','Apr','May','June','Jul','Aug','Sept','Oct','Nov','Dec']

    final=f"{splitter[2]}, {months[int(splitter[1])]}, {splitter[0]}"
    return final



@app.route('/')
def home():
    l=database.child("posts").get().val()
    posts=[]
    for i in l:
        posts.append(i)
    random.shuffle(posts)
    #date=get_date(database.child("posts").child(i).get().val()['date_posted'])
    return render_template('index.html',db2=database,bs=bs4,posts=posts,date=get_date)

@app.route('/subscribe',methods=['POST','GET'])
def subscribe():
    if request.form['button']=='Subscribe':
        email=request.form['sub-email']
        url=request.form['url']
        try:    
            save={'email':email}
            get_count=database.child("sub_count").get().val()
            database.child('subscribers').child(f'reader{get_count}').set(save)
            database.child("sub_count").set(get_count+1)
            return redirect(f"{url}?result=success")
        except:
            return redirect(f"{url}?result=failed")
    else:
        return "Failed!"
@app.route('/sitemap.xml')
def sitemap():
    l=database.child("posts").get().val()
    posts=[]
    for i in l:
        posts.append(i)
    xml=render_template('sitemap.xml',post=posts,db2=database)
    return Response(xml, mimetype='application/xml')
#text/plain
@app.route('/robots.txt')
def static_from_root():
    txt=render_template('robots.txt')
    return Response(txt,mimetype='text/plain')

@app.route('/article/<id>/<title>')
def article(id,title):
    count=f'number{id}'
    l=database.child("posts").get().val()
    posts=[]
    for i in l:
        posts.append(i)
    posts.remove(count)
    random.shuffle(posts)
    get_tit=database.child("posts").child(count).get().val()['title']
    desc=bs4.BeautifulSoup(database.child("posts").child(count).get().val()['content'],features="lxml").get_text()[0:145]
    if title.replace("-"," ")==get_tit:
        url=database.child("posts").child(count).get().val()['banner']
        tag=database.child("posts").child(count).get().val()['tags']
        return render_template('show_article.html',count=count,db=database,url=url,titles=get_tit,tag=tag,desc=desc,post=posts[0:4])
    else:
        return "<h1>Content not found</h1>",404
   
if __name__=="__main__":
    app.run(debug=True)

