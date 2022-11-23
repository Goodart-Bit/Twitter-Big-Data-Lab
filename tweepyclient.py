import tweepy

class TweepyClient():
    def authenticateV2(self):
        # Twitter AUTH V2 Token
        # API V2 app-only (BEARER) || works for AuthV1 too with API Keys
        return tweepy.Client(bearer_token=self.bearer_token)

    def search_tweets(self, search_query, limit):
        # Tweepy Response -> Named Tuple
        response_list = tweepy.Paginator(
        self.client.search_recent_tweets, search_query, max_results=100, tweet_fields=['context_annotations'])
        return response_list.flatten(limit=limit)  # tweet object list

    def get_a_tweet(self, id):
        # Tweepy Response -> Named Tuple BUT we only need 1 value
        self.client.get_tweet(id)[0]
        self.client.get_liked_tweets()

    def __init__(self, bearer_token):
        self.bearer_token = bearer_token
        self.client = self.authenticateV2()