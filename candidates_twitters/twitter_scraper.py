import twitter
import csv
from time import sleep

# Set up a config.py file with your values
# can create/get your existing from https://apps.twitter.com/
from config import key, secret, token_key, token_secret

api = twitter.Api(consumer_key = key,
                      consumer_secret = secret,
                      access_token_key = token_key,
                      access_token_secret = token_secret)


def all_tweets(name):
    """ Twitter limits the number of tweets returned to 200
    per call and 3200 total. So this itterate through them to
    get all tweets. """
    raw_statuses = []
    last_id = ''
    for i in range(0,16):
        page = api.GetUserTimeline(screen_name = name,
                                count = 200, max_id = last_id)
        raw_statuses.extend(page)
        last_id = page[(len(page)-1)].id
    return raw_statuses


def write_csv(tweet_list, file_name):
    """ Write all tweets passed to it to csv"""
    with open(file_name, 'wb') as csvfile:
        quotewriter = csv.writer(csvfile)
        quotewriter.writerow(['id',
                    'canidate',
                    'created',
                    'text',
                    'likes',
                    'retweets'])
        for tweet in tweet_list:
            quotewriter.writerow([tweet.id,
                                tweet.user.name,
                                tweet.created_at,
                                tweet.text.encode("utf-8"),
                                tweet.favorite_count,
                                tweet.retweet_count])


def everyones_tweets(canidates, master_list):
    """ Gets all tweets from all canidates in list passed to it
    Twitter rate limits agresively so this waits 15 minutes after
    each. Total time is 4.25 hours"""
    for canidate in canidates:
        master_list.extend(all_tweets(canidate))
        sleep(900)


# All canidates
# from https://twitter.com/cspan/lists/presidential-candidates/members
canidates = ['gov_gilmore',
    'GovernorPataki',
    'ChrisChristie',
    'HillaryClinton',
    'RealBenCarson',
    'LindseyGrahamSC',
    'RandPaul',
    'BernieSanders',
    'JebBush',
    'CarlyFiorina',
    'RickSantorum',
    'realDonaldTrump',
    'tedcruz',
    'JohnKasich',
    'MartinOMalley',
    'marcorubio',
    'GovMikeHuckabee']

# Twitter rate limit makes this not work
canidate_tweets =[]

everyones_tweets(canidates, canidate_tweets)
write_csv(canidate_tweets, 'canidate_tweets.csv')






