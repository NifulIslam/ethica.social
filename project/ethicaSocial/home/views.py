import profile
import datetime
from tokenize import Comment
from django.shortcuts import render
from email import message
from django.shortcuts import render,redirect,HttpResponseRedirect
from django.http import HttpResponse
from pymongo import MongoClient
import requests
import gridfs
from sympy import content
from bson.objectid import ObjectId
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

def getAllComment(post):
    allComment=[]
    db=DBConnect.getInstance()
    collection=db["user"]
    for i in post['comment']:
        commenterNid=i[0]
        commenter=collection.find_one({"nid":commenterNid})
        commenterName=commenter['name']
        allComment.append([commenterName,i[1]])
    return allComment

def newsFeed(request):
    nid=request.session['nid']
    return render(request, 'html/newsFeed.html')

def settings(request):
    return render(request, 'html/settings.html')

def logout(request):
    del request.session['nid']
    return redirect("/login")

def addComment(request):
    content=request.POST["comment"]
    postid=request.POST["postid"]
    if(len(content)==0):
        return redirect("profile")
    
    
    db=DBConnect.getInstance()
    collection=db["post"]
    postData=collection.find_one({"_id":ObjectId(postid)})
    allComments=postData["comment"]
    allComments.append([request.session['nid'], content])
    postData["comment"]=allComments
    collection.delete_one({"_id":ObjectId(postid)})
    collection.insert_one(postData)
    return redirect(request.META.get('HTTP_REFERER'))
    


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
        comments=getAllComment(i)
        postShow={
            "postNo":i["_id"],
            "content": i['content'],
            "likes":len(i["reaction"]["like"]),
            "comment":comments,
            "viewers":i["audience"],
            "type":i["type"],
            "date":i['date'],
        }
        
        allPosts.append(postShow)
        
    
    userInfo["posts"]=allPosts
    

    return render(request, 'html/profile.html',userInfo)

def createPost(request):
    return render(request, 'html/createPost.html')

def makeOtherComment(request):
    ownerOfPost=request.GET['nid']
    commenter=request.GET['commenter']
    postid=request.GET['postid']
    comment=request.GET['comment']
    if(len(comment)==0):
        redirect(request.META.get('HTTP_REFERER'))
    
    db=DBConnect.getInstance()
    collection=db["post"]
    postData=collection.find_one({"_id":ObjectId(postid)})
    allComments=postData["comment"]
    allComments.append([commenter,comment])
    postData["comment"]=allComments
    collection.delete_one({"_id":ObjectId(postid)})
    collection.insert_one(postData)
    

    return redirect(request.META.get('HTTP_REFERER'))

def changeBasicInfo(request):
    nid=request.session['nid']
    db=DBConnect.getInstance()
    collection=db["user"]
    usr=collection.find_one({"nid":nid})
    newName=request.GET['name']
    if(len(newName)>=6):
        usr['name']=newName
    
    newCity=request.GET['city']
    if(len(newCity)>4):
        usr['location']['city']=newCity

    newCountry=request.GET['country']
    if(len(newCountry)>4):
        usr['location']['country']=newCountry
    
    usr['email']=request.GET['email']
    usr['bloodGroup'] = request.GET['bloodGroup']
    collection.delete_one({"nid":nid})
    collection.insert_one(usr)
    
    return redirect("profile")
    


def showBasicInfo(request):
    nid=request.session['nid']
    db=DBConnect.getInstance()
    collection=db["user"]
    usr=collection.find_one({"nid":nid})
    usrData={
    "balance":usr['balance'],
    "name":usr['name'],
    "gender":usr['gender'],
    "age":usr["dob"]['age'],
    "city":usr['location']['city'],
    "country":usr['location']['country'],
    "email":usr['email'],
    "bloodGroup":usr['bloodGroup'],
    }

    return render(request, 'html/showBasicInfo.html',usrData)

def recharge(request):
    nid=request.session['nid']
    
    db=DBConnect.getInstance()
    collection=db["user"]
    usr=collection.find_one({"nid":nid})
    
    amount=request.GET['rechargeAmount']
    usr['balance']+=int(amount)
    
    collection.delete_one({"nid":nid})
    collection.insert_one(usr)
    return redirect(request.META.get('HTTP_REFERER'))

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
        "date":datetime.datetime.now(),
    }
    db=DBConnect.getInstance()
    collection=db["post"]
    collection.insert_one(post)
      

    return redirect(profilePage)


def followAction(request):
    isFollowing=request.GET['isFollowing']=="True"
    ownernid=request.GET['nid']
    viewernid=request.GET['viewerNid']

    db=DBConnect.getInstance()
    collection=db["user"]
    usr=collection.find_one({"nid":viewernid})
    usr2=collection.find_one({"nid":ownernid})
    

    
    if(isFollowing):
        usr['followings'].remove(ownernid)
        usr2['followers'].remove(viewernid)
    else:
        usr["followings"].append(ownernid)
        usr2['followers'].append(viewernid)
    
    collection.delete_one({"nid":viewernid})
    collection.insert_one(usr)

    collection.delete_one({"nid":ownernid})
    collection.insert_one(usr2)
    page=request.META.get('HTTP_REFERER')
    url="othersProfile/?nid="+ownernid
    
    return redirect(request.META.get('HTTP_REFERER'))

    

        


def followers(request):
    nid=request.session['nid']
    db=DBConnect.getInstance()
    collection=db["user"]
    usr=collection.find_one({"nid":nid})

    followerShow=[]
    for i in usr['followers']:
        follower=collection.find_one({"nid":i})
        followerShow.append(
            {
            "nid":i,
            "name":follower['name'],
            "city":follower['location']['city'],
            "country":follower['location']['country']
            }
            )

    followersInfo={
        "allFollowers":followerShow,
    }
    return render(request, 'html/followers.html',followersInfo)

def followings(request):
    return HttpResponse("this is create followings")
def othersProfile(request):
    nid=request.GET["nid"]
    mynid=request.session['nid']
    if(mynid==nid):
        return redirect("profile")

    # USER
    db=DBConnect.getInstance()
    collection=db["user"]
    usr=collection.find_one({"nid":nid})
    me=collection.find_one({"nid":mynid})
    #posts
    collection=db["post"]
    posts=collection.find({"nid":nid})

    allPosts=[]
    for i in posts:
        if(i["audience"]=="onlyme"):
            continue
        comments=getAllComment(i)
        postShow={
            "postNo":i["_id"],
            "content": i['content'],
            "likes":len(i["reaction"]["like"]),
            "comment":comments,
            "viewers":i["audience"],
            "type":i["type"],
            "date":i['date'],
        }
        
        allPosts.append(postShow)
    
    isFollowing=nid in me['followings']
    followBtn="follow"
    if(isFollowing):
        followBtn="unfollow"
    
    userInfo={
        "name":usr["name"],
        "nid":nid,
        "seeingNid":mynid,
        "gender": usr["gender"],
        "isFollowing":isFollowing,
        "posts": allPosts,
        "age":usr['dob']['age'],
        "city":usr['location']['city'],
        "country":usr['location']['country'],
        "followBtn":followBtn,
        "isFollowing":isFollowing,
    }
    
    

    return render(request, 'html/othersProfile.html',userInfo)


def message(request):
    return HttpResponse("this is message")

def notification(request):
    return HttpResponse("this is notification")
def bloodDonatin(request):
    return HttpResponse("this is blood donation")

def shop(request):
    return HttpResponse("this is shop")
def jobs(request):
    return HttpResponse("this is jobs")
def news(request):
    return HttpResponse("this is news")
def followersPost(request):
    nid=request.session['nid']
    db=DBConnect.getInstance()
    collection=db["user"]
    usr=collection.find_one({"nid":nid})
    collection=db["post"]
    allPost=collection.find()
    allPosts=[]
    collection=db["user"]
    for i in allPost:
        if((i["nid"]in usr['followings'] )and (i["audience"]!="onlyme")):
            comments=getAllComment(i)
            posterNid=i["nid"]
            usr=collection.find_one({"nid":posterNid})
            postShow={
                "posterName":usr['name'],
                "posterNid":i["nid"],
                "postNo":i["_id"],
                "content": i['content'],
                "likes":len(i["reaction"]["like"]),
                "comment":comments,
                "viewers":i["audience"],
                "type":i["type"],
                "date":i['date'],
                
                
                }
            allPosts.append(postShow)


    postShowAll={
        "nid":i['nid'],
        "seeingNid":nid,
        "posts": allPosts,
        
    }
    return render(request,"html/followersPost.html",postShowAll)




