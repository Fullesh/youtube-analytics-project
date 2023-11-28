from datetime import timedelta
from googleapiclient.discovery import build
import os
import isodate


class PlayList:

    def __init__(self, playlist_id):
        self.duration = []
        self.api_key: str = os.getenv('YT_API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        self.playlist_id = playlist_id
        playlist_info = self.youtube.playlists().list(id=self.playlist_id, part='snippet',maxResults=50).execute()
        self.title = playlist_info['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'

    def get_response(self):
        video_ids = self.get_all_videos()
        video_response = self.youtube.videos().list(part='contentDetails,statistics', id=','.join(video_ids)).execute()
        return video_response

    def get_all_videos(self):
        playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        return video_ids

    @property
    def total_duration(self):
        total_duration = timedelta()
        video_response = self.get_response()
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def show_best_video(self):
        response = self.get_response()
        likes = 0
        video_id = ''
        for video in response['items']:
            likes_counter = video['statistics']['likeCount']
            if int(likes_counter) > likes:
                likes = int(likes_counter)
                video_id = video['id']
        return f'https://youtu.be/{video_id}'
