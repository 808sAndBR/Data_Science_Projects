import twitter
from config import key, secret, token_key, token_secret

api = twitter.Api(consumer_key = key,
                      consumer_secret = secret,
                      access_token_key = token_key,
                      access_token_secret = token_secret)

statuses = api.GetUserTimeline(screen_name = 'HillaryClinton',
                                count = 200, since_id = '')

statuses2 = api.GetUserTimeline(screen_name = 'HillaryClinton',
                                count = 200, since_id = 667007489460862977)

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


hil = all_statuses('HillaryClinton')

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
