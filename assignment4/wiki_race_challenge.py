"""
Bonus task
"""
from __future__ import annotations

import re

from requesting_urls import get_html
from filter_urls import find_articles

def bfs_shortest(start: str, finish: str) -> dict[str, str | None]:
    """Find the shortest paths from 'start' using the bfs algorithm.
    Terminate if 'finish' has been found.

    Arguments:
        start (str): wikipedia article URL to start from
        finish (str): wikipedia article URL to stop at

    Returns:
        parents (dict[str, str | None]):
        Dictionary of parent articles to any url
        'start' will not have a parent article
    """

    # create and compile regular expression(s)
    # check if the article is an english language wikipedia article, to make search easier
    en_pat = re.compile(r"https://en.")

    # dict to save urls with direct connection, queue to save and read urls
    parents = {start: None}
    queue = [start]

    # article htmls parsed
    i = 0
    # url count, reset after 1000
    n = 0
    while queue:
        # extract first element in queue
        curr = queue.pop(0)
        i += 1
        # get html and find urls to other articles
        curr_html = get_html(curr)
        articles = find_articles(curr_html)
        for url in articles:
            # check that article links to english wiki
            if not url in parents and en_pat.search(url):
                n += 1
                if n == 1000:
                    # print every 1000th url found
                    print(f"Articles searched: {i}, URL found: {url}")
                    n = 0
                # set currently searched url as parent to found url
                parents[url] = curr
                # add url 
                queue.append(url)
            if url == finish:
                print(f"{finish} found after searching {i} articles\n")
                return parents

    print(f"{finish} not found")
    return parents


def find_path(start: str, finish: str) -> list[str]:
    """Find the shortest path from `start` to `finish`

    Arguments:
        start (str): wikipedia article URL to start from
        finish (str): wikipedia article URL to stop at

    Returns:
        urls (list[str]):
        List of URLs representing the path from `start` to `finish`.
        The first item should be `start`.
        The last item should be `finish`.
        All items of the list should be URLs for wikipedia articles.
        Each article should have a direct link to the next article in the list.
    """
    path = []
    
    parents = bfs_shortest(start, finish)

    # if 'finish' not found
    if not finish in parents:
        return path
    
    v = finish
    # construct path between start and finish
    while v:
        path.append(v)
        v = parents[v]
    # reverse list so that start is first and finish is last
    path.reverse()

    print("Shortest path between start and finish:")
    for url in path:
        print(url)

    assert path[0] == start
    assert path[-1] == finish
    return path


if __name__ == "__main__":
    start = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    finish = "https://en.wikipedia.org/wiki/Peace"
    find_path(start, finish)
