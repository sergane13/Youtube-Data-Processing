from YT.data_acquisition import *
import time
from YT.plot_generator import *


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