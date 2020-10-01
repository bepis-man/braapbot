import tweepy # the stuff so that i can tweet
import random # rng generator
import sys
from datetime import datetime # for logging

debug = 0

if len(sys.argv) > 1:
    debug = 1
    debugText = sys.argv[1] # second argument, since the script itself is an argument

    print(debugText)

tweetChance = 10 # chance to tweet, to avoid spam

if debug == 0: # don't bother authenticating if debug mode

    # read keys from file and authenticate
    keysFile = open("keys.txt", "r") # not included in repository for security
    keysRead = keysFile.read()
    keys = keysRead.split() # separate into list

    API_KEY = keys[1]
    API_KEY_SECRET = keys[3]
    ACCESS_TOKEN = keys[5]
    ACCESS_TOKEN_SECRET = keys[7]

    auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # get api
    api = tweepy.API(auth)

    # check if authentication even worked
    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")
        exit()

def getWords():
    # set a bunch of variables and things AFTER authenticating since there's no point doing all this if it doesn't run
    # import fart selection to choose from
    fartFile = open("wordlists/farts.txt", "r")
    fartRead = fartFile.read()
    farts = fartRead.split()

    # import verbs list
    verbList = open("wordlists/verbs.txt", "r")
    verbsRead = verbList.read()
    verbs = verbsRead.split()

    # import nono words list - don't want to reply to a serious or vent tweet
    nonoList = open("wordlists/nono.txt", "r")
    nonoRead = nonoList.read()
    nonoWords = nonoRead.split()

    sexList = open("wordlists/sex.txt", "r")
    sexRead = sexList.read()
    sexWords = sexRead.split()

    class words:
        fartsW = farts
        verbsW = verbs
        nonoWordsW = nonoWords
        sexWordsW = sexWords

    return words

def tweet(mode, mode1len, text, status, farts):
    if mode == 1:
        replyToTweetWithSex(text[random.randint(0,len(text)-1)], status)
    elif mode == 2:
        replyToTweetWithAFunny(text[random.randint(0,len(text)-1)], farts, status)
    elif mode == 3:
        if not random.randint(0,1): # random true or false
            replyToTweetWithSex(text[random.randint(0,mode1len-1)], status)
        else:
            replyToTweetWithAFunny(text[random.randint(mode1len,len(text)-1)], farts, status)

def findWord(word, text):
    for char in "\"'~*?!.,":
        word = word.replace(char,'')

    return ((' ' + word.lower() + ' ') in (' ' + text.lower() + ' '))

def replyToTweetWithAFunny(verb, farts, status):
    if debug == 0:
        tweetMessage = f"@{status.user.screen_name} {verb} THIS! {farts[random.randint(0,len(farts)-1)]}"
    else:
        tweetMessage = f"{verb} THIS! {farts[random.randint(0,len(farts)-1)]}"

    print(tweetMessage)
    if debug == 0:
        api.update_status(tweetMessage, in_reply_to_status_id=status.id)

def replyToTweetWithSex(sex, status):
    if debug == 0:
        tweetMessage = f"@{status.user.screen_name} haha {sex} like the sex"
    else:
        tweetMessage = f"haha {sex} like the sex"

    print(tweetMessage)
    if debug == 0:
        api.update_status(tweetMessage, in_reply_to_status_id=status.id)

def mainReply(status, tweetChance, followingList):
    wordsList = getWords()

    nonoWords = wordsList.nonoWordsW
    sexWords = wordsList.sexWordsW
    verbs = wordsList.verbsW
    farts = wordsList.fartsW

    mode = 0
    mode1len = 0
    words = []
    mentions = 0

    for string in nonoWords:
        if findWord(string, status.text):
            print('serious/vent/upset tweet or retweet detected - not replying')
            mode -= 1
            break

    if debug == 0:

        if random.randint(1,tweetChance) > 1: # don't spam
            print(f'1 in {tweetChance} chance NOT met')
            mode -= 1
        else:
            print(f'1 in {tweetChance} chance met')

            mentions = status.text.count('@')

            if not mentions == 0:
                for string in followingList:
                    if findWord(f'@{api.get_user(string).screen_name}', status.text): # decrement if it finds any followed accounts
                        mentions -= 1

                if not str(status.user.id) in followingList:
                    print('cannot reply to accounts not followed')
                    mode -= 1
                
                if mentions > 0: # should be zero if all accounts mentioned are followed
                    print('cannot reply to tweets mentioning unfollowed accouunts')
                    mode -= 1

        if status.user.screen_name == 'braapbot':
            print('cannot reply to self')
            mode -= 1

    if not mode == -1:
        for string in sexWords:
            if findWord(string, status.text):
                words.append(string)
                mode1len += 1
        if not words == []:
            mode += 1

    if not mode == -1:
        for string in verbs:
            if findWord(string, status.text):
                words.append(string)
        if not words == []:
            mode += 2

    tweet(mode,mode1len,words,status,farts)
    print(mode)

if debug == 0:
    followingList = [] 

    for user in tweepy.Cursor(api.friends, screen_name="braapbot").items():
        followingList.append(str(user.id))

    print(followingList)

    class MyStreamListener(tweepy.StreamListener):
        def on_status(self,status):
            print(status.text)

            mainReply(status, tweetChance, followingList)
        
        def on_error(self,status_code):
            log = open("log.txt", "at")
            log.write(f"error {status_code} on {str(datetime.now())}\n") # log so i can have an idea of what happened and when
            log.close()
            return False

    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

    myStream.filter(follow=followingList)

else:
    class Dstatus:
        text = debugText

    mainReply(Dstatus, 0, 0)