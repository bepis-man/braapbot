# BRAAP Bot

[BRAAP Bot](https://twitter.com/braapbot) is a fun little Twitter bot I wrote to reply to tweets based on their contents, like so:

`{verb} THIS! BRAAP` (with some variation)

Note: it also requires keys.txt in the script's directory if you intend to actually post to twitter. For security reasons I've not included it in here, but it's formatted as:

```html (not actually it just needs to not be coloured)
API_KEY {api key}
API_KEY_SECRET {api secret}
ACCESS_TOKEN {access token}
ACCESS_TOKEN_SECRET {acces secret}
BEARER_TOKEN {bearer token}
```

The labels don't have to be exactly as shown, but are required to be a single word and in that order. You could also not include the bearer token, since it's never used or even set in this script.

## Requirements

Not sure why you'd want or need to run this, but in order to use it you need [Tweepy](https://www.tweepy.org), which you can install using pip:

```html
pip install tweepy
```

## Debug mode

Debug mode is activated whenever there is more than 1 argument (script name included) and essentially ignores all code relating to Twitter API and Tweepy, and only outputs what would be tweeted based on the input.

For example:

```html
python3 bot.py "test input"
```

would output something like:

```html
test output
test THIS! *BRAPS*
2
```

whereas:

```html
python3 bot.py
```

would run everything and communicate to Twitter, outputting `Authentication OK` and a stream of tweets.
