from py_wikiracer.internet import Internet
from typing import List
import re
import heapq

class Parser:

    @staticmethod
    def get_links_in_page(html: str) -> List[str]:
        """
        In this method, we should parse a page's HTML and return a list of links in the page.
        Be sure not to return any link with a DISALLOWED character.
        All links should be of the form "/wiki/<page name>", as to not follow external links
        """
        links = []
        disallowed = Internet.DISALLOWED

        # YOUR CODE HERE
        # You can look into using regex, or just use Python's find methods to find the <a> tags or any other identifiable features
        # A good starting place is to print out `html` and look for patterns before/after the links that you can string.find().
        # Make sure your list doesn't have duplicates. Return the list in the same order as they appear in the HTML.
        # This function will be stress tested so make it efficient!

        wiki_link_pattern = re.compile(
            r"""
                <a # Start of anchor tag
                .*? # Account for any attributes and spaces in between
                href=" # Start of href
                (?P<url>/wiki/[^"{disallowed_chars}]*?) # Main wikilink page
                " # End of href
            """.format(
                disallowed_chars="".join(disallowed)
            ),
            re.VERBOSE,
        )

        links = wiki_link_pattern.findall(html)
        unique_links = []  # Need this list to pass tests

        for link in links:
            if link not in unique_links:
                unique_links.append(link)

        return unique_links


# In these methods, we are given a source page and a goal page, and we should return
#  the shortest path between the two pages. Be careful! Wikipedia is very large.

class DijkstrasProblem:
    def __init__(self):
        self.internet = Internet()
        self.parser = Parser()
    # Links should be inserted into the heap as they are located in the page.
    # By default, the cost of going to a link is the length of a particular destination link's name. For instance,
    #  if we consider /wiki/a -> /wiki/ab, then the default cost function will have a value of 8.
    # This cost function is overridable and your implementation will be tested on different cost functions. Use costFn(node1, node2)
    #  to get the cost of a particular edge.
    # You should return the path from source to goal that minimizes the total cost. Assume cost > 0 for all edges.
    def dijkstras(
        self,
        source="/wiki/Calvin_Li",
        goal="/wiki/Wikipedia",
        costFn=lambda x, y: len(y),
    ):
        path = []
        distances = {source: 0}
        priority_queue = [(0, source)]  # (distance, link)

        # Dictionary to store the predecessor of each link
        predecessors = {source: None}

        while priority_queue:
            current_distance, current_link = heapq.heappop(priority_queue)

            # If the extracted distance is greater than the known shortest, skip
            if current_distance > distances[current_link]:
                continue

            current_link_html = self.internet.get_page(current_link)
            neighbor_links = self.parser.get_links_in_page(current_link_html)

            for neighbor_link in neighbor_links:
                if neighbor_link not in distances:
                    distances[neighbor_link] = float("infinity")
                    predecessors[neighbor_link] = None

                weight = costFn(current_link, neighbor_link)
                distance = current_distance + weight

                # If a shorter path to the neighbor is found, update and push to queue
                if distance < distances[neighbor_link]:
                    distances[neighbor_link] = distance
                    predecessors[neighbor_link] = current_link
                    heapq.heappush(priority_queue, (distance, neighbor_link))

            # If we reached the target, reconstruct and return the path
            if goal in neighbor_links:
                neighbor_link = goal
                while neighbor_link is not None:
                    path.insert(0, neighbor_link)
                    neighbor_link = predecessors[neighbor_link]

                if source == goal:
                    path.append(goal)
                return path
        
        # If the loop finishes without finding the goal
        return None

class WikiracerProblem:
    def __init__(self):
        self.internet = Internet()

    # Time for you to have fun! Using what you know, try to efficiently find the shortest path between two wikipedia pages.
    # Your only goal here is to minimize the total amount of pages downloaded from the Internet, as that is the dominating time-consuming action.

    # Your answer doesn't have to be perfect by any means, but we want to see some creative ideas.
    # One possible starting place is to get the links in `goal`, and then search for any of those from the source page, hoping that those pages lead back to goal.

    # Note: a Dijkstra implementation with no optimizations will not get credit, and it will suck.
    # You may find Internet.get_random() useful, or you may not.

    def wikiracer(self, source = "/wiki/Calvin_Li", goal = "/wiki/Wikipedia"):
        path = [source]
        # YOUR CODE HERE
        # ...
        path.append(goal)
        return path # if no path exists, return None
