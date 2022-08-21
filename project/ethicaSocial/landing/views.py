from email import message
from django.shortcuts import redirect, render
from django.http import HttpResponse
from pymongo import MongoClient
import requests
import json
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




# backend of every page at landing
 
def logIn(request):
	# if already logged in, send to homepage
	try:
		request.session['nid']
		return redirect("/home")
	except:
		return render(request, 'html/login.html',{"msg":None})


def createAccoutn(request):
	
	try:
		request.session['nid']
		return redirect("/home")
	except:
		message={}
		message={'msg' : None}
		return render(request, 'html/createAccount.html',message)
def validateLogin(request):
	#came in the right way
	if(request.method=='POST'):
		db=DBConnect.getInstance()
		collection=db["user"]
		email=request.POST["email"]
		password=request.POST["password"]

		#invalid try
		if(collection.count_documents({"email":email, "password":password})!=1):
			message={"msg": "invalid email or password"}
			return render(request, 'html/login.html',message)
		
		# valid user
		data=collection.find_one({"email":email, "password":password})
		nid=data["nid"]
		
		#save session
		request.session['nid']=nid

		return redirect("/home")

	#came from somewere else
	return render(request, 'html/createAccount.html',message)

def createAccountDb(request):
	if(request.method=='POST'):
		# database connection
		db=DBConnect.getInstance()
		collection=db["user"]

		# validating evrything
		hasError=False
		msg  =None

		# name validation 
		name=request.POST['name']
		if(len(name)<2):
			hasError=True
			msg="invalid name. must be atleast 2 character long"

		
		#nid validation
		nid=request.POST['nid']
		if(len(nid)<5 or not (nid.isdigit()) ) :
			hasError = True
			msg="invalid nid. must be a digit and 5 character long"
		
		# nid already taken
		elif(collection.count_documents({"nid":nid}) !=0):
			hasError=True
			msg="nid already in use"
		


		# password validation

		password=request.POST['password']
		if(len(password)<6):
			hasError=True
			msg="password too short"


		email=request.POST['email']

		# email validation 
		if(collection.count_documents({"email":email}) !=0):
			hasError=True
			msg="email alrady in use"
		

		# has some error 
		if(hasError):
			message={"msg": msg}
			return render(request, 'html/createAccount.html',message)
		
		#generating random data
		response_API = requests.get('https://randomuser.me/api/')
		
		data = response_API.text
		parse_json = json.loads(data)
		data = parse_json['results'][0]

		userInfo={
			"name":name,
			"nid":nid,
			"email":email,
			"password":password,
			"gender":data['gender'],
			"location":data['location'],
			"dob":data['dob'],
			"phone_number":data['phone'],
			"balance":0,
			"bloodGroup":None,
			"sellData":True,
			"maxUseLimit":1e9,
			"maxPostView":1e9,
			"todayUse":0,
			"todayPostView":0,
			"followers":[],
			"followings":[],
			"activityLog":[],
			"dp":"nodp.jpg",

		}
		request.session['nid']=nid
		#save data to cloud
		collection.insert_one(userInfo)
		
		return redirect("/home");

		

	#came from somewere else	
	return render(request, 'html/createAccount.html',message)

