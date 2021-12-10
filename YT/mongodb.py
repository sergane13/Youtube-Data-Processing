from pymongo import MongoClient

"""

This is a file which contain the majority of the functions that are responsible for database manipulation

"""


def routine_mongodb():

    """

    This function enables the communication with the database

    :return:
        Returns all the data from the database

    """

    url = f'mongodb+srv://root:tardis1313@cluster0.5jll2.mongodb.net/youtube?retryWrites=true&w=majority'
    cluster = MongoClient(url)
    db = cluster["youtube"]
    collection = db["yt data"]
    return collection


def upload_data(dictionary):

    """

    This function upload data to database

    :param dictionary:
        The dictionary with all the specific data to be saved on databse

     """

    collection = routine_mongodb()
    collection.insert_one(dictionary)


def find_data(subject):
    collection = routine_mongodb()
    subject_main = create_mongodb_string(subject)
    return collection.find_one({'_id': subject_main})


def find_all_data():
    collection = routine_mongodb()
    return collection.find({})


def check_if_already_stored(subject):
    data = find_data(subject)
    if data is None:
        return False
    else:
        return True


def create_mongodb_string(subject):
    return f"{subject}"
