import datacollection
import pymongo

client = pymongo.MongoClient("client connection string")
db = client.test
print(db)



#url='https://www.youtube.com/@krishnaik06/videos'
#url='https://www.youtube.com/@HiteshChoudharydotcom/videos'
#url='https://www.youtube.com/@Telusko/videos'
#url='https://www.youtube.com/@saurabhexponent1/videos'

#count=50

datacollection.fetch_data(url,count)

d=datacollection.fetch_comments()

db=client['youtubers_comments']
collection = db['mysirg_video_comments']
collection.insert_many(d)