import base64

import requests
import tempfile
from requests_oauthlib import OAuth1


class TwitterBot(object):
    def __init__(self, consumer_key, consumer_secret, oauth_token, oauth_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        self.oauth = self.get_oauth()

    def get_oauth(self):
        oauth = OAuth1(
            self.consumer_key,
            client_secret=self.consumer_secret,
            resource_owner_key=self.oauth_token,
            resource_owner_secret=self.oauth_token_secret,
        )
        return oauth

    def send_tweet(self, message):
        payload = {'status': message}
        url = 'https://api.twitter.com/1.1/statuses/update.json'
        res = requests.post(url=url, auth=self.oauth, params=payload)
        return res.json()

    def tweet_with_photo(self, message, photo_base64):
        image_encoded = photo_base64.encode('utf-8')

        image_bytes = base64.decodebytes(image_encoded)
        payload = {'media': image_bytes}
        url = "https://upload.twitter.com/1.1/media/upload.json"
        res = requests.post(url, auth=self.oauth, files=payload)

        media_id = res.json()['media_id']

        payload = {'status': message, 'media_ids': [media_id]}
        url = 'https://api.twitter.com/1.1/statuses/update.json'
        res = requests.post(url=url, auth=self.oauth, params=payload)
        return res.json()
