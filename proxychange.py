import requests
from bs4 import BeautifulSoup


class ProxyChanger:

    def __init__(self):
        self.proxies = self.get_proxy_list()
        self.used_proxies = set()
        self.actual_proxy = None
        self.set_new_proxy()

    def get_proxy_list(self):
        proxy_url = 'https://free-proxy-list.net/'
        soup = BeautifulSoup(requests.get(proxy_url).text, 'html.parser')
        proxies = set()
        for proxy in soup.find(id='proxylisttable').tbody.find_all('tr'):
            proxies.add(
                f"{proxy.find_all('td')[0].string}:{proxy.find_all('td')[1].string}")
        return proxies

    def try_proxy(self, proxy):
        try:
            r = requests.get('https://httpbin.org/ip',
                             proxies={"http": proxy, "https": proxy}, timeout=4)

            return r.status_code == 200
        except:
            return False

    def set_new_proxy(self):
        while True:
            proxy = self.check_proxies()
            if proxy:
                self.actual_proxy = proxy
                break
            else:
                print("Getting new list of proxies...")
                self.proxies = self.get_proxy_list()
                self.used_proxies = set()

    def check_proxies(self):
        print("Gettng new proxy")
        for proxy in self.proxies:
            if proxy not in self.used_proxies:
                if self.try_proxy(proxy):
                    print("Got new proxy: ", proxy)
                    return proxy
                else:
                    self.used_proxies.add(proxy)
                    print("Bad proxy: ", proxy)
        # if we iterate through all proxies.
        print("All proxies used.")
        return False
