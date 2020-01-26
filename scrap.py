import json
import requests
from bs4 import BeautifulSoup
from pprint import pprint


class InstagramScraper(object):

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                          'AppleWebKit/537.11 (KHTML, like Gecko) '
                          'Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }
        self.discovered_hashtags = set()
        self.already_checked = set()

    def __request_url(self, link):
        try:
            response = requests.get(
                link,
                timeout=4,
                headers=self.headers,
            ).text
        except requests.HTTPError:
            raise requests.HTTPError(
                'Received non 200 status code from Instagram')
        except requests.RequestException:
            raise requests.RequestException
        else:
            return response

    @staticmethod
    def extract_json_data(html):
        soup = BeautifulSoup(html, 'html.parser')
        body = soup.find('body')
        script_tag = body.find('script')
        raw_string = script_tag.text.strip().replace(
            'window._sharedData =', '').replace(';', '')
        return json.loads(raw_string)

    def get_current_profile_info(self, username):
        try:
            link = f"https://www.instagram.com/{username}/"
            response = self.__request_url(link)
            json_data = self.extract_json_data(response)
        except Exception as e:
            raise e
        else:
            profile_page_metrics = self.profile_page_metrics(json_data)
            profile_page_recent_posts = self.profile_page_recent_posts(json_data)
            # taken_at_timestamp
            # >> > from datetime import datetime
            # >> > datetime.fromtimestamp(1172969203.1)
            # datetime.datetime(2007, 3, 4, 0, 46, 43, 100000)
        # return info and add it to api in another function

    def profile_page_metrics(self, json_data_from_profile):
        results = {}
        metrics = json_data_from_profile['entry_data']['ProfilePage'][0]['graphql']['user']
        for key, value in metrics.items():
            if key != 'edge_owner_to_timeline_media':
                if value and isinstance(value, dict):
                    value = value['count']
                    results[key] = value
                elif value:
                    results[key] = value
        return results

    def profile_page_recent_posts(self, json_data_from_profile):
        results = []
        metrics = \
        json_data_from_profile['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media'][
            "edges"]
        for node in metrics:
            node = node.get('node')
            if node and isinstance(node, dict):
                results.append(node)
        return results

    def discover_posts(self, hashtag):
        # get id to posts. Then we can get posts and their accounts.
        results = []
        try:
            response = self.__request_url(f"https://www.instagram.com/explore/tags/{hashtag}/")
            json_data = self.extract_json_data(response)
            metrics = json_data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_top_posts'][
                "edges"]
        except Exception as e:
            raise e
        else:
            for node in metrics:
                node = node.get('node')
                if node and isinstance(node, dict):
                    results.append(node['shortcode'])
        return results

    def get_account_name_from_post(self, post_id):
        try:
            response = self.__request_url(f"https://www.instagram.com/p/{post_id}/")
            json_data = self.extract_json_data(response)
            username = json_data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['owner']['username']
            return username
        except Exception as e:
            raise e

    def __get_connected_hashtags(self, current_hashtag):
        results = []
        try:
            response = self.__request_url(f"https://www.instagram.com/explore/tags/{current_hashtag}/")
            json_data = self.extract_json_data(response)
            metrics = json_data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_related_tags'][
                "edges"]
        except Exception as e:
            raise e
        else:
            for node in metrics:
                node = node.get('node')
                if node and isinstance(node, dict):
                    results.append(node['name'])
        return results

    def get_category_hashtags(self, current_hashtag, deepth):
        if deepth == 0:
            return
        if current_hashtag not in self.already_checked:
            new_hashtags = self.__get_connected_hashtags(current_hashtag)
            self.discovered_hashtags.update(new_hashtags)
            for hashtag in new_hashtags:
                self.get_category_hashtags(hashtag, deepth - 1)
                self.already_checked.update(hashtag)

    def discover_hashtags(self, firsthashtag):
        self.discovered_hashtags = set()
        self.already_checked = set()
        self.get_category_hashtags(firsthashtag, 2)
        new_hashtags = list(self.discovered_hashtags)
        return new_hashtags


# x = InstagramScraper()
# print(x.discover_hashtags('coding'))
# x.get_current_profile_info('jakobowsky')
# print(x.discover_hashtags('coding'))
# x.__get_connected_hashtags('coding')
# print(x.get_connected_hashtags('coding'))
# m1 = x.get_account_name_from_post('')
