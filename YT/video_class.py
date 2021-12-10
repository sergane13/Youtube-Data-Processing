"""

    This is a class which contain all the available data for a video
    The variables are self explanatory

"""


class Video:
    def __init__(self, view_count, like_count, dislike_count, category_id, upload_date, duration):
        self.view_count = view_count
        self.like_count = like_count
        self.dislike_count = dislike_count
        self.category_id = category_id
        self.upload_date = upload_date
        self.duration = duration
