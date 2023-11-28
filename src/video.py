from googleapiclient.discovery import build
import os
import json


class Video:
    def __init__(self, video_id):
        self.api_key: str = os.getenv('YT_API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        self.video_id = video_id
        self.video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                         id=self.video_id
                                                         ).execute()
        self.video_title = self.video_response['items'][0]['snippet']['title']
        self.video_url = 'www.youtube.com/watch?=' + self.video_id
        self.views = self.video_response['items'][0]['statistics']['viewCount']
        self.likes = self.video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.video_title


class PLVideo(Video):
    def __init__(self, video_id, video_playlist_id):
        super().__init__(video_id)
        self.video_playlist_id = video_playlist_id
        print(json.dumps(self.video_response, indent=4))

    def __str__(self):
        return self.video_title
