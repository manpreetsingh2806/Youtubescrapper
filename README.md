# **Youtube Scrapper project**

## Using this project:

*HomePage*

1. **Youtube channel URL** : you will be required to enter url in following format https://www.youtube.com/@channelname/videos  , for example: https://www.youtube.com/@PrimeVideoIN/videos

2. **Number of videos to scrape**: Max limit is set to be equal to or less than 50 videos. However YouTube Data API have a default quota allocation of 10,000 units per day, over which we have cost for every activity you perform


*Video Section*

It shows the following information for the channel input:

1. Creator Name
2. Title
3. Thumbnail Url
4. Video ID
5. Video Url
6. Likes
7. Number of comments
8. Link to see video comments
9. Link to download video

*Comments Section*

It shows the top level comments and respective replies if any on that comment


**Inueron chanllenge**
As part of Inueron chanllenge, data is fetched for 4 channels
1. Krish Naik
2. Hitesh Choudhary
3. mysirg.com
4. Telusko

For them I retrieved data and stored in MySql and MongoDB, but the application can be used to fetch data from any channel
