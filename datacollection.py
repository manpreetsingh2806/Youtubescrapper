from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import requests
import base64
import config

from googleapiclient.discovery import build
youtube_build = build('youtube', 'v3', developerKey=config.api_key)


def fetch_channel_id(url):
    """
    :param url: youtube channel url, example: 'https://www.youtube.com/@krishnaik06/videos'
    :return: channel id of respective youtube channel url
    """
    try:
        uClient = uReq(url)

    except Exception as e:
        print("cannot open url", e)

    channelPage = uClient.read()
    uClient.close()
    channel_html = bs(channelPage, "html.parser")
    channel_id = channel_html.find('link', rel="canonical")['href'].split('/')[-1]
    return channel_id

def fetch_uploadplaylist_id(channel_id):
    """
    :param channel_id:
    :return: upload playlist id in which all videos are there
    """
    request = youtube_build.channels().list(part="contentDetails",id=channel_id).execute()
    upload_playlist_id=request['items'][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    return upload_playlist_id

def videos_uploaded(channel_id):
    """
    :param channel_id:
    :return: count of videos uploaded in youtube channel
    """
    request = youtube_build.channels().list(part="statistics",id=channel_id).execute()
    videos_count=request['items'][0]["statistics"]["videoCount"]
    return videos_count

#dictionary to store all related information to a channel
data = {'Creater_name': [], 'title': [], 'thumbnail_url': [], 'videoid': [], 'video_url': [], 'like': [],
        'comment_count': []}


def fetch_data(url: str, count: int):
    """
    :param url: url of youtube channel
    :param count: no of videos you want to fetch
    :return: dictionary with youtube channel information of videos
    """
    channel_id = fetch_channel_id(url)
    upload_playlistid = fetch_uploadplaylist_id(channel_id)
    videos = videos_uploaded(channel_id)

    try:
        request1 = youtube_build.playlistItems().list(part="snippet,contentDetails", playlistId=upload_playlistid,
                                                      maxResults=count).execute()

    except Exception as e:
        print("unable to fetch playlist items", e)

    for i in request1['items']:
        data['Creater_name'].append(i["snippet"]["videoOwnerChannelTitle"])
        data['title'].append(i["snippet"]["title"])
        data['thumbnail_url'].append(i["snippet"]["thumbnails"]["default"]["url"])
        data['videoid'].append(i["snippet"]["resourceId"]["videoId"])

    for i, videoid in enumerate(data['videoid']):
        try:
            request2 = youtube_build.videos().list(part="statistics", id=videoid).execute()

        except Exception as e:
            print("unable to fetch video details", e)

        data['video_url'].append("https://www.youtube.com/watch?v=" + data['videoid'][i])
        data['like'].append(request2['items'][0]["statistics"]["likeCount"])
        data['comment_count'].append(request2['items'][0]["statistics"]["commentCount"])

    return data

def conversiontobase64(i):
    """
    :param i: thumbnail url
    :return: base 64 thumbnail url
    """
    thumbnail_fetched = requests.get(i).content
    return (base64.b64encode(thumbnail_fetched).decode("utf-8"))

def get_full_replies(id):
    """
    :param id: comment id
    :return: replies on that particular comment
    """
    replies_comment = []
    request4 = youtube_build.comments().list(part="snippet", parentId=id).execute()
    while request4:
        for r in request4['items']:
            replies_comment.append({'reply': r["snippet"]["textOriginal"],
                                    'replier_name': r["snippet"]["authorDisplayName"]})

        if ("nextPageToken" in request4):
            request4 = youtube_build.comments().list(part="snippet", parentId=id,
                                                     pageToken=request4['nextPageToken']).execute()
        else:
            break

    return (replies_comment)


video_comments = []


def fetch_comments():
    """
    :return: list,comments with a dictionary video wise
    """
    for i, videoid in enumerate(data['videoid']):
        data_comments = {'videoid': None, 'comments': [], 'thumbnail_64': None}
        request3 = youtube_build.commentThreads().list(part="snippet,replies", videoId=videoid).execute()
        data_comments['videoid'] = videoid
        data_comments['thumbnail_64'] = conversiontobase64(data['thumbnail_url'][i])
        while request3:
            for j in request3['items']:

                replycount = j['snippet']['totalReplyCount']

                if replycount > 0:
                    id = j['id']
                    replies = get_full_replies(id)
                    data_comments['comments'].append(
                        {'comment': (j["snippet"]["topLevelComment"]["snippet"]["textOriginal"]),
                         'commentor_name': (j["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]),
                         'reply_data': (replies)})

                else:
                    data_comments['comments'].append(
                        {'comment': (j["snippet"]["topLevelComment"]["snippet"]["textOriginal"]),
                         'commentor_name': (j["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"])})

            if ("nextPageToken" in request3):
                request3 = youtube_build.commentThreads().list(part="snippet,replies", videoId=videoid,
                                                               pageToken=request3['nextPageToken']).execute()

            else:
                break

        video_comments.append(data_comments)

    return (video_comments)

def fetch_singlevideo_comments(videoid):
    """
    :param videoid: Id of a particular video
    :return: dict, comments from a particular video
    """

    data_comments = {'videoid': None, 'comments': [], 'thumbnail_64': None}
    request3 = youtube_build.commentThreads().list(part="snippet,replies", videoId=videoid).execute()
    data_comments['videoid'] = videoid

    for i, video_id in enumerate(data['videoid']):
        if (videoid == video_id):
            pos = i

    data_comments['thumbnail_64']=conversiontobase64(data['thumbnail_url'][pos])
    while request3:
        for i in request3['items']:

            replycount = i['snippet']['totalReplyCount']

            if replycount > 0:
                id = i['id']
                replies = get_full_replies(id)
                data_comments['comments'].append(
                    {'comment': (i["snippet"]["topLevelComment"]["snippet"]["textOriginal"]),
                     'commentor_name': (i["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]),
                     'reply_data': (replies)})

            else:
                data_comments['comments'].append(
                    {'comment': (i["snippet"]["topLevelComment"]["snippet"]["textOriginal"]),
                     'commentor_name': (i["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"])})

        if ("nextPageToken" in request3):
            request3 = youtube_build.commentThreads().list(part="snippet,replies", videoId=videoid,
                                                               pageToken=request3['nextPageToken']).execute()

        else:
            break

    return (data_comments)

