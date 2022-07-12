# Holiday Manager

A python program designed for importing, editing, and exporting a list of holidays.

### holiday manager.py

The holiday manager program. Initializes a 'Holiday' object class and a 'HolidayList' container and wrapper class for holiday objects.

On startup, adds holidays from 'holidays.json' and scraped holidays from [timeanddate](https://www.timeanddate.com/holidays/us/) using BeautifulSoup. Scrapes all holidays and national/global observances from the current year, the previous 2 years, and the next 2 years.

Users have the option to:
* add or delete a holiday by inputting a holiday name and date,
* export the current list of holidays to 'saved holidays.json',
* view holidays for the current week and year, or
* view holidays for a specified week and year.

### holidays.json

Starter file containing 7 holidays with their names and dates. Lays out the basic format of .json files to be imported/exported.

### saved holidays.json

Exported file from the holiday manager build. Contains the holidays from the starter 'holidays.json' file, as well as scraped holidays from years 2020 to 2024. Follows the formatting of the 'holidays.json' file.