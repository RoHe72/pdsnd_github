import time
import pandas as pd
import numpy as np

#adding key for the city and file name as value
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = {'january':1,'february':2,'march':3,'april':4,'may':5,'june':6}

DAYS = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    while True:
        city=input("Would you like to see the data for Chicago, New York or Washington?\n").lower()
        if city in CITY_DATA.keys():
            print('\nSo you want to see the data from {}. If you change your mind or your choice was a mistake, please restart the programm now\n'.format(city.title()))
            break
        elif city == 'new york':
            city = 'new york city'
            print('\nSo you want to see the data from New York. If you change your mind or your choice was a mistake, please restart the programm now\n')
            break
        else:
            print('\nSorry, your answer is not correct! Please try again')


    # get user input for month (all, january, february, ... , june)

    while True:
        month=input("Do you want to filter by Month? Say all if you don't want to filter or choose a month between January and June\n").lower()
        if month in MONTHS :
            print('\nAlright, you want to see the data for the month: ',month.title())
            break
        elif month == 'all' :
            print('\nAlright, you want to see the data for every month')
            break
        else :
            print('\nSorry your answer doesn\'t match, please try again')



    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day=input("\nLast question, do you want to filter by day? Like for month, you can say all or choose a day\n").lower()
        if day in DAYS:
            print('\nAlright, you want to see the data for: ',day.title())
            break
        elif day == 'all':
            print('\nAlright, you want to see the data for every day')
            break
        else:
            print('\nSorry, your answer doesn\'t match, please try again')





    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    #load data file into a dataframe
    df= pd.read_csv(CITY_DATA[city])

    #convert the start time column to date time
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]

    for m in MONTHS :
        if MONTHS[m] == most_common_month:
            most_common_month = m.title()


    print('The most common month is: ',most_common_month)

    # display the most common day of week
    most_common_day= df['day_of_week'].mode()[0]
    print('The most common day is: ', most_common_day)

    # display the most common start hour
    most_common_hour= df['hour'].mode()[0]
    print('The most common start hour is: {} hour'.format(most_common_hour))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_used_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is: ',most_used_start_station)

    # display most commonly used end station
    most_used_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station is: ',most_used_end_station)

    # display most frequent combination of start station and end station trip
    most_combination_station = df['Start Station'] + ' to ' + df['End Station']
    print('The most frequent combination of start station and end station trip was {}'.format(most_combination_station.mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_minutes =  total_travel_time//60%60
    total_hours =  total_travel_time//3600%60
    total_days =  total_travel_time//24//3600
    print('The total time spent to travel is {} days, {} hours and {} minutes :'.format(total_days,total_hours,total_minutes))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_minutes = mean_travel_time//60%60
    mean_hours = mean_travel_time//3600%60
    print('In mean, the travel takes {} hours and {} minutes'.format(mean_hours,mean_minutes))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    print('Counts of user types: ')
    print(df['User Type'].value_counts())

    #Display counts of gender
    if 'Gender' not in df:
        print("\nSorry we don't have gender information for this city")
    else :
        print('\nGender count:')
        print(df['Gender'].value_counts())

    if 'Birth Year' not in df:
          print("\nSorry we don't have birth year information for this city")
    else:

    #Display earliest, most recent, and most common year of birth
          print('\nThe oldest users are born in: {}'.format(int(df['Birth Year'].min())))


          print('The youngest users are born in: {}'.format(int(df['Birth Year'].max())))



          print('Most of the users are born in:{}'.format(int(df['Birth Year'].mode().values[0])))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_rawdata(df):
    """
    Display contents of the CSV file in range 5, until the user don't want anymore
    """

    start = 0
    end = 5

    show_rawdata = input("\nDo you want to see the raw data? Say yes or no\n").lower()

    if show_rawdata == 'yes':
        while end <= df.shape[0] - 1:

            print(df.iloc[start:end,:])
            start += 5
            end += 5

            end_data = input("\nDo you want to see more? Say yes or no\n").lower()
            if end_data == 'no':
                break



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_rawdata(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
