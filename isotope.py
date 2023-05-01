#!/usr/bin/env python3
import argparse as argp
import scrap_utils as utils
from bs4 import BeautifulSoup as soup

'''
Isotope will be a utility for law enforcement and cybersecurity analysts who need to retrieve data from different websites. 
Rather than building scraping tools for each site, Isotope will be an all-in-one utility that 
abstracts most of the work and focuses on the actual data.

## TODO


### CLI 

- Handle URL input
- HREF Enumeration
- HTTP Header extraction

### GUI

- Translate CLI functions to display fields
- Buttons to search by HTML attribute (p, img, href)
- Search field for phrases and text
- Add items to a docx report
- docx preview window


One concern is that some sites will require cookies / tokens so there could be a 
snapshot utility included that lets you manually go to a page and then it pulls all the data. 

Selenium would be good for this.
'''

version = "0.0.1"
ISO_COMMANDS = ["help", "find", "generate", "add", "preview", "show", "swap", "dump"]
ISO_HELP = {
    "help": "This displays all commands.",
    "find": "Usage: find [target].\nSearches current page for a phrase or tag.",
    "show": "Usage: show.\nShows the current webpage and lists other pages.",
    "swap": "Usage: swap [page number].\nSwaps you to a new webpage.",
    "add": "Usage: add [command][target].\nAdds the output of a command to the report.",
    "preview": "Previews the report.",
    "dump": "Dumps the contents of the current page.",
    "generate": "Generates a report and closes the program."
}


def print_out(values):
    for val in values:
        print(val)


def print_help(command):
    print(ISO_HELP[command])


def find(html, target):
    matches = []
    for hit in html.findAll(target):
        matches.append(hit)

    # Quick way to see if they search for tag
    # or keyword
    if len(matches) == 0:
        hits = html.find(text=lambda text: text and target in text)
        return hits
    else:
        return matches


def dump():
    print_out(current)


def crawl():
    # Crawl the website looking for links.
    for link in current.findAll("a"):
        websites.append(link.get("href"))
    for link in current.find_all("link"):
        if link not in websites:
            websites.append(link.get("href"))

## TODO add way to add links from a new url / recursive pages
def show():
    # If we did not check every link at the start, do so now.
    if len(websites) == 0:
        crawl()

    for i, v in enumerate(websites):
        print(f"{i+1}{v}")


def swap(site_number):
    # Makes sure we swap to a real site and dob't have index errors.
    try:
        current = websites[site_number - 1]
    except:
        print("Page number not recognized. Type 'show' to view all pages.")


def handle_input(html):
    # Show current page in input?
    try:
        command = input("isotope> ")
        if command == "help":
            print(f"Commands are: {ISO_COMMANDS}")
        elif command[0:4] == "help":
            # Starting from 5 because of space.
            if command[5:] in ISO_COMMANDS:
                print_help(command[5:])
            else:
                print("Command not recognized. Type 'help' to view all commands and help [command] to learn more.")
        elif command[0:4] == "find":
            # Find a phase on webpage
            results = find(html, command[5:])
            print(results)
        elif command[0:4] == "show":
            # Shows all available pages
            show()
        elif command[0:4] == "dump":
            # Dumps content
            dump()
        elif command[0:4] == "swap":
            # Swap to a different page
            swap(int(command[5:]))
        elif command[0:3] == "add":
            # TODO figure out how to take a command from add and put it on doc object
            # document.add(output)
            tmp = command[4:]
        elif command[0:8] == "generate":
            #Generates a report
            return True
        else:
            print("Incorrect command! Type 'help' to view all commands and help [command] to learn more.")
    except IndexError:
        utils.log_error("No second argument entered!")



if __name__ == "__main__":
    parser = argp.ArgumentParser(description='Isotope is a utility for web scraping.')
    parser.add_argument('url', help="The URL we scrape.")
    parser.add_argument('-attr', default="None", help="An attribute to scan for.")
    parser.add_argument('-e', action="store_true", default=False, help="HREF Enumeration")
    args = parser.parse_args()

    # Make sure url is formatted properly

    html_resp = utils.simple_get(args.url)
    html_page = utils.soupify(html_resp)
    global websites
    global current
    global document
    document = utils.Document
    current = html_page
    websites = []
    print(args)
    if args.attr is not None:
        # Print out anything that matches our attribute
        print("bop")
        page_matches = utils.grab_attribute( current, args.attr)
        print_out(page_matches)

    if args.e:
        # Crawl all hrefs found.
        crawl()
        #print_out(websites)

    # Could add a main menu once args are parsed
    # Asking what they want to do with the data
    # View pages, extract data, etc
    # - cache all pages
    # - output formatting in scrap_utils
    # - docx handling
    print(f"Welcome to Isotope {version}")
    print(f"What would you like to do with {args.url}?\n")
    while True:
        track = handle_input(current)
        if track is not None:
            break
    print("Isotope. Written by IronCityCoder.")


"""
Could turn this into a full on query language.
FIND [target] WHERE [conditions]
"""
