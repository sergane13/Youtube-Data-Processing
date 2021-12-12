import numpy as np
from YT.auxilary_functions import *
from YT.channel_class import Channel
import time


"""

 Short description:
 
 After the subject has been introduced , a search request will be made for the number of videos you wish.
 From this number of videos will be extracted all channels without duplicates
 For every channel , will be made a request to get statistics and content from all videos in the last 3 months
 Finally, for every channel will be made a custom report (in a dictionary) which will contain some custom statistics
 
 For every channel there is an object created with the class 'Channel' 
 For every video there is an object created with the class 'Videos' 
 
"""


class YtStat:

    def __init__(self, max_results, subject):

        self.api_key = api_key(2)
        self.subject = subject
        self.maxResults = max_results
        self.raw_data = self.urls_search()
        self.channels = []
        self.thread_list = []

    def urls_search(self):

        """

        This function uses youtube search engine to search for a number of videos related to the subject

        The number of videos is self.maxResults
        The subject is self.subject

        @:return
            All the data from search request in form of a dictionary full of lists and other dictionarys

        """

        url = f'https://www.googleapis.com/youtube/v3/search?key={self.api_key}&type=video&q={self.subject}' \
              f'&order=viewCount&part=snippet&maxResults={self.maxResults}'

        return extracting_data(url)

    def urls_channels_ids(self):

        """

        This function processes and returns channels ids from the raw data

        @:return
            All channels ids which have been searched via search request

        """

        data = self.raw_data
        channel_id = [data['items'][i]['snippet']['channelId'] for i in range(self.maxResults)]
        return list(dict.fromkeys(channel_id))

    def urls_channels_names(self):

        """

        This function processes and returns channels names from the raw data

        @:return
            All channels names which have been searched via search request

        """

        data = self.raw_data
        channel_name = [data['items'][i]['snippet']['channelTitle'] for i in range(self.maxResults)]
        return list(dict.fromkeys(channel_name))

    def urls_search_channels(self):
        start = time.perf_counter()
        """

        This function processes channels statistics and content details
        This function has integrated timer to see the amount of time it takes to do the majority of the job
        
        """

        ids = self.urls_channels_ids()
        url = f'https://www.googleapis.com/youtube/v3/channels?key={self.api_key}&id={string_from_ids(ids)}&' \
              f'part=statistics,contentDetails'
        self.create_channel_objects(extracting_data(url))
        self.search_all_videos()
        end = time.perf_counter()
        print(f'{round(end - start, 4)} seconds')

    def create_channel_objects(self, data):

        """

        This function creates for every channel an object type called 'Channel' with the specific data(total_view_count,
        subscriber_count, video_count and upload_id)

        All channel objects are stored in self.channels
        @:param
            The data tha has been extracted from the channels request to create the channel objects
            
        """

        names = self.urls_channels_names()
        for i in range(len(data['items'])):
            total_view_count = data['items'][i]['statistics']['viewCount']
            subscriber_count = data['items'][i]['statistics']['subscriberCount']
            video_count = data['items'][i]['statistics']['videoCount']
            upload_id = data['items'][i]['contentDetails']['relatedPlaylists']['uploads']
            channel_object = Channel(total_view_count, subscriber_count, video_count, upload_id, names[i])
            self.channels.append(channel_object)

    def search_all_videos(self):

        """

        This function create multiple threads to do individual requests and processing for every channel
        Creates the threads here and also destroy them

        """

        threads = operations_threading_create(self.channels)
        operations_threading_join(threads)

    def extract_all_channels_data(self):

        """

        This function extract all the custom statistics for every channel and concatenate them in one list there all the
        lists in a dictionary

        The keys from the dictionary are self explanatory

        @:returns
            _id = represent the id that will be stored in the database (the subject)
            name = a list with the name of the channels
            average_views = a list with the average views if a channel per video
            average_likes = a list with the average likes if a channel per video
            average_dislikes = a list with the average dislikes if a channel per video
            upload_frequency = a list with the upload frequency of the channel per month
            status = a list with the percentage of the growth of the channels in last 3 months
            category = a list with the main category of the channels (using mode to extract the most frequent id )
            average_duration = a list with the average durations of a video for every channel
            subscribers = a list with the number of subscribers of the channels

            All data is in a dictionary

        """

        channel_has_videos = np.array([True if self.channels[i].metrics()['has_videos'] else False for i in range(len(self.channels))])
        channel = np.array(self.channels)[channel_has_videos]
        name = np.array([channel[i].name for i in range(len(channel))])
        average_views = np.array([channel[i].metrics()['average_views'] for i in range(len(channel))])
        average_likes = np.array([channel[i].metrics()['average_likes'] for i in range(len(channel))])
        average_dislikes = np.array([channel[i].metrics()['average_dislikes'] for i in range(len(channel))])
        upload_frequency = np.array([channel[i].metrics()['upload_frequency'] for i in range(len(channel))])
        status = np.array([channel[i].metrics()['status'] for i in range(len(channel))])
        category = np.array([channel[i].metrics()['category'] for i in range(len(channel))])
        average_duration = np.array([channel[i].metrics()['average_duration'] for i in range(len(channel))])
        subscribers = np.array([channel[i].subscriber_count for i in range(len(channel))])

        return {
                "_id": self.subject,
                'name': name.tolist(),
                'average_views': average_views.tolist(),
                'average_likes': average_likes.tolist(),
                'average_dislikes': average_dislikes.tolist(),
                'upload_frequency': upload_frequency.tolist(),
                'status': status.tolist(),
                'category': category.tolist(),
                'average_duration': average_duration.tolist(),
                'subscribers': subscribers.tolist()
                }
