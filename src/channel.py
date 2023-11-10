import os
from googleapiclient.discovery import build
import json


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.info = self.youtube.channels().list(id=self.__channel_id, part='snippet, statistics').execute()
        self.title = self.info['items'][0]['snippet']['title']
        self.description = self.info['items'][0]['snippet']['description']
        self.url = 'https://www.youtube.com/' + str(self.__channel_id)
        self.subscribers = self.info['items'][0]['statistics']['subscriberCount']
        self.video_count = self.info['items'][0]['statistics']['videoCount']
        self.total_views = self.info['items'][0]['statistics']['viewCount']

    def print_info(self) -> str:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    @property
    def get_id(self):
        """
        Геттер для атрибута channel_id
        """
        return self.__channel_id

    @get_id.setter
    def channel_id(self, new_id):
        """
        Ловушка сэттера для channel_id. Так как из условия задачи channel_id изменять мы не можем
        """
        if new_id:
            print("AttributeError: property 'channel_id' of 'Channel' object has no setter")
            self.__channel_id = self.__channel_id

    @classmethod
    def get_service(cls):
        """
        Класс-метод возвращающий экземпляр j,]trn для работы с YouTube API
        """
        return build('youtube', 'v3', developerKey=os.getenv('YT_API_KEY'))

    def to_json(self, directory):
        """
        Метод, сохранающий в JSON файл значения атрибутов экземпляра Channel
        """
        json_data = {
            'channel_id': self.__channel_id,
            "channel_name": self.title,
            "channel_description": self.description,
            "channel_url_short": self.url,
            "channel_subscribers": self.subscribers,
            "channel_video_count": self.video_count,
            "channel_total_views": self.total_views
        }
        # Открытие файла на запись
        with open(directory, 'w') as file:
            file.write(json.dumps(json_data, indent=2, ensure_ascii=False))
