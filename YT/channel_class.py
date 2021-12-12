from YT.auxilary_functions import *
from YT.video_class import Video
import statistics
import numpy as np
import time


class Channel:
    def __init__(self, total_view_count, subscriber_count, video_count, upload_id, name):
        self.total_view_count = total_view_count
        self.subscriber_count = subscriber_count
        self.video_count = video_count
        self.upload_id = upload_id
        self.name = name
        self.videos = []
        self.api_key = api_key(2)

    def urls_get_playlist_raw_data(self):

        """

        This function returns data from the playlist request

        @:return
            All the data from the playlistItems request

        """

        url = f'https://www.googleapis.com/youtube/v3/playlistItems?playlistId={self.upload_id}&key={self.api_key}' \
              f'&part=snippet&maxResults=50'
        return extracting_data(url)

    def urls_videos_ids(self):

        """

        This function processes and returns videos ids from the playlist request

        @:return
            All the video ids from the playlistItems request

        """

        data = self.urls_get_playlist_raw_data()
        video_ids = [data['items'][i]['snippet']['resourceId']['videoId'] for i in range(len(data['items']))]
        return video_ids

    def urls_search_videos(self):

        """

        This function processes videos statistics and content details

        """

        # We have problem HERE with removing print()
        # Unknown reasons for this problem
        time.sleep(0.01)
        # print(self.name)
        ids = self.urls_videos_ids()
        url = f'https://www.googleapis.com/youtube/v3/videos?part=statistics,snippet,contentDetails&' \
              f'key={self.api_key}&id={string_from_ids(ids)}'
        self.create_videos_objects(extracting_data(url))

    def create_videos_objects(self, data):

        """

        This function creates for every video an object type called 'Video' with the specific data(view_count,
        like_count, dislike_count, category_id, upload_date, duration)

        All videos objects are stored in self.videos

        """

        for i in range(len(data['items'])):
            view_count = data['items'][i]['statistics']['viewCount']
            like_count, dislike_count = 0, 0
            if 'likeCount' in data['items'][i]['statistics']:
                like_count = data['items'][i]['statistics']['likeCount']
                dislike_count = data['items'][i]['statistics']['dislikeCount']

            category_id = data['items'][i]['snippet']['categoryId']
            upload_date = data['items'][i]['snippet']['publishedAt'][0:10]

            duration = data['items'][i]['contentDetails']['duration']
            if duration == 'P0D':
                duration = 'live'
            else:
                duration = seconds_converter(duration)

            video_object = Video(view_count, like_count, dislike_count, category_id, upload_date, duration)
            self.videos.append(video_object)

    def metrics(self):

        """

        This method creates from all videos a custom statistic for the channel in shape of a dictionary

        @:returns
            average_views = the mean of views from all searched videos that fulfill the threshold date
            average_likes = the mean of likes from all searched videos that fulfill the threshold date
            average_dislikes = the mean of dislikes from all searched videos that fulfill the threshold date
            upload_frequency = the number of videos in average that the channel uploads per month
            status = the percentage of the growth of the channel in last 3 months (specific the threshold date)
            category = the main category of the channel (using mode to extract the most frequent id in videos)
            average_duration = the average duration of a video
            has_videos = 1/0 used to identify if channel has videos that fulfill the threshold

            All data is in a dictionary

        """

        var = time_set()
        videos_last_3months = np.array([True if var < self.videos[i].upload_date else False for i in range(len(self.videos))])
        view_count = np.array([int(self.videos[i].view_count) for i in range(len(self.videos))])[videos_last_3months]
        like_count = np.array([int(self.videos[i].like_count) for i in range(len(self.videos))])[videos_last_3months]
        dislike_count = np.array([int(self.videos[i].dislike_count) for i in range(len(self.videos))])[videos_last_3months]
        category_id = np.array([int(self.videos[i].category_id) for i in range(len(self.videos))])[videos_last_3months]
        duration = np.array([int(self.videos[i].duration) for i in range(len(self.videos))])[videos_last_3months]

        # print(videos_last_3months.sum())

        if videos_last_3months.sum() != 0:
            average_views = np.mean(view_count)
            average_likes = np.mean(like_count)
            average_dislikes = np.mean(dislike_count)
            upload_frequency = int(len(view_count) / 3)
            status = (100 * (view_count.sum() / int(self.total_view_count)))
            category = statistics.multimode(category_id)
            average_duration = np.mean(duration)

            return {
                'average_views': average_views,
                'average_likes': average_likes,
                'average_dislikes': average_dislikes,
                'upload_frequency': upload_frequency,
                'status': status,
                'category': category,
                'average_duration': average_duration,
                'has_videos': 1
            }
        else:
            return {
                'has_videos': 0
            }
