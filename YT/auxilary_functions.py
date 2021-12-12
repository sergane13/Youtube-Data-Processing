from datetime import date
import datetime
import requests
import json
from threading import *


def seconds_converter(duration):

    """

    This is a function that process a strig and convert it to a more workable format
    It is used to extract the duration from yt requests in a more approachable way

    @:param duration:
        A string in a yt format that represent the duration of a video
    @:return:
        A more workable format and easy to use

    """

    week, day, hour, minutes, sec = 0, 0, 0, 0, 0
    duration = duration.lower()
    value = ''
    for c in duration:
        if c.isdigit():
            value += c
            continue
        elif c == 'p' or c == 't':
            pass
        elif c == 'w':
            week = int(value) * 604800
        elif c == 'd':
            day = int(value) * 86400
        elif c == 'h':
            hour = int(value) * 3600
        elif c == 'm':
            minutes = int(value) * 60
        elif c == 's':
            sec = int(value)
        value = ''

    return str(week + day + hour + minutes + sec)


def time_set():

    """

    This function sets the threshold for the videos(time threshold)

    @:return:
        Returns the threshold data in a string format

    """

    return str(date.today() - datetime.timedelta(days=90))


def get_data():

    """

    This function is responsible for the input parameters of the whole program

    @:return:
        Returns the subject in a format the is usable in requests
        Returns the number of videos that will be searched according to the subject

    """

    print('Enter what you search: ')
    aux = input()
    print('Enter the number of videos to search: ')
    number = input()
    return '%20'.join(aux.split()), int(number)


def api_key(number):

    """

    This function contain 3 api keys used to do requests

    @:param number:
        Represent the number of what api key you chose
    @:return:
        The api key

    There are 3 api keys because I used 3 different google accounts

    """

    if number == 1:
        return '-api 1-'
    elif number == 2:
        return '-api 2-'
    elif number == 3:
        return '-api 3-'


def extracting_data(url):

    """

    Take all the data from the request
    @:param url:
        A simple url from web
    @:return:
        A variable which contain all the data

    """

    file_url = requests.get(url)
    return json.loads(file_url.text)


def string_from_ids(ids):

    """

    Concatenates the ids with ',' to do only one request for all ids

    @:return
        A concatenated string

    """

    return ','.join(ids)


def operations_threading_create(threads):

    """

    This function is responsible for creation of multiple threads for every channel to do the processing faster

    @:param threads:
        A list which contain all the channels (object types)
    @:return:
        A list with all created threads

    """

    thread_list = []

    for i in range(len(threads)):
        thread = Thread(target=threads[i].urls_search_videos)
        thread.start()
        thread_list.append(thread)

    return thread_list


def operations_threading_join(threads):

    """

    This function join all the threads

    @:param threads:
        A list with all created threads

    """

    for thread in threads:
        thread.join()
