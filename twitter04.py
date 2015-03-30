import tweepy
import json

import time

localtime   = time.localtime()
timeString  = time.strftime("%H:%M:%S", localtime)

def get_api(cfg):
    auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
    auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
    return tweepy.API(auth)

def main():
    # Fill in the values noted in previous step here
    cfg = {
    "consumer_key"        : "QgRcWDdeMB0UxxvoYsgVCPaDM",
    "consumer_secret"     : "MHKNSApkVXPlepeP9oAswBRQX2GKZG4UBh9vwLAd2zLPFDiV2T",
    "access_token"        : "3066078365-Uy7Cr4GnBlOl4CQqFFAteM6eRlGTvT1q7Vh78ZP",
    "access_token_secret" : "nGtHOkR4XTVRf1dnU9k7cLV2Kh2NeEKRFAHB3ZE0F7LFD"
    }

    api = get_api(cfg)
    print(api.me().name,"name",timeString)
    results = dict()
    while True:
        search_results = api.search(q="@dqscolasanti", count=1000)
        #print(localtime.tm_hour,localtime.tm_min,localtime.tm_sec)
        time_start =datetime.datetime.fromtimestamp(time.mktime(time.localtime()))
        print(time_start)
        for tweet in search_results:
            print("From:",tweet._json['user']['name'],len(results))
            print(tweet.text[13:])
            print()

        time.sleep(10)

if __name__ == '__main__':
	main()
