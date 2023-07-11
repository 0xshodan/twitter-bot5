import tweepy

client = tweepy.OAuth2UserHandler(client_secret="18a72d152b031b215d326cd52fdd33d626a2eeea:2023.06.09|5")
client.get_bookmarks()