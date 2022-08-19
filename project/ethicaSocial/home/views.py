import profile
from django.shortcuts import render
from email import message
from django.shortcuts import render,redirect
from django.http import HttpResponse
from pymongo import MongoClient
import requests
import gridfs
class DBConnect:
   __instance = None
   @staticmethod 
   def getInstance():
      if DBConnect.__instance == None:
        DBConnect()
      return DBConnect.__instance
   def __init__(self):
      if DBConnect.__instance != None:
        raise Exception("This class is a singleton!")
      else:
        cluster = MongoClient("mongodb+srv://root:1234@cluster1.8jmyghr.mongodb.net/?retryWrites=true&w=majority")
        db = cluster["ethica"]

        DBConnect.__instance = db


class igmDBConnect:
   __instance = None
   @staticmethod 
   def getInstance():
      if igmDBConnect.__instance == None:
        igmDBConnect()
      return igmDBConnect.__instance
   def __init__(self):
      if igmDBConnect.__instance != None:
        raise Exception("This class is a singleton!")
      else:
        cluster = MongoClient("mongodb+srv://root:1234@cluster1.8jmyghr.mongodb.net/?retryWrites=true&w=majority")
        db = cluster["ethicaPhotos"]

        igmDBConnect.__instance = db

def uploadPhoto(photo):
    cluster = MongoClient("mongodb+srv://root:1234@cluster1.8jmyghr.mongodb.net/?retryWrites=true&w=majority")
    db = cluster["ethicaPhotos"]
    fs=gridfs.GridFS(db)
    fs.put(photo,filename="1.jpg")

def getImg(nid):
    #db connection 
    db=DBConnect.getInstance()
    collection=db["user"]

    data=collection.find_one({"nid":nid})
    imgName=data['dp']

    # image db collection
    db=igmDBConnect.getInstance()
    fs=gridfs.GridFS(db)
    data=db.fs.files.find_one({"filename":imgName})
    id_=data['_id']
    outputdata=fs.get(id_).read()
    output=open(imgName,"wb")
    output.write(outputdata)
    output.close()

    return imgName

    

def newsFeed(request):
    nid=request.session['nid']
    return render(request, 'html/newsFeed.html')

def profilePage(request):
    nid=request.session['nid']
    db=DBConnect.getInstance()
    collection=db["user"]
    usr=collection.find_one({"nid":nid})
    dp=getImg(nid)
    userInfo={
        "dp":dp,
        "name":usr["name"],
    }
    
    collection=db["post"]
    posts=collection.find({"nid":nid})
    allPosts=[]
    for i in posts:
        postShow={
            "content": i['content'],
            "likes":len(i["reaction"]["like"]),
            "comment":i["comment"],
            "viewers":i["audience"],
        }
        allPosts.append(postShow)
        
    
    userInfo["posts"]=allPosts
    

    return render(request, 'html/profile.html',userInfo)

def createPost(request):
    return render(request, 'html/createPost.html')

def createPostHandle(request):
    #came from unknown source
    if(request.method!='POST'):
        return redirect("createPost")


    photo=None
    try:
        photo=request.POST['img']
    except:
        pass
    
    react=None
    try:
        react=request.POST['hideReaction']
    except:
        pass
    price=0
    try:
        price=int(request.POST['price'])
        if(price<0):
            price=0
    except:
        pass
    
    
    
    postContent=request.POST['postcontent']
    
    #empty post
    if(len(postContent)==0):
        return render(request, 'html/createPost.html',{"msg":"post cannot be empty"})
    

    

    
    tags=request.POST['tags'].split(" ")
    audience=request.POST["audience"]
    
    post={
        "nid":request.session['nid'],
        "content":postContent,
        "photo":None,
        "reaction":{
            "like":[],
        },
        "comment":[],
        "audience":audience,
        "type":"regular",
        "price":price,
        "tags":tags,
    }
    db=DBConnect.getInstance()
    collection=db["post"]
    collection.insert_one(post)
      

    return redirect(profilePage)

def followers(request):
    return HttpResponse("this is create followers")
def followings(request):
    return HttpResponse("this is create followings")
def othersProfile(request):
    return render(request, 'html/othersProfile.html')
# def followUser(request):



def message(request):
    return HttpResponse("this is message")
def notification(request):
    return HttpResponse("this is notification")
def settings(request):
    return HttpResponse("this is settings")
def bloodDonatin(request):
    return HttpResponse("this is blood donation")

def shop(request):
    return HttpResponse("this is shop")
def jobs(request):
    return HttpResponse("this is jobs")
def news(request):
    return HttpResponse("this is news")
def followersPost(request):
    return HttpResponse("this is follwoersPost")




