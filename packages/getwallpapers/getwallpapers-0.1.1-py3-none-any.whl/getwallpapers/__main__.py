from getwallpapers import *
from sys import argv, exit

def main():

    """
    Main which calls all the other functions
    """

    wallpaper_url = argv[1]
    if '://getwallpapers.com/' not in wallpaper_url:
        print("Invalid URL")
        exit(0)
    else:
        soup = parse_link(wallpaper_url)
        folder_name = get_folder(soup)
        download(soup, folder_name)

if __name__ == "__main__":
    main()