from pymongo import MongoClient
cluster = MongoClient("mongodb+srv://root:1234@cluster1.8jmyghr.mongodb.net/?retryWrites=true&w=majority")
db = cluster["test"]
collection=db["sttry"]
post={
    "roll":2,
    "name" : "abcd"
}
all=collection.find()
for i in all:
    print(i)
