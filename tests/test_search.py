import random
import sys
from typing import Callable, Iterator
from itertools import chain, combinations
from collections import defaultdict
from types import ModuleType
from importlib import reload
from urllib.request import urlopen

import pytest
from py_wikiracer.internet import Internet
from py_wikiracer.wikiracer import Parser, DijkstrasProblem, WikiracerProblem

REQ_LIMIT = 75 # per test, normally


def test_parser():
    internet = Internet()
    html = internet.get_page("/wiki/Henry_Krumrey")
    assert Parser.get_links_in_page(html) == ['/wiki/Main_Page',
                                             '/wiki/Henry_Krumrey',
                                             '/wiki/Wisconsin_State_Senate',
                                             '/wiki/Wisconsin_Senate,_District_20',
                                             '/wiki/Wisconsin_State_Assembly',
                                             '/wiki/Plymouth,_Sheboygan_County,_Wisconsin',
                                             '/wiki/Republican_Party_(United_States)',
                                             '/wiki/Sheboygan_County,_Wisconsin',
                                             '/wiki/United_States_presidential_election_in_Wisconsin,_1900',
                                             '/wiki/Farmers%27_suicides_in_the_United_States',
                                             '/wiki/Crystal_Lake,_Illinois']


def test_trivial():
    """
    All pages contain a link to themselves, which any search algorithm should recognize.
    """
    dij = DijkstrasProblem()

    assert dij.dijkstras(source = "/wiki/ASDF", goal = "/wiki/ASDF") == ["/wiki/ASDF", "/wiki/ASDF"]
    assert dij.internet.requests == ["/wiki/ASDF"]


def test_trivial_2():
    """
    Searches going to page 1 distance away.
    """
    dij = DijkstrasProblem()

    assert dij.dijkstras(source = "/wiki/Reese_Witherspoon", goal = "/wiki/Academy_Awards") == ["/wiki/Reese_Witherspoon", "/wiki/Academy_Awards"]
    assert dij.internet.requests == ["/wiki/Reese_Witherspoon"]


def test_dijkstras_basic():
    """
    DFS depth 2 search
    """
    dij = DijkstrasProblem()
    # This costFn is to make sure there are never any ties coming out of the heap, since the default costFn produces ties and we don't define a tiebreaking mechanism for priorities
    assert dij.dijkstras(source = "/wiki/Calvin_Li", goal = "/wiki/Wikipedia", costFn = lambda y, x: len(x) * 1000 + x.count("a") * 100  + x.count("u") + x.count("h") * 5 - x.count("F")) == ['/wiki/Calvin_Li', '/wiki/Main_Page', '/wiki/Wikipedia']
    assert dij.internet.requests == ['/wiki/Calvin_Li',
                                     '/wiki/Weibo',
                                     '/wiki/Hubei',
                                     '/wiki/Wuxia',
                                     '/wiki/Wuhan',
                                     '/wiki/Pinyin',
                                     '/wiki/Tencent',
                                     '/wiki/Wu_Yong',
                                     '/wiki/Cao_Cao',
                                     '/wiki/John_Woo',
                                     '/wiki/Kelly_Lin',
                                     '/wiki/Sina_Corp',
                                     '/wiki/Huo_Siyan',
                                     '/wiki/Shawn_Yue',
                                     '/wiki/Main_Page']

class CustomInternet():
    def __init__(self):
        self.requests = []
    def get_page(self, page):
        self.requests.append(page)
        return f'<a href="{page}"></a>'


def test_none_on_fail():
    """
    Program should return None on failure
    """
    dij = DijkstrasProblem()

    # Testing hack: override the internet to inject our own HTML
    dij.internet = CustomInternet()

    assert dij.dijkstras(source = "/wiki/Calvin_Li", goal = "/wiki/Wikipedia") == None
    assert dij.internet.requests == ["/wiki/Calvin_Li"]


def test_wikiracer_1():
    """
    Tests wikiracer speed on one input.
    A great implementation can do this in less than 8 internet requests.
    A good implementation can do this in less than 15 internet requests.
    A mediocre implementation can do this in less than 30 internet requests.

    To make your own test cases like this, I recommend finding a starting page,
    clicking on a few links, and then seeing if your program can get from your
    start to your end in only a few downloads.
    """
    limit = 15

    racer = WikiracerProblem()
    racer.wikiracer(source="/wiki/Computer_science", goal="/wiki/Richard_Soley")
    assert len(racer.internet.requests) <= limit


def test_wikiracer_2():
    """
    Tests wikiracer speed on one input.
    A great implementation can do this in less than 25 internet requests.
    A good implementation can do this in less than 80 internet requests.
    A mediocre implementation can do this in less than 300 internet requests.
    """
    limit = 80

    racer = WikiracerProblem()
    racer.wikiracer(source="/wiki/Waakirchen", goal="/wiki/A")
    assert len(racer.internet.requests) <= limit


def test_wikiracer_multiple():
    '''
    Tests wikiracer on multiple websites.
    Does a combination of all links and calls wikiracer to tests those combinations.
    This also tests that the path between pages is actually navigable
    Beware: This function test take long time to run. You can change to a smaller list to verify
    that your algorithm works.
    The default test takes around 5-10 minutes when the pages are not cached.
    '''
    pages = ['Jesus', 'Adolf_Hitler', 'Michael_Jordan', 'United_Nations', 'Kobe_Bryant', 'Brazil']

    allCombinations = list(combinations(pages, 2))
    paths = []
    with open("../results.txt", "w") as results:
        for combination in allCombinations:
            racer = WikiracerProblem()
            paths.append(racer.wikiracer(source=r'/wiki/' + combination[0], goal=r'/wiki/' + combination[1]))
            results.write(f"{combination} {len(racer.internet.requests)}\n")

        for i, path in enumerate(paths):
            results.write(f"\n####### {i} #######\n")
            source = path.pop(0)
            results.write(f"{source}\n")
            while len(path) > 0:
                destination = path.pop(0)
                results.write(f"{destination}\n")
                links = Parser.get_links_in_page(Internet().get_page(source))
                assert destination in links
                source = destination
            results.write(f"#################\n")
