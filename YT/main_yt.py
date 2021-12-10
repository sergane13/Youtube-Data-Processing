from data_acquisition import *
import time
from plot_generator import *


def main():

    subject, number_of_results = get_data()
    if check_if_already_stored(subject) is False:
        start = time.perf_counter()
        yt = YtStat(number_of_results, subject)
        yt.urls_search_channels()
        dictionary = yt.extract_all_channels_data()
        upload_data(dictionary)
        end = time.perf_counter()
        print(f'{round(end-start, 2)} seconds')
        show_plots(subject)
    else:
        print("Already stored in database.")
        show_plots(subject)


if __name__ == "__main__":
    main()

# https://www.googleapis.com/youtube/v3/search?key=AIzaSyC6ibX0SQssEvI33QtMKtPJCAvAFNj8zik&type=video&q=tank&order=viewCount&part=snippet&maxResult=30}

# https://www.googleapis.com/youtube/v3/channels?id=UC-F6LZSWz34xKknY8NNCzgQ&key=AIzaSyC6ibX0SQssEvI33QtMKtPJCAvAFNj8zik&part=snippet

# https://www.googleapis.com/youtube/v3/playlistItems?playlistId=VVUtRjZMWlNXejM0eEtrblk4Tk5DemdRLjU2QjQ0RjZEMTA1NTdDQzY=&key=AIzaSyC6ibX0SQssEvI33QtMKtPJCAvAFNj8zik&part=snippet&maxResults=50

# https://www.googleapis.com/youtube/v3/playlistItems?playlistId={ids}&key=AIzaSyC6ibX0SQssEvI33QtMKtPJCAvAFNj8zik&part=statistics&maxResults=50'

# https://www.googleapis.com/youtube/v3/videos?part=statistics&key=AIzaSyC6ibX0SQssEvI33QtMKtPJCAvAFNj8zik&id=rE_bJl2GAY8,-56x56UppqQ
