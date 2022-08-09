from pymongo import MongoClient
import gridfs
cluster = MongoClient("mongodb+srv://root:1234@cluster1.8jmyghr.mongodb.net/?retryWrites=true&w=majority")
db = cluster["test"]
fs=gridfs.GridFS(db)
name="photomy.jpg"
data=db.fs.files.find_one({"filename":name})
print(data)
id_=data['_id']
outputdata=fs.get(id_).read()
output=open("downloadPhoto.jpg","wb")
output.write(outputdata)
output.close()

