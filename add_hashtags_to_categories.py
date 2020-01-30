from scrap import InstagramScraper
import requests
import time


class HashtagScript:

    def __init__(self, category, basic_hashtags):
        self.scraper = InstagramScraper()
        self.base_url = 'http://127.0.0.1:8000/api/'
        self.category = category.title()
        self.basic_hashtags = basic_hashtags
        self.headers = {'Content-type': 'application/json', 'Accept': '*/*'}

    def __call__(self, *args, **kwargs):
        self.add_category_to_db()

    def check_current_hashtags(self):
        links_to_hashtags = f'{self.base_url}hashtags?category__name={self.category}'
        try:
            response = requests.get(links_to_hashtags).json()
            return response
        except Exception as e:
            print("ERROR: ", e)

    def check_amount_current_hashtags(self):
        return len(self.check_current_hashtags())

    def find_new_hashtags(self):
        print('finding new hastags')
        all_hashtags = set(self.basic_hashtags)
        for hashtag in self.basic_hashtags:
            time.sleep(2)
            print("Looking for related hashtags to: ", hashtag)
            related_hashtags = self.scraper.discover_hashtags(hashtag)
            all_hashtags.update(related_hashtags)
        print('all hashtags: ', all_hashtags)
        return all_hashtags

    def add_new_hashtags_to_db(self, category_id):
        hashtags = self.find_new_hashtags()
        link_to_adding_hashtag = f'{self.base_url}add_multi_hashtags/'
        body = {
            "category_id": int(category_id),
            "hashtags": list(hashtags)
        }
        r = requests.post(link_to_adding_hashtag, json=body, headers=self.headers)
        if r.status_code == 200:
            return True
        else:
            return False

    def __add_category(self):
        link_to_category = f'{self.base_url}categories'
        body = {
            "name": f"{self.category.title()}"
        }
        r = requests.post(link_to_category, json=body, headers=self.headers)
        if r.status_code == 201:  # created
            print("Added new category to db: ", r.json())
            return True
        else:
            print("Smth went wrong: ", r.json())
            raise

    def add_category_to_db(self):
        link_to_category = f'{self.base_url}categories?name={self.category}'
        try:
            response = requests.get(link_to_category).json()
            category_id = None
            category_name = None
            if response:
                # check if db is not empty
                category_id = response[0].get('id')
                category_name = response[0].get('name').title()
            if category_name == self.category:
                print("This category is already in db.")
                amount_of_hashtags = self.check_amount_current_hashtags()
                print(f'It has {amount_of_hashtags} hashtags.')
                if amount_of_hashtags < 10:  # not sure about this
                    if self.add_new_hashtags_to_db(category_id):
                        print("Success")
                    else:
                        print("Smth went wrong with adding hashtags to db")
            else:
                print("This category is not in db. Adding and finding hashtags.")
                if self.__add_category():
                    response = requests.get(link_to_category).json()
                    print(response)
                    category_id = response[0].get('id')
                    if self.add_new_hashtags_to_db(category_id):
                        print("Success")
                    else:
                        print("Smth went wrong with adding hashtags to db")

        except Exception as e:
            print("ERROR: ", e)


if __name__ == '__main__':
    print("Script is not active now")

    # new_category = "Technology"
    # basic_hashtags = ['tech', 'coding', 'robotics']
    # script = HashtagScript(new_category, basic_hashtags)
    # script()
