#Import of time module to calculate processing times
#Import of pandas to filter the pandas DataFrame
#Import of matplotlib to generate a chart
#Import tkinter to build Filter GUI
#Import calendar to convert month number to month name


import matplotlib.pyplot as plt
import time
import pandas as pd
import tkinter as tk
import calendar


#City Data ditionary to choose the data (contained in a csv file) of the City
CITY_DATA = { 'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

#global lists to use them in the functions
cities = list(CITY_DATA.keys())
cities.insert(0, 'all')
months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():

   '''
   Asks user to specify a city, month, and day to analyze.

   Returns:
       (str) city - name of the city, or 'all' to analyze
       (str) month - name of the month to filter by, or 'all' to apply no month filter
       (str) day - name of the day of week to filter by, or 'all' to apply no day filter
   '''

   #defines master which contains all functionality
   master = tk.Tk()
   #Label for welcoming
   lab_welcome = tk.Label(text='Hello! Let\'s explore some US bikeshare data! Welcome in the Filter GUI!').pack()

   lab_city = tk.Label(text="Choose a city. If you don't want to filter the data by city choose 'all': ").pack()
   #Variable to get city value
   variable_city = tk.StringVar(master)
   variable_city.set(cities[0]) # default value
   #drop down widget
   w_city = tk.OptionMenu(master, variable_city, *cities).pack()

   lab_month = tk.Label(text="Choose a month. If you don't want to filter the data by month choose 'all': ").pack()

   variable_month = tk.StringVar(master)
   variable_month.set(months[0]) # default value

   w_month = tk.OptionMenu(master, variable_month, *months).pack()

   lab_day = tk.Label(text="Choose a day. If you don't want to filter the data by day choose 'all': ").pack()

   variable_day = tk.StringVar(master)
   variable_day.set(days[0]) # default value

   w_day = tk.OptionMenu(master, variable_day, *days).pack()

   #Function to get the confirmed values selected
   def cnfrm():
       #make the variable city global to use it the get filter function
       global city
       city = variable_city.get()
       global month
       month = variable_month.get()
       global day
       day = variable_day.get()
       print('You have choosen (' + city + ' / ' + month + ' / ' + day + ') as Filters.')
       if city == 'washington':
           print('There is no data for the Birth Year and Gender column for the city of washington.\nThe output of the User Statistics will make no sense.')

   button = tk.Button(master, text="Confirm your selection", command=cnfrm)
   button.pack()
   #Button to close the master
   button_close = tk.Button(master, text="Press this button and see the results in the terminal screen", command=master.destroy)
   button_close.pack()
   master.mainloop()

   print('-'*40)
   #Function output
   return city, month, day


def load_data(city, month, day):

   '''
   Loads data for the specified city and filters by month and day if applicable.

   Args:
       (str) city - name of the city to analyze
       (str) month - name of the month to filter by, or 'all' to apply no month filter
       (str) day - name of the day of week to filter by, or 'all' to apply no day filter
   Returns:
       df - Pandas DataFrame containing city data filtered by month and day
   '''
   # if clause to generate Df for cities
   if city != 'all':
       df = pd.read_csv(CITY_DATA[city])
   #concatenate all csv files to one dataframe
   else:
       df = pd.concat(map(pd.read_csv, list(CITY_DATA.values())), sort = False)
   #add column Gender, Birth Year to df(washington)
   if city == 'washington':
       df['Gender'] = 'unknown'
       df['Birth Year'] = 'unknown'
   # convert the Start Time column to datetime
   df['Start Time'] = pd.to_datetime(df['Start Time'])
   df['End Time'] = pd.to_datetime(df['End Time'])
   # extract month, day and hour of week from Start Time to create new columns
   df['month'] = df['Start Time'].dt.month
   df['day_of_week'] = df['Start Time'].dt.day_name()
   #generate a new column trip by concatenanting 'Start Station' and 'End Station'
   df["trip"] = df['Start Station'] + ' to ' + df['End Station']
   # filter by month if applicable
   if month != 'all':
       # use the index of the months list to get the corresponding int
       month = months.index(month)
       # filter by month to create the new dataframe
       df = df[df['month'] == month]
   # filter by day of week if applicable
   if day != 'all':
       # filter by day of week to create the new dataframe
       df = df[df['day_of_week'] == day.title()]
   #converts the values of the month column from number to name, found on stackoverflow
   df['month'] = df['month'].apply(lambda x: calendar.month_name[x])
   x =  df.isnull().sum().sum()
   print('Number of NaN values in our DataFrame:', x)
   x_by =  df['Birth Year'].isnull().sum()
   print('Number of NaN values in column Birth Year of our DataFrame:', x_by)
   x_gd =  df['Gender'].isnull().sum()
   print('Number of NaN values in column Gender of our DataFrame:', x_gd)
   print('The sum of NaN values in column Gender and Birth Year of our DataFrame:', x_gd + x_by)
   return df

def time_stats(df):

   '''Displays statistics on the most frequent times of travel.'''

   print('\nCalculating The Most Frequent Times of Travel...\n')
   start_time = time.time()
   # TO DO: display the most common month
   print('The most common month is: ', df.month.mode()[0])
   # TO DO: display the most common day of week
   print('The most common day is: ', df.day_of_week.mode()[0])
   # TO DO: display the most common start hour
   print('The most common hour is: ', pd.to_datetime(df['Start Time']).dt.hour.mode()[0])
   #comparison of most common months of different datasets, f.e. genderspecific, agespecific

   print('\nThis took %s seconds.' % (time.time() - start_time))
   print('-'*40)

def station_stats(df):

   '''Displays statistics on the most popular stations and trip.'''

   print('\nCalculating The Most Popular Stations and Trip...\n')
   start_time = time.time()
   # TO DO: display most commonly used start station
   print('The most common start station is: ', df['Start Station'].mode()[0])
   # TO DO: display most commonly used end station
   print('The most common end station is: ', df['End Station'].mode()[0])
   # TO DO: display most frequent combination of start station and end station
   print('The most common trip is: ', df['trip'].mode()[0])
   # TO DO: display most frequent combination of start station and end station trip
   #print('The most common trip is: ', df.groupby(['Start Station','End Station']).size().idxmax()[0], ' to ',df.groupby(['Start Station','End Station']).size().idxmax()[1])#TRY MODE CONCENTATION OF START AND END STATION

   print('\nThis took %s seconds.' % (time.time() - start_time))
   print('-'*40)


def trip_duration_stats(df):

   '''Displays statistics on the total and average trip duration.'''

   print('\nCalculating Trip Duration...\n')
   start_time = time.time()

   # TO DO: display total travel time
   print('The sum of travel time analyzed is: ', int(df['Trip Duration'].sum()/3600), ' hours')
   # TO DO: display mean travel time
   print('The average of travel time analyzed is: ', int(df['Trip Duration'].mean()/60), ' minutes')
   #To Do: display longest trip by trip Duration
   print('The longest trip by duration is: ', int(df['Trip Duration'].max()/60), ' minutes')
   #To Do: display shortst trip by trip Duration
   print('The shortest trip by duration is: ', int(df['Trip Duration'].min()/60), ' minute(s)')
   # To Do: display the longest trip by substracting EndTime - Start time in a seperate column 'Time Duration'

   print('\nThis took %s seconds.' % (time.time() - start_time))
   print('-'*40)


def user_stats(df):

   '''Displays statistics on bikeshare users.'''

   print('\nCalculating User Stats...\n')
   start_time = time.time()

   # TO DO: Display counts of user types
   try:


       print('There are ', df['User Type'].value_counts()[0], 'as Subscribers')
       print('There are ', df['User Type'].value_counts()[1], 'as Customers')
       print('There are ', len(df.index) - df['User Type'].count(), 'as unknown Users (no Subscribers nor Customers)')
       # TO DO: Display counts of gender
       print('There are ', df['Gender'].value_counts())
       print('There are ', df['Gender'].isnull().sum() + len(df[df['Gender'] == 'unknown']), ' with unknown Gender')
       print('There are totally', len(df.index), 'Users')
       # TO DO: Display earliest, most recent, and most common year of birth
       print('The earliest year of birth is: ', int(df['Birth Year'].min()))
       print('The most recent year of birth is: ', int(df['Birth Year'].max()))
       print('The most common year of birth is: ', int(df['Birth Year'].mode()[0]))

   except ValueError:
       print("There is no data for the Birth Year and Gender column for the city of washington.")


   print('\nThis took %s seconds.' % (time.time() - start_time))
   print('-'*40)

def m_plot_age(df):

   '''
   Plots a chart Age/Trip Duration
   '''
   askfch = input("Do you want to see a chart with the Age on the x-axis and Trip Duration on the y-axis? Enter 'y' for yes! \nFor escaping press Enter.\n")
   if askfch.lower() == 'y':
       plt.rcParams['agg.path.chunksize'] = 10000
       trip = df['Trip Duration'] / 60
       age = df['Birth Year']
       plt.plot(age, trip, 'bo', color='#6760a6')
       plt.title('If you want to proceed, close this window and return to the terminal screen\nAge Trip Correlation')
       plt.ylabel('Trip Duration in min')
       plt.xlabel('Year of birth')
       plt.show()
   else:
       pass


def m_bar_gend(df):
   '''
   Plots a bar chart Age/Usage
   '''

   askfch = input("Do you want to see a chart with the 'Gender' on the x-axis and 'Count of Usage' on the y-axis? Enter 'y' for yes! \nFor escaping press Enter.\n")
   if askfch.lower() == 'y':
       plt.rcParams['agg.path.chunksize'] = 10000
       gdm = len(df[df['Gender'] == 'Male'])
       gdf = len(df[df['Gender'] == 'Female'])
       gunknw = df['Gender'].isnull().sum() + len(df[df['Gender'] == 'unknown'])
       names = ['male', 'female', 'unknown']
       values = [gdm, gdf, gunknw]
       plt.bar(names, values, color='#fc5603')
       plt.title('If you want to proceed, close this window and return to the terminal screen\n\nGender Usage Correlation')
       plt.ylabel('Count of Usage')
       plt.xlabel('Gender')
       plt.show()
   else:
       pass

def raw_data(df):

   '''
   Asks the User if he wants to see the raw data
   '''

   raw_data = input("Do you want to see the analyzed raw data? Enter 'y' for yes.\nFor escaping press Enter.")
   if raw_data.lower() == 'y':
       all_or_five = input("Do you want to see the data scrolling 5 rows below, enter '5'!\nOr do you want an output of all rows at once, enter 'all'!\n")
       if all_or_five == 'all':
           print('Here is the analyzed raw data:\n', df)
       elif all_or_five == '5':
               lines = df.iloc[0:5]
               print('Here are the first 5 rows of raw data:\n', lines)
               j = len(df.index)
               for i in range(5, j, 5):
                   next_lines_question = input("Do you want to see the next 5 lines? Enter 'y' for yes.\nFor escaping press Enter.\n")
                   if next_lines_question == 'y':
                       next_lines = df.iloc[i:(i+5)]
                       print('Here are the next 5 sets of raw data:\n ', next_lines)
                   else:
                       break
   else:
       print('ok')

def main():
   while True:
       city, month, day = get_filters()
       df = load_data(city, month, day)
       time_stats(df)
       station_stats(df)
       trip_duration_stats(df)
       user_stats(df)
       m_plot_age(df)
       m_bar_gend(df)
       raw_data(df)


       restart = input("\nWould you like to restart? Enter 'y' for yes. For escaping press Enter.\n")
       if restart.lower() != 'y':
           break

if __name__ == '__main__':
	main()
