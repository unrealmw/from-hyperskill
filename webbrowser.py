import argparse
import os
from collections import deque
import requests
from bs4 import BeautifulSoup
from colorama import Fore


class WebBrowser:
    def __init__(self, path):
        self.path = path
        self.history = deque()
        self.site = None
        self.clear_content = None

    def folder_creator(self):
        if not os.access(self.path, os.F_OK):
            os.mkdir(self.path)

    def write_file(self):
        file_name = self.site.lstrip("https://").split(".")[0]
        file_path = os.path.join(self.path, file_name)
        with open(file_path, "w") as w_file:
            w_file.write(self.clear_content)

    def site_checker(self, site):
        try:
            if "https://" not in site:
                site = "https://" + site
            r = requests.get(site)
            if r.status_code == 200:
                self.site = site
                return True
        except requests.exceptions.ConnectionError:
            print("Invalid URL")

    def get_content(self):
        r = requests.get(self.site)
        soup = BeautifulSoup(r.content, "html.parser")
        for i in soup.find_all("a"):
            i.string = "".join([Fore.BLUE, i.get_text(), Fore.RESET])
        content = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li'])
        self.clear_content = "\n".join([i.get_text(" ", strip=True) for i in content]).strip()
        return self.clear_content


def main():
    parser = argparse.ArgumentParser(description="This program downloads sites and puts it to the folder.")
    parser.add_argument("directory", type=str, help="Directory where your files will be saved.")
    args = parser.parse_args()
    directory = args.directory

    a = WebBrowser(directory)
    a.folder_creator()
    while True:
        site = input()
        if site == "exit":
            break
        elif site == "back" and len(a.history) == 0:
            continue
        elif site == "back" and len(a.history) > 0:
            a.history.pop()
            print(a.history[-1])
        elif a.site_checker(site):
            a.get_content()
            print(a.clear_content)
            a.write_file()


if __name__ == '__main__':
    main()
