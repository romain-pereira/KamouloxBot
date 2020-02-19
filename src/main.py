import tweepy, threading, logging
from random import randint
import config.config as cfg
from logging.handlers import RotatingFileHandler

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
file_handler = RotatingFileHandler('../log/kamouloxbot.log', 'a', 1000000, 1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)

voyelle = "a", "e", "é", "ê", "è", "i", "o", "u", "y", "h"

verbs = open("../resources/verbs.txt", "r", encoding="utf-8")
male = open("../resources/male.txt", "r", encoding="utf-8")
feminine = open("../resources/feminine.txt", "r", encoding="utf-8")
adjectifMale = open("../resources/adjectifMale.txt", "r", encoding="utf-8")
adjectifFeminine = open("../resources/adjectifFeminin.txt", "r", encoding="utf-8")

verbsLines = verbs.readlines()
maleLines = male.readlines()
feminineLines = feminine.readlines()
adjMaleLines = adjectifMale.readlines()
adjFemininLines = adjectifFeminine.readlines()

auth = tweepy.OAuthHandler(cfg.apiKey, cfg.apiSecret)
auth.set_access_token(cfg.accessToken, cfg.accessTokenSecret)

api = tweepy.API(auth)
user = api.me()

try:
    api.verify_credentials()
    logger.info("Authentication OK")
except:
    logger.warning("Error during authentication")


def generateVerb():
    randVerbs = randint(0, len(verbsLines) - 1)
    verb = verbsLines[randVerbs]

    if verb.startswith(voyelle):
        return "j\'" + verb.rstrip()
    else:
        return "je " + verb.rstrip()


def generateWord(withAdj):
    int = randint(0, 1)
    adj = ""

    if withAdj == 1 and int == 1:
        adj = " " + adjMaleLines[randint(0, len(adjMaleLines)) - 1].rstrip()
    elif withAdj == 0 and int == 0:
        adj = " " + adjFemininLines[randint(0, len(adjFemininLines)) - 1].rstrip()

    if int == 1:
        return " un " + maleLines[randint(0, len(maleLines)) - 1].strip() + adj
    else:
        return " une " + feminineLines[randint(0, len(feminineLines)) - 1].strip() + adj


def postTweet():
    threading.Timer(3600.0, postTweet).start()
    tweet = (generateVerb() + generateWord(randint(0, 1)) + " et "
             + generateVerb() + generateWord(randint(0, 1)) + ".").capitalize()
    api.update_status(tweet)
    logger.info("@" + user.screen_name + " Tweet : \"" + tweet + "\" as been posted")

postTweet()
