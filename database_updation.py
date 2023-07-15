import datacollection
import pandas as pd
from sqlalchemy import create_engine


#url='https://www.youtube.com/@krishnaik06/videos'
#url='https://www.youtube.com/@HiteshChoudharydotcom/videos'
#url='https://www.youtube.com/@Telusko/videos'
#url='https://www.youtube.com/@saurabhexponent1/videos'

count=50

engine = create_engine("mysql+mysqlconnector://user:password@localhost", echo=True)
with engine.connect() as connection:
    connection.execute("CREATE DATABASE IF NOT EXISTS youtubers")
    connection.execute("USE youtubers")

data_find=datacollection.fetch_data(url,count)
channel=datacollection.data['Creater_name'][0].lower().replace(" ","")

df=pd.DataFrame.from_dict(data_find)
df.to_sql( name=channel, con=engine, if_exists='replace', index = False)

#df.to_csv(channel+".csv",index=False)




