## Import and configuration
import json
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
import pytz
import pandas as pd
from configparser import ConfigParser
import sys
import os
import math
from clarku_youtube_crawler.crawlerObject import _CrawlerObject

CONFIG = "config.ini"
config = ConfigParser(allow_no_value=True)
config.read(CONFIG)


class RawCrawler(_CrawlerObject):
    def __init__(self):
        self.video_list_path = None
        super().__init__()

    def __build__(self):
        super().__build__("raw")

    # Crawl a list of videos which matches {search_key}. Save the data in {video_list_dir}
    # JSON returned from https://developers.google.com/youtube/v3/docs/search/list
    def _search_data(self, file_path, start_time, end_time, page_token=None):
        #     print("CURRENT_API: " + DEVELOPER_KEY)
        part = "snippet"
        try:
            if page_token:
                response = self.youtube.search().list(part=part,
                                                      maxResults=50,
                                                      q=self.search_key,
                                                      pageToken=page_token,
                                                      type="video",
                                                      publishedAfter=start_time.isoformat(),
                                                      publishedBefore=end_time.isoformat(),
                                                      regionCode="US"
                                                      ).execute()
            else:
                response = self.youtube.search().list(part=part,
                                                      maxResults=50,
                                                      q=self.search_key,
                                                      type="video",
                                                      publishedAfter=start_time.isoformat(),
                                                      publishedBefore=end_time.isoformat(),
                                                      regionCode="US"
                                                      ).execute()
            self._write_item(file_path, response["items"], check_duplicate=False) #remove duplicate
            return response
        except HttpError as e:
            error = json.loads(e.content)["error"]["errors"][0]["reason"]
            print(error)
            if error == "dailyLimitExceeded" or error == "quotaExceeded":
                self._try_next_id()
                return self._search_data(file_path, start_time, end_time, page_token)
        except Exception as e:
            sys.exit(0)
            return "error"

    def _write_item(self, file_path, items, check_duplicate=False):
        if check_duplicate:
            with open(file_path, 'a+') as fp:
                for item in items:
                    item_path = self.video_data_dir + item["videoId"] + ".json"
                    if not self.isCrawled(item_path):
                        fp.write(json.dumps(item)+"\n")
            return

        with open(file_path, 'a+') as fp:
            for item in items:
                fp.write(json.dumps(item) + "\n")

    def _crawl_data(self, start_time, end_time):
        response = self._search_data(self.video_list_path, start_time, end_time)
        total_result = response["pageInfo"]["totalResults"]
        while True:
            response = self._search_data(self.video_list_path, start_time, end_time, response["nextPageToken"])
            if "nextPageToken" not in response:
                start_time_mark = self.toDayFormat(start_time)
                end_time_mark = self.toDayFormat(end_time)
                print(f"total results:{str(total_result)} between {start_time_mark} and {end_time_mark}")
                break

    def _crawl_data_one_day(self, start_datetime):
        delta = timedelta(hours=24)
        print(f"crawling video list....")
        self._crawl_data(start_datetime, start_datetime + delta)

    # check for duplicate video item
    def crawl(self, search_key, **kwargs):
        self.search_key = search_key
        default = datetime.now() - timedelta(days=self.TIME_DELTA)
        start_day = kwargs.get("start_day", default.day)
        start_month = kwargs.get("start_month", default.month)
        start_year = kwargs.get("start_year", default.year)
        day_count = kwargs.get("day_count", math.inf)

        start_datetime = datetime(year=start_year, month=start_month, day=start_day, tzinfo=pytz.utc)
        date_mark = self.toDayFormat(start_datetime)
        delta = timedelta(hours=24)

        count = 0
        while count < day_count:
            print(f"start crawling:{date_mark}")
            # Initialize the paths
            self.video_list_path = f"{self.video_list_dir}{self.search_key}_video_list_{date_mark}.json"
            # crawl data, update start date.
            self._crawl_data_one_day(start_datetime)
            start_datetime += delta
            date_mark = self.toDayFormat(start_datetime)
            count += 1

    # The field crawler will use the video_list_workfile.csv to crawl video data of each video id.
    def _merge_to_workfile(self, filepath, destination, keep_duplicate=True):
        video_list = set()
        json_list = (file for file in os.listdir(filepath) if file.endswith(".json"))
        # Save video meta data of all the videos saved in {video_list_path}
        for filename in json_list:
            with open(filepath + filename, 'r') as fp:
                line = fp.readline()
                while line and line != "":
                    search_result = json.loads(line)
                    if "videoId" in search_result["id"]:
                        item_path = self.video_data_dir + search_result["id"]["videoId"] + ".json"
                        if (not keep_duplicate and not self.isCrawled(item_path)) or keep_duplicate:
                            video_id = ":" + search_result["id"]["videoId"]
                            channel_id = search_result["snippet"]["channelId"]
                            date = search_result["snippet"]["publishedAt"].split("T")[0]
                            search_key = self.search_key
                            video_list.add((video_id, channel_id, date, search_key))
                    line = fp.readline()

        df = pd.DataFrame(data=video_list, columns=["videoId", "channelId", "publishedAt", "searchKey"])
        df.to_csv(destination, index=False)

    # comment_page_count: how many pages of comments will be crawled. Each page has 50 comments.
    def crawl_videos_in_list(self, comment_page_count):
        self._merge_to_workfile(self.video_list_dir, self.video_list_workfile, keep_duplicate=False)
        print(f"crawling data from {self.video_list_workfile}....")
        df = pd.read_csv(self.video_list_workfile)
        for index, row in df.iterrows():
            video_id = row["videoId"][1:]  # remove the ":" in the 1st char
            channel_id = row["channelId"]
            filename = video_id + ".json"
            print(filename)
            if not self.isCrawled(self.video_data_dir+filename):
                video = self.get_video(video_id)
                comments = self.get_comments(video_id, comment_page_count)
                channel = self.get_channel(channel_id)
                caption = self.get_caption(video_id)
                result = {
                    "videoId": video_id,
                    "channelId": channel_id,
                    "video": video,
                    "comments": comments,
                    "channel": channel,
                    "caption": caption,
                }
                with open(self.video_data_dir + filename, 'w+') as fp:
                    fp.write(json.dumps(result) + "\n")

    # def merge_all(self, **kwargs):
    #     # merge all video jsons into one big json
    #     video_result_path = kwargs.get("save_to", self.DEFAULT_RAW_FINAL_FILE)
    #     video_writer = open(video_result_path, "w+")
    #     # df = pd.read_csv(self.video_list_workfile)
    #     # id_list = list(df["videoId"])
    #     # id_list = [i[1:] for i in id_list]
    #     # id_set = set(id_list)
    #     # print(f"Total id {len(id_set)}")
    #     json_list = (file for file in os.listdir(self.video_data_dir) if file.endswith(".json"))
    #     for filename in json_list:
    #         # if filename.split(".")[0] not in id_set:
    #         #     print(filename)
    #         # Save video meta data of all the videos saved in {video_list_path}
    #         with open(self.video_data_dir + filename, 'r') as fp:
    #             line = fp.readline()
    #             while line and line != "":
    #                 video_writer.write(line)
    #                 line = fp.readline()
    #
    #     video_writer.flush()
    #     video_writer.close()
    def merge_all(self, **kwargs):
        # merge all video jsons into one big json
        video_result_path = kwargs.get("save_to", self.DEFAULT_RAW_FINAL_FILE)
        video_writer = open(video_result_path, "w+")

        json_list = (file for file in os.listdir(self.video_data_dir) if file.endswith(".json"))
        for filename in json_list:
            with open(self.video_data_dir + filename, 'r') as fp:
                line = fp.readline()
                while line and line != "":
                    video_writer.write(line)
                    line = fp.readline()

        video_writer.flush()
        video_writer.close()