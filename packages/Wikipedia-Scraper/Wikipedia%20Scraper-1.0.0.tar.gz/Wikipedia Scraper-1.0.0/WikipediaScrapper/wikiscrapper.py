# wikipedia module is easier to use but can scrape only wikipedia
# import wikipedia
# title = input("Wikipedia Search: ")
# search = wikipedia.WikipediaPage(title=title)
# # print(search.content)
# print(search.links)

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import wikipedia


class WikiScrapper(object):

    def __init__(self, search):
        self.search = search.lower()
        try:
            _source = urlopen("https://en.wikipedia.org/wiki/{}".format(search)).read()
        except:
            for i in wikipedia.search(search):
                print(f"- {i}")
            print("Choose the relevant one.")
            exit(0)

        self.soup = BeautifulSoup(_source, "lxml")
        self.head = ""
        self.wiki = {}
        self.processing()

    @staticmethod
    def case(tag):
        return (tag.name[0] == 'h' or
                tag.name == 'p' and not tag.has_attr('class') or
                tag.name == 'li')

    def processing(self):
        h1 = 0
        h2 = 0
        h3 = 0

        wiki = {}

        head1 = ""
        head2 = ""
        head3 = ""

        for i in self.soup.find_all(self.case):
            try:
                if i.name == "h1":
                    head1 = i.text.lower()
                    self.head = head1
                    wiki[head1] = {0: ""}
                    h1 = 1
                elif i.name == "h2":
                    h1 = 0
                    h2 = 1
                    h3 = 0
                    head2 = i.contents[0].string.lower()
                    wiki[head1][head2] = {0: ""}
                elif i.name == "h3":
                    h2 = 0
                    h3 = 1
                    head3 = i.contents[0].string.lower()
                    wiki[head1][head2][head3] = ""
                elif i.name == 'p' or i.name[1] not in '123':
                    if h1 == 1 and i.text:
                        wiki[head1][0] += re.sub("\[[A-Z0-9a-z/]+]", "", i.text)
                    elif h2 == 1 and i.text:
                        wiki[head1][head2][0] += re.sub("\[[A-Z0-9a-z/]+]", "", i.text)
                    elif h3 == 1 and i.text:
                        wiki[head1][head2][head3] += re.sub("\[[A-Z0-9a-z/]+]", "", i.text)
            except (KeyError, AttributeError):
                pass
        self.wiki = wiki

    def sections(self) -> list:
        sec = [i.capitalize() for i in self.wiki[self.head].keys() if not i == 0]
        sec.insert(0, self.wiki[self.head][0])
        return sec

    def subsections(self, section) -> list:
        sec = [i.capitalize() for i in self.wiki[self.head][section].keys() if not i == 0]
        sec.insert(0, self.wiki[self.head][section][0])
        return sec

    def hyperlinks(self) -> list:  # BONUS
        hy = []
        for i in self.soup.find_all("a"):
            try:
                hy.append(i['href'])
            except KeyError:
                continue
        return hy

    def display(self, arr):
        print(arr[0])
        for i, x in enumerate(arr[1:], 1):
            print("{}. {}".format(i, x))

    def sub_display(self, sec, subsec):
        print(self.wiki[self.head][sec][subsec])

    def query(self):
        while True:
            scrapper.display(scrapper.sections())
            print("Press Enter to Exit.")
            query1 = input("Select a Section: ").lower()
            if not query1:
                exit(0)
            try:
                self.display(self.subsections(query1))
            except KeyError:
                print("Select only from the above!!")

            if len(self.subsections(query1)) == 1 and list(self.wiki[self.head][query1]) == [0]:
                print("No Subsection Found!!")
            else:
                break

        while True:
            query2 = input("Select a Subsection: ").lower()
            if not query2:
                exit(0)
            try:
                self.sub_display(query1, query2)
                break
            except KeyError:
                print("Select only from the above!!")
                self.display(self.subsections(query1))


if __name__ == "__main__":
    search = input("Wikipedia Scrape: ")
    scrapper = WikiScrapper(search)
    scrapper.display(scrapper.hyperlinks())
    print("_"*100)
    scrapper.query()