#import all the libraries

import os
import re
import sys
import urllib.request as request
import bs4
from tqdm import tqdm

base_url = 'http://getwallpapers.com'

# All the function definitions

def parse_link(wallpaper_url):

    """
    Parse the url and give back the soup
    """

    url = request.urlopen(wallpaper_url)
    soup = bs4.BeautifulSoup(url, "lxml")
    return soup

def get_folder(html_data):

    """
    Get the title from the html and create a directory out of it
    """

    title = html_data.title.string
    directory = title
    path = os.path.dirname(os.path.realpath(__file__))
    final_directory = os.path.join(path, directory)
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)

    return final_directory

def download(html_data, folder_name):

    """
    Parse the soup to get the url of the image.
    """

    for url in tqdm(html_data.findAll("a", attrs={"class": "download_button"})):
        downloadable_url = url.get("href")
        final_url = request.urljoin(base_url, downloadable_url)
        get_name = re.compile(r"(?:.(?!/))+$")
        file_name = get_name.search(downloadable_url)
        file_name = file_name.group(0).rsplit("/")[1]
        fullfilename = os.path.join(folder_name, file_name)
        request.urlretrieve(final_url, fullfilename)

    return
