import requests
from bs4 import BeautifulSoup


class Crawler:
    def __init__(self, url):
        self.url = url
        self.soup = None
        self.data_new = None
        self.data_old = None

    def get_soup(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            self.soup = BeautifulSoup(response.text, 'lxml')
        else:
            raise ValueError(f'status code error: {response.status_code}')

    def find_all(self, tag, class_name=None):
        if class_name is not None:
            self.data_old = self.soup.find_all(tag, class_=class_name)
        else:
            self.data_old = self.soup.find_all(tag)

    def data_processing(self, param=None):
        self.data_new = []
        if param is not None:
            for data in self.data_old:
                try:
                    self.data_new.append(data.attrs[param])
                except KeyError:
                    continue
        else:
            for data in self.data_old:
                self.data_new.append(data.text)
