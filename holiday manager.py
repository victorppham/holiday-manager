import datetime                     # datetime object used by holiday dataclass
import json                         # importing/exporting JSON
from bs4 import BeautifulSoup       # soup for scraping
import requests                     # requests for weather API
from dataclasses import dataclass


# -------------------------------------------
# Modify the holiday class to 
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------
@dataclass
class Holiday:
    name: str
    date: datetime

    def __str__(self):
        template = '{0}\n{1}'
        return template.format(self.name, self.date.strftime('%Y-%m-%d'))
          
           
# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------
class HolidayList:
    def __init__(self):
       self.innerHolidays = [] # list

    def __str__(self):
        return self.innerHolidays
   
    def addHoliday(self, holidayObj):
        # Make sure holidayObj is an Holiday Object by checking the type
        # Use innerHolidays.append(holidayObj) to add holiday
        # print to the user that you added a holiday 

        if type(holidayObj) is Holiday:         # checks type
            self.innerHolidays.append(holidayObj)
            print('Holiday added!')
        else:
            print('An error has occurred trying to add a holiday.')


    def findHoliday(self, HolidayName, Date):
        # Find Holiday in innerHolidays
        # Return Holiday

        if type(Date) == str:
            date_object = datetime.datetime.strptime(Date, '%Y-%m-%d')

        elif type(Date) == datetime.datetime:
            date_object = Date

        else:
            print('Invalid parameters passed for date! Strings in yyyy-mm-dd and datetime objects are accepted.')
            return

        # list of holidays
        holiday_search = [item for item in self.innerHolidays if item.name.find(HolidayName) != -1 and item.date == date_object]

        # ideally this will only have 1 holiday if holidays are unique in innerHolidays
        # list of dicts created with 1 element

        if len(holiday_search) == 1:
            return holiday_search[0] # eliminates the list

        else: # holiday_search contains 2 or more holidays, or no holiday was found
            return # if assigned, this is None


    def removeHoliday(self, HolidayName, Date):
        # Find Holiday in innerHolidays by searching the name and date combination.
        # remove the Holiday from innerHolidays
        # inform user you deleted the holiday

        holiday_to_delete = self.findHoliday(HolidayName, Date) # will return 1 or no holidays

        if bool(holiday_to_delete): # boolean true if 1 holiday returned
            self.innerHolidays.remove(holiday_to_delete)
            print('Deleted holiday {}!'.format(holiday_to_delete.name))

        else: # findHoliday() returned nothing
            print("Could not delete the holiday.\nMaybe the holiday wasn't found, or more than one was queried.")


    def read_json(self, filelocation):
        # Read in things from json file location
        # Use addHoliday function to add holidays to inner list.

        f = open(filelocation)
        data = json.load(f)
        f.close()

        for i in data['holidays']:
            name = i['name']
            date = i['date']
            date_object = datetime.datetime.strptime(date, "%Y-%m-%d")

            holidayObj = Holiday(name, date_object)

            self.addHoliday(holidayObj) # !! will print many lines of 'Holiday added!' due to function output


    def myconverter(self, o):
        if isinstance(o, datetime.datetime):
            return o.__str__()


    def save_to_json(self, filelocation):
        # Write out json file to selected file.

        json_string = json.dumps({'holidays':[ob.__dict__ for ob in self.innerHolidays]}, default = self.myconverter)
        jsonFile = open(filelocation, "w")
        jsonFile.write(json_string) # writes everything as a single line
        jsonFile.close()
        

    def scrapeHolidays(self):
        # Scrape Holidays from https://www.timeanddate.com/holidays/us/ 
        # Remember, 2 previous years, current year, and 2 years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
        # Check to see if name and date of holiday is in innerHolidays array
        # Add non-duplicates to innerHolidays
        # Handle any exceptions.     

        current_year = datetime.datetime.now().year                 # selects from the current year
        year_range = range(current_year-2, current_year+3, 1)       # 5 year range
        html_string = "https://www.timeanddate.com/holidays/us/{}"  # modifiable url to scrape from the 5 required years

        list_scraped_holidays = []

        for i in year_range:

            html = requests.get(html_string.format(i)).text
            soup = BeautifulSoup(html,'html.parser')
            table = soup.find('table',attrs = {'class':'table--holidaycountry'})

            for row in table.find_all_next('tr'):

                table_headers = row.find_all_next('th') # dates contained within 'th' instead of 'td'
                cells = row.find_all_next('td')

                if len(cells) == 1: # avoiding the table footers
                    break

                scraped_holiday = {}

                scraped_holiday['Date'] = table_headers[0].string + " {}".format(i) # appending a year onto the date as a string
                scraped_holiday['Name'] = cells[1].string # scraping holiday name

                list_scraped_holidays.append(scraped_holiday) # list of scraped holidays

            # adding scraped holidays to innerholidays list as Holiday objects

            for i in list_scraped_holidays:
                list_name = i['Name']
                list_date = i['Date']

                while True:
                    try:
                        date_object = datetime.datetime.strptime(list_date, "%b %d %Y")
                        holidayObj = Holiday(list_name, date_object)

                        # seeing if the holiday is already in innerHolidays
                        holiday_search = self.findHoliday(list_name, date_object)

                        if not holiday_search: # holiday is not in innerHolidays
                            self.innerHolidays.append(holidayObj) # used over addHoliday fxn to avoid printing too many lines
                        break

                    except ValueError: # each year has an invalid date "Date"; this handles those exceptions
                        break # total of 5 exceptions should be expected

    def numHolidays(self):
        # Return the total number of holidays in innerHolidays
        holiday_count = len(self.innerHolidays)

        return holiday_count
    
    def filter_holidays_by_week(self, year, week_number):
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Week number is part of the the Datetime object
        # Cast filter results as list
        # return your holidays

        year_and_week = '{}-{}'.format(year, week_number)
        holidays = filter(lambda x: x.date.strftime('%Y-%W') == year_and_week, self.innerHolidays)

        filtered_list = list(holidays) # turns filter type into list type

        return filtered_list


    def displayHolidaysInWeek(self, holidayList):
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week. 
        # * Remember to use the holiday __str__ method.

        for i in holidayList:
            print("{}\n{}\n".format(i.date.strftime('%a'), i))


    def getWeather(weekNum):
        # Convert weekNum to range between two days
        # Use Try / Except to catch problems
        # Query API for weather in that week range
        # Format weather information and return weather string.

        pass

        

    def viewCurrentWeek(self):
        # Use the Datetime Module to look up current week and year
        # Use your filter_holidays_by_week function to get the list of holidays 
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results

        current_date = datetime.datetime.now()

        current_year = current_date.year
        current_week = datetime.datetime.strftime(current_date, '%W')

        filtered_list = self.filter_holidays_by_week(current_year, current_week)
        self.displayHolidaysInWeek(filtered_list)


def divider():
    print('===================')


def main():
    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Initialize HolidayList Object
    # 2. Load JSON file via HolidayList read_json function
    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    # 3. Create while loop for user to keep adding or working with the Calender
    # 4. Display User Menu (Print the menu)
    # 5. Take user input for their action based on Menu and check the user input for errors
    # 6. Run appropriate method from the HolidayList object depending on what the user input is
    # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going. 

    # initializing
    holiday_list = HolidayList()
    user_working = True

    # reading from json file and adding holidays
    holiday_list.read_json('holidays.json')

    # scraping from web and adding holidays
    holiday_list.scrapeHolidays()

    # start up menu
    print('Holiday Management')
    divider()
    print('There are {} holidays stored in the system.'.format(holiday_list.numHolidays()))

    while user_working == True:
        print('Holiday Menu')
        divider()
        print('1. Add a Holiday\n2. Remove a Holiday\n3. Save Holiday List\n4. View Holidays\n5. Exit')
        
        user_option = int(input('What would the user like to do? [1-5]'))

        if user_option == 1: # adding a holiday
            print("Add a Holiday\n=============")
    
            holiday_name = str(input('Enter the name of the holiday to be added: ')).strip()
            print("\nHoliday: {0}".format(holiday_name))

            holiday_date_string = str(input('Enter the date of the holiday to be added, in yyyy-mm-dd format: ')).strip()
            print("Date: {0}".format(holiday_date_string))

            while True:
                try:

                    # check for duplicate holidays
                    if bool(holiday_list.findHoliday(holiday_name, holiday_date_string)):
                        print('holiday already exists!')
                        break

                    holiday_date_object = datetime.datetime.strptime(holiday_date_string, "%Y-%m-%d")
                    holidayObj = Holiday(holiday_name, holiday_date_object)

                    holiday_list.addHoliday(holidayObj) 

                except ValueError:
                    print('Error encountered! Check the date format.')
                    break

        elif user_option == 2: # removing a holiday
            print('Remove a Holiday')
            divider()

            holiday_name = str(input('Enter the name of the holiday to be deleted: ')).strip()
            print("\nHoliday: {0}".format(holiday_name))

            holiday_date_string = str(input('Enter the date of the holiday to be deleted, in yyyy-mm-dd format: ')).strip()
            print("Date: {0}".format(holiday_date_string))

            holiday_list.removeHoliday(holiday_name, holiday_date_string)

        elif user_option == 3:
            print('Saving Holiday List')
            divider()
            user_save = str(input('Are you sure you want to save your changes? [y/n]')).lower()

            if user_save == 'n':
                print('Canceled:\nHoliday list file save canceled.')

            elif user_save == 'y':
                holiday_list.save_to_json('saved holidays.json')
                print('Success:\nYour changes have been saved.')

            else:
                print('Invalid option for saving!')

        elif user_option == 4:
            print('View Holidays')
            divider()

            print('Would you like to see the current week? [y/n]')
            user_current_week = str(input('Please enter your choice:'))

            if user_current_week == 'y': # current week selected
                holiday_list.viewCurrentWeek()

            elif user_current_week == 'n': # past/future week selected

                print('Which year would you like to check? Holidays can be viewed up to 2 future years.') # !! will not check for years not scraped !!
                user_year = int(input('Please input the year you want to view holidays for:'))
                print(user_year)

                print('Which week? [1-52, 0 for current week')
                user_week = int(input('Please input the week you want to view holidays for:'))
                print(user_week)

                if user_week > 52 or user_week < 0:
                    print('Invalid week!')
                elif user_week == 0:
                    current_date = datetime.datetime.now()
                    user_week = datetime.datetime.strftime(current_date, '%W')

                filtered_list = holiday_list.filter_holidays_by_week(user_year, user_week) # filters according to user input
                holiday_list.displayHolidaysInWeek(filtered_list) # displayed holidays for year and week selected

            else:
                print('Invalid option for holiday viewing!')

        elif user_option == 5: # user wants to quit
            print('Exit\n=====\nAre you sure you want to exit? Any unsaved changes will be discarded! [y/n]')
            user_exit = str(input('Please enter your input:')).lower()

            if user_exit == 'y':
                print('Goodbye!')
                user_working = False
            elif user_exit == 'n':
                pass
            else:
                print('Invalid option for exiting!')

        else:
            print('Invalid option!')


if __name__ == "__main__":
    main();


# Additional Hints:
# ---------------------------------------------
# You may need additional helper functions both in and out of the classes, add functions as you need to.
#
# No one function should be more then 50 lines of code, if you need more then 50 lines of code
# excluding comments, break the function into multiple functions.
#
# You can store your raw menu text, and other blocks of texts as raw text files 
# and use placeholder values with the format option.
# 

# Example:
# In the file test.txt is "My name is {fname}, I'm {age}"
# Then you later can read the file into a string "filetxt"
# and substitute the placeholders 
# for example: filetxt.format(fname = "John", age = 36)
# This will make your code far more readable, by seperating text from code.