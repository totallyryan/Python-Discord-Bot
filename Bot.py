import requests
import time
import sys
import os
os.system("color 1e")
 
class RobloxBot:
    """A simple Roblox bot class"""
    def __init__(self, group_id):
        # creates a session
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0'}
        self.session = requests.session()
        self.session.headers.update(self.headers)
        # sets group id
        self.group_id = group_id
        # checks if program is able to connect
        if requests.get('https://pastebin.com/raw/iRDJv57z').text != 'OK':
            sys.exit('Unable to connect')
 
    def login(self, username, password):
        print('Logging In...')
        # logs into Roblox with the provided username and password
        payload = {'username': username, 'password': password}
        self.session.post('https://www.roblox.com/newlogin', data=payload)
        print('Successfully Logged In.')
 
    def get_shirts(self, starting_page='1', category='12', wait=30):
        page_num = starting_page
        while page_num < 999999:
            # gets asset ids of shirts
            params = {'CatalogContext': 66, 'Subcategory': category, 'SortAggregation': '5', 'LegendExpanded': 'true', 'Category': '3', 'PageNumber': page_num}
            try:
                r = self.session.get('https://www.roblox.com/catalog/json', params=params)
                r.raise_for_status()
            except requests.exceptions.HTTPError:
                print('Status Error: {}'.format(r.status_code))
                time.sleep(30)
                continue
            print('Got items from page: {}'.format(page_num))
            # iterates through json and grabs asset ids from page
            for asset in r.json():
                # calls download with the asset id
                while True:
                    try:
                        self.__download(asset['AssetId'])
                        break
                    except:
                        print('Found an error. Retrying.')
                        continue
                time.sleep(wait)
            page_num += 1
 
    def __download(self, assetId):
        # gets name, description, price and file
        data = self.session.get('https://api.roblox.com/Marketplace/ProductInfo', params={'assetId': assetId}).json()
        name, description, price, asset_type = data['Name'], data['Description'], data['PriceInRobux'], data['AssetTypeId']
        # gets templates asset id
        count = 0
        while count < 10:
            assetId -= 1
            try:
                r = self.session.get('https://api.roblox.com/Marketplace/ProductInfo', params={'assetId': assetId})
                count += 1
                r.raise_for_status()
                if r.json()['Name'] == name:
                    print('Got template id for: {}'.format(assetId))
                    r1 = requests.post("discord webhook", data={'content': assetId})
                    break
            except (requests.exceptions.HTTPError, ValueError):
                print('Could not find template for: {}'.format(assetId))
                return
        else:
            print('Could not find template for: {}'.format(assetId))
            return
 
if __name__ == '__main__':
    # instantiates RobloxBot
    bot = RobloxBot(group_id='3357233')
    # logs into Roblox
    bot.login(username='username', password='password')
    # starts collecting shirts on page one with a wait time of 10 seconds
    bot.get_shirts(starting_page=5, category='12', wait=5)