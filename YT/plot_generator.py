import matplotlib.pyplot as plt
from YT.mongodb import *


"""
    Plot data received
"""


def show_plots(subject):

    subject_main = create_mongodb_string(subject)
    df = find_data(subject_main)

    name = df['name']
    views = df['average_views']
    likes = df['average_likes']
    dislikes = df['average_dislikes']
    upload_frequency = df['upload_frequency']
    status = df['status']
    # category = df['category'][0]
    average_duration = df['average_duration']
    # subscribers = df['subscribers']

    fig, ax = plt.subplots(nrows=2, ncols=2)

    ax[0, 0].scatter(views, upload_frequency)
    ax[0, 0].set_xlabel('views')
    ax[0, 0].set_ylabel('upload_frequency')

    ax[0, 1].scatter(views, status)
    ax[0, 1].set_xlabel('views')
    ax[0, 1].set_ylabel('status')

    ax[1, 0].scatter(views, average_duration)
    ax[1, 0].set_xlabel('views')
    ax[1, 0].set_ylabel('average_duration')

    ax[1, 1].scatter(likes, dislikes)
    ax[1, 1].set_xlabel('likes')
    ax[1, 1].set_ylabel('dislikes')

    for i, txt in enumerate(name):
        ax[0, 0].annotate(txt, (views[i], upload_frequency[i]))
        ax[0, 1].annotate(txt, (views[i], status[i]))
        ax[1, 0].annotate(txt, (views[i], average_duration[i]))
        ax[1, 1].annotate(txt, (likes[i], dislikes[i]))

    plt.show()
