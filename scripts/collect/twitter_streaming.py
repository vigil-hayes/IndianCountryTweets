#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

#Variables that contains the user credentials to access Twitter API 
access_token = "2288788914-0iDOoqhGKxd4hK8QgAAmW7RMWSzkHVpklcFJLbu"
access_token_secret = "g4IPiEkWiae3Kz5ACB0M63BCK5yBUcgAG2aC1ja7XU61L"
consumer_key = "cpfe8RIjIwZPRJ34SCuTvIutq"
consumer_secret = "yrymUGLo04OORXzIzEkLr7oz6RQ6jXbjQClFb3H7J1jTMKOedo"

# Location filename
rez_loc_filename = "" #TODO

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status
def getRezLocations(filename):
	print filename
if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(locations=[106.41646806548069, 34.95120264470216, 106.80428683265481, 35.26988299433271, -74,40,-73,41])
