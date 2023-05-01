"""
Utility library for Isotope
Handles functions for web-scraping
Code is expanded from
https://realpython.com/python-web-scraping-practical-introduction/
"""
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup as soup
import sys
import socket
from contextlib import closing

def soupify(request):
    return soup(request, 'html.parser')

def valid_response(response):
    """
    Goes through the response to determine if we received HTML.
    :param response:
    :return: boolean
    """
    content_type = response.headers['Content-Type'].lower()
    if response.status_code == 200:
        if content_type is not None:
            if content_type.find("html") > -1:
                return True
    return False


def grab_attribute(html_page, attribute):
    """
    Looks through a HTML page for desired tags.
    Checks for proper formatting.
    :param html_page:
    :param attribute:
    :return:
    """
    try:
        if hasattr(html_page, 'title'):
            pass
        elif hasattr(html_page, "status_code"):
            html_page = soupify(html_page)
        else:
            response = simple_get(html_page)
            if response is not None:
                html_page = soupify(response)
            else:
                raise Exception(f"Response for {html_page} is None!")
        matches = set()
        for attr in html_page.select(attribute):
            matches.add(attr)
        return list(matches)
    # Add specific exceptions.
    except:
        log_error(f"{html_page} could not be parsed!")


def simple_get(url):
    """
    Attempts to retrieve our url through HTTP.
    """
    try:
        with closing(requests.get(url, stream=True)) as response:
            if valid_response(response):
                return response.content
            else:
                return None

    except RequestException as err:
        log_error(f'Error during requests to {url}: {err}')


def log_error(err):
    """
    Made as a function for future extendability.
    :param err:
    :return:
    """
    print(err)


# https://www.quora.com/How-can-I-write-a-string-to-a-docx-file-in-Python
# put method for creating documents here
class Document:
    def __init__(self):
        self.sections = []

    def update_sections(self, index, content):
        """
        Updates a section with new content.
        :param index: int
        :param content: string
        :return:
        """
        try:
            self.sections[index] = content
        except IndexError as err:
            print(f"{err}")

    def add(self, content):
        """
        Adds section to end of content.
        :param content:
        :return:
        """
        self.sections.append(content)

    def add_section(self, location, content):
        """
        Adds a section a specific location.
        :param location: int
        :param content: string
        :return:
        """
        clone = self.sections[:location]
        clone[location] = content
        for i, v in enumerate(self.sections[location:]):
            clone.append(v)
        self.sections = clone

    # add way to move section?

    def preview(self):
        """
        Add actual preview window later.
        :return:
        """
        for pos, section in enumerate(self.sections):
            print(f"Line {pos}: \n{section}")
