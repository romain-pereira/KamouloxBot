import tweepy
import threading
from random import randint
from config import config as cfg

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

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")


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
             + generateVerb() + generateWord(randint(0, 1)) + ".".capitalize())
    api.update_status(tweet)
    print("Le tweet \"" + tweet + "\" à bien été posté")


postTweet()
