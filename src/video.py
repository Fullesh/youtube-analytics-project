from googleapiclient.discovery import build
import os
import json

api_key: str = os.getenv('YT_API_KEY')
youtube = build('youtube', 'v3', developerKey=api_key)
class Video:
    def __init__(self, video_id):
        self.video_id = video_id
        self.video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=self.video_id
                                               ).execute()
        self.video_title = self.video_response['items'][0]['snippet']['title']
        self.video_url = 'www.youtube.com/watch?='+self.video_id
        self.views = self.video_response['items'][0]['statistics']['viewCount']
        self.likes = self.video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.video_title
