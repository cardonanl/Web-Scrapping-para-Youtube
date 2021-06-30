# -*- coding: utf-8 -*-

##########################################################
############# Web Scrapping. Caso Youtube.################
##########################################################

"""
 - Tener en cuenta que requiere una  API de Google. Referirse al Readme para más información.
"""

#################################################################
### Código base. No requiere modificaciones para su uso actual ##
#################################################################
import json
import requests
from tqdm import tqdm


class YTstats:

    def __init__(self, api_key, channel_id):
        self.api_key = api_key
        self.channel_id = channel_id
        self.channel_statistics = None
        self.video_data = None

    def extract_all(self):
        self.get_channel_statistics()
        self.get_channel_video_data()

    def get_channel_statistics(self):
        """Extract the channel statistics"""
        print('Obteniendo las estadísticas del canal...')
        url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={self.channel_id}&key={self.api_key}'
        pbar = tqdm(total=1)

        json_url = requests.get(url)
        data = json.loads(json_url.text)
        try:
            data = data['items'][0]['statistics']
        except KeyError:
            print('No se logró obtener las estadísticas del canal')
            data = {}

        self.channel_statistics = data
        pbar.update()
        pbar.close()
        return data

    def get_channel_video_data(self):
        "Extract all video information of the channel"
        print('Obteniendo datos del video')
        channel_videos, channel_playlists = self._get_channel_content(limit=50)

        parts = ["snippet", "statistics", "contentDetails", "topicDetails"]
        for video_id in tqdm(channel_videos):
            for part in parts:
                data = self._get_single_video_data(video_id, part)
                channel_videos[video_id].update(data)

        self.video_data = channel_videos
        return channel_videos

    def _get_single_video_data(self, video_id, part):
        """
        Extract further information for a single video
        parts can be: 'snippet', 'statistics', 'contentDetails', 'topicDetails'
        """

        url = f"https://www.googleapis.com/youtube/v3/videos?part={part}&id={video_id}&key={self.api_key}"
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        try:
            data = data['items'][0][part]
        except KeyError as e:
            print(f'Error! Could not get {part} part of data: \n{data}')
            data = dict()
        return data

    def _get_channel_content(self, limit=None, check_all_pages=True):
        """
        Extract all videos and playlists, can check all available search pages
        channel_videos = videoId: title, publishedAt
        channel_playlists = playlistId: title, publishedAt
        return channel_videos, channel_playlists
        """
        url = f"https://www.googleapis.com/youtube/v3/search?key={self.api_key}&channelId={self.channel_id}&part=snippet,id&order=date"
        if limit is not None and isinstance(limit, int):
            url += "&maxResults=" + str(limit)

        vid, pl, npt = self._get_channel_content_per_page(url)
        idx = 0
        while (check_all_pages and npt is not None and idx < 10):
            nexturl = url + "&pageToken=" + npt
            next_vid, next_pl, npt = self._get_channel_content_per_page(nexturl)
            vid.update(next_vid)
            pl.update(next_pl)
            idx += 1

        return vid, pl

    def _get_channel_content_per_page(self, url):
        """
        Extract all videos and playlists per page
        return channel_videos, channel_playlists, nextPageToken
        """
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        channel_videos = dict()
        channel_playlists = dict()
        if 'items' not in data:
            print('Error! No se logró obtener información del canal!\n', data)
            return channel_videos, channel_videos, None

        nextPageToken = data.get("nextPageToken", None)

        item_data = data['items']
        for item in item_data:
            try:
                kind = item['id']['kind']
                published_at = item['snippet']['publishedAt']
                title = item['snippet']['title']
                if kind == 'youtube#video':
                    video_id = item['id']['videoId']
                    channel_videos[video_id] = {'publishedAt': published_at, 'title': title}
                elif kind == 'youtube#playlist':
                    playlist_id = item['id']['playlistId']
                    channel_playlists[playlist_id] = {'publishedAt': published_at, 'title': title}
            except KeyError as e:
                print('Error! No se logró extraer información del objeto:\n', item)

        return channel_videos, channel_playlists, nextPageToken

    def dump(self):
        """Dumps channel statistics and video data in a single json file"""
        if self.channel_statistics is None or self.video_data is None:
            print('data is missing!\nCall get_channel_statistics() and get_channel_video_data() first!')
            return

        fused_data = {self.channel_id: {"channel_statistics": self.channel_statistics,
                                        "video_data": self.video_data}}

        channel_title = self.video_data.popitem()[1].get('channelTitle', self.channel_id)
        channel_title = channel_title.replace(" ", "_").lower()
        filename = channel_title + '.json'
        with open(filename, 'w') as f:
            json.dump(fused_data, f, indent=4)

        print('file dumped to', filename)
        
######################################################
########### Código para ejecución ####################
######################################################
"""
Requiere tener el API de Youtube/Google y el ID del canal que se desea explorar.

Si el código se desea ejecutar en un ambiente como Pycharm (y no en notebooks como Google Colab o Jupyter) se recomienda que el Código Base sea alojado en un .py independiente y se nombre con por ejemplo "estadisticas_youtube.py".

Posteriormente, el código de ejecución se puede iniciar con una linea tipo "from estadisticas_youtube import YTstats".
"""

API_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
channel_id = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'

yt = YTstats(API_KEY, channel_id)

yt.extract_all()

yt.dump()  # dumps to .json

################################
"""# Análisis de informaición"""
#################################

import json
import pandas as pd

file = "matarife_oficial.json"
data = None
with open(file, 'r') as f:
  data = json.load(f)

channel_id, stats = data.popitem()
print(channel_id)
channel_stats = stats["channel_statistics"]
video_stats = stats["video_data"]

"""# Estadísticas del Canal"""

print('views', channel_stats["viewCount"])
print('subscriber', channel_stats["subscriberCount"])
print('videos', channel_stats["videoCount"])

# Estadísticas de los videos

"""
Notese lo siguiente en esta sección. 
El ForIn para extraer las estadísticas de los videos usa los puntos de información alojados en el archivo .Json. 
Este puede ser consultado en un explorador web común donde el objeto "video data" contiene cada video alojado como token (ej: "ukNAtIFuJCk"). 
De manera que si se desea extraer más información, solo se necesita agragar a la lista del blucle.

"""

sorted_vids = sorted(video_stats.items(), key=lambda item: int(item[1]["viewCount"]), reverse=True)
stats = []
for vid in sorted_vids:
  video_id = vid[0]
  date = vid[1]["publishedAt"]
  title = vid[1]["title"]
  views = int(vid[1]["viewCount"])
  likes = int(vid[1]["likeCount"])
  dislikes = int(vid[1]["dislikeCount"])
  comments = int(vid[1]["commentCount"])
  stats.append([date,title, views, likes, dislikes, comments])

df = pd.DataFrame(stats, columns =["date","title", "views","likes","dislikes","comments"])
df.head()

top10 = df.head(10)
ax = top10.plot.bar(x="title", y = "views", fontsize=14)

#Guardar CSV

df.to_csv("/content/DF_XXXXXXX.csv", index=True)







####FIN
