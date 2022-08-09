from pymongo import MongoClient
import gridfs
cluster = MongoClient("mongodb+srv://root:1234@cluster1.8jmyghr.mongodb.net/?retryWrites=true&w=majority")
db = cluster["test"]
photo= "input.jpg"
filedata=open(photo,"rb")
data=filedata.read()
fs=gridfs.GridFS(db)
fs.put(data,filename=photo)
