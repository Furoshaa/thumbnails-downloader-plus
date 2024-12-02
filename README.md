# Thumbnail Downloader Plus for Retroarch

This Python script is designed to quickly download thumbnails for RetroArch. It automates the process of checking for missing thumbnails and provides multiple options for the user to choose from when downloading missing thumbnails from the [Libretro Thumbnails](https://thumbnails.libretro.com) website.

## Features

- **Check for missing thumbnails**: The script scans `.lpl` playlist files and compares the game labels with local thumbnails stored in the `thumbnails` directory.
- **Fetch missing thumbnails**: If a thumbnail is missing, the script will fetch possible matches from the Libretro Thumbnails website and display a list for you to choose from..
- **Supports multiple thumbnail categories**: The script should downloads the thumbnails in the three categories: `Named_Boxarts`, `Named_Snaps`, and `Named_Titles`.
- **Summary report**: After processing, the script generates a report showing the percentage of games with thumbnails for each console.

## How to use

- Put the .py file in the root of the "thumbnails" folder in your retroarch installation folder. Should be "C:\RetroArch-Win64\thumbnails".
Tho if you installed retroarch somewhere else, you could just right click on your retroarch shortcut and click on "open file location". From there you should be able to see your thumbnails folder.
If you don't find your retroarch folder ro you changed it, you can just start retroarch, go to settings, folders, and check the thumbnails folder location from there.
- Once you put the .py file in the thumbnails folder you can just launch it using python. If you don't know how to do juste right click on a blank space inside you folder and select "open in terminal".
Then from the terminal you can type "python thumbnails_downloader_plus.py" and the script should start.
- The script will go through you games playlist and then if a thumbnail is missing for the game, it'll show you al list of thumbnails name that looks like the game from your playlist from libretro website.
- Then you can type the assigned number of the game in the list to select the desired thumbnail.
- Once done the script should download the thumbnails and put them automaticly in the right folders and go on to the next game that miss a thumbnail.
- At the and you'll see a list of your playlist with a percentage of games that has a thumbnails. for exemple 98% would mean that 98% of your playlist a have thumbnails.

## Requirements

To use this script, you need:

- Python 3.x
- `requests` library (for downloading thumbnails)
- `BeautifulSoup` from `bs4` (for scraping the Libretro Thumbnails website)

You can install the required libraries with pip:

```bash
pip install requests beautifulsoup4
