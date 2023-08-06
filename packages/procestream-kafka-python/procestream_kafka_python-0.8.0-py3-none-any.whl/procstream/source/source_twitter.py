import os, json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from procstream.source.source import DataSourceService


config = {"TWITTER_ACCESS_TOKEN": os.environ.get("TWITTER_ACCESS_TOKEN", ""),
          "TWITTER_ACCESS_TOKEN_SECRET": os.environ.get("TWITTER_ACCESS_TOKEN_SECRET", ""),
          "TWITTER_CONSUMER_KEY": os.environ.get("TWITTER_CONSUMER_KEY", ""),
          "TWITTER_CONSUMER_SECRET": os.environ.get("TWITTER_CONSUMER_SECRET", ""),
          "TWITTER_FILTER_TRACK": os.environ.get("TWITTER_FILTER_TRACK", ""),
          "MODULE_NAME": os.environ.get("MODULE_NAME", "TWITTER_DATA_COLLECTOR"),
          "CONSUMER_GROUP": os.environ.get("CONSUMER_GROUP", "TWITTER_DATA_COLLECTOR_CG")
          }


class StdOutListener(StreamListener):

    def __init__(self, datasource_service_obj):
        super().__init__()
        self.datasource_service_obj = datasource_service_obj

    def on_data(self, data):
        # print(data)
        tweet_data = json.loads(data)
        for key, value in tweet_data.items():
            if isinstance(value, str):
                new_string = value.replace("\r", " ")
                tweet_data[key] = new_string.replace("\n", " ")
        self.datasource_service_obj.produce_to_topic(tweet_data)
        print(tweet_data)
        return True

    def on_error(self, status):
        print(status)


class TwitterDataCollector():

    def run(self, new_config=None):
        new_config = config if not new_config else new_config

        twitter_data_source_service_obj = DataSourceService(new_config)

        listener = StdOutListener(twitter_data_source_service_obj)

        auth = OAuthHandler(new_config.get("TWITTER_CONSUMER_KEY"), new_config.get("TWITTER_CONSUMER_SECRET"))

        auth.set_access_token(new_config.get("TWITTER_ACCESS_TOKEN"), new_config.get("TWITTER_ACCESS_TOKEN_SECRET"))

        stream = Stream(auth, listener)

        stream.filter(track=new_config.get("TWITTER_FILTER_TRACK").split(","))
