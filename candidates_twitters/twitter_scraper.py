import twitter
import csv
from config import key, secret, token_key, token_secret

api = twitter.Api(consumer_key = key,
                      consumer_secret = secret,
                      access_token_key = token_key,
                      access_token_secret = token_secret)


def all_statuses(name):
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
        print last_id
        print (len(page)-1)
    return raw_statuses

# No need to format if I'm going to write directly to csv
# def formatter(status_list):
#     formatted = []
#     for status in status_list:
#         info = [status.id,
#                 status.user.name,
#                 status.created_at,
#                 status.text,
#                 status.favorite_count,
#                 status.retweet_count]
#         formatted.append(info)
#     return formatted

def write_csv(tweet_list, file_name):
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


# From https://twitter.com/cspan/lists/presidential-candidates/members
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
