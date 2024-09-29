import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no 
        month filter
        (str) day - name of the day of week to filter by, or "all" to apply no 
        day filter
    """
    global city, month, day, filt
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a 
    #while loop to handle invalid inputs
    city = input('Would you like to see data for Chicago, New York City, or Washington? ')
    while city.lower() != 'chicago' and city.lower() != 'new york city' and city.lower() != 'washington': 
        city = input('Not a valid city. Please enter the city again: ')

    #Ask user what time filters they want to implement
    filt = input('Would you like to filter {} data by month, day, both, or \'none\'? '.format(city.title() if city.title() != 'Washington' else 'Washington D.C.' ))
    if filt.lower() != 'month' and filt.lower() != 'day' and filt.lower() != 'both' and filt.lower() != 'none':
        filt = input('\nYour response is not a filter type. Please enter a filter type.\nRepeated non-filter answer will assume filter = \'none\' ')
        if filt.lower() != 'month' and filt.lower() != 'day' and filt.lower() != 'both':
            filt = None
            month = None
            day = None

    # get user input for month (all, january, february, ... , june)
    if filt.lower() == 'month' or filt.lower() == 'both':
        if filt.lower() == 'month': day = None 
        month = input('Please type a month (between Jaunary and June) for analysis: ')
        #Check and correct for accidental spaces
        month = month.replace(' ','')
        while True:
            answers = ['January', 'February', 'March', 'April', 'May', 'June',
                      'July','August','September','October','November','December']
            if month.title() in answers:
                break
            else:
                month = input('Not a month or "all", please re-enter: ')
                #Check and correct for accidental spaces
                month = month.replace(' ','')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    if filt.lower() =='day' or filt.lower() == 'both':
        if filt.lower() == 'day': month = None
        day = input('Please type the day for analysis: ')
        #Check and correct for accidental spaces
        day = day.replace(' ','')
        while True:
            answers = ['Monday', 'Tuesday', 'Wednesday','Thursday','Friday',
                    'Saturday','Sunday']
            if day.title() in answers:
                break
            else:
                day = input('Not a day(word), please re-enter: ')
                #Check and correct for accidental spaces
                day = day.replace(' ','')
    if filt.lower() == 'none':
        filt = None
        month = None
        day = None

    print('-'*40)
    return city, month, day, filt

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day, if 
    applicable.
    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no
            month filter
        (str) day - name of the day of week to filter by, or "all" to apply 
            no day filter
    Returns:
        df - pandas DataFrame containing city data filtered by month and day
    """
    global df
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    month_index = df['Start Time'].dt.month
    day_index = df['Start Time'].dt.day_of_week
    # filter by month if applicable
    if month != None:
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month.title())+1
    
        # filter by month to create the new dataframe
        df = df[month_index == month]
    # filter by day of week if applicable
    if day != None:
        # filter by day of week to create the new dataframe
        days = ['Monday', 'Tuesday', 'Wednesday','Thursday','Friday',
                'Saturday','Sunday']
        day = days.index(day.title())
        df = df[day_index == day]
    #Remove unknown column
    df = df.drop(columns=['Unnamed: 0'])
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Extract month, day, and hour from Start Time
    df['Month'] = df['Start Time'].dt.month_name()
    df['Day'] = df['Start Time'].dt.day_name()
    df['Hour'] = df['Start Time'].dt.hour

    # Most common month (only if month is None)
    if month is None:
        popular_month = df['Month'].mode()[0]
        print(f'In the city of {city.title()}, {popular_month} is the most common usage month...')

    # Most common day
    popular_day = df['Day'].mode()[0]
    print(f'{popular_day} is the most common usage day...')

    # Most common hour
    popular_hour = df['Hour'].mode()[0]
    print(f'And {popular_hour}:00 is the most common usage hour')

    print(f"\n...This calculation took {round(time.time() - start_time, 5)} seconds.")
    print('-' * 40)
    
    return


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('In the city of {}, {} is the most start station.'.format(city.title() if city.title() != 'Washington' else 'Washington D.C.', str(df['Start Station'].mode().iloc[0])))

    # display most commonly used end station
    print('{} is the most common end station.'.format(str(df['End Station'].mode().iloc[0])))

    # display most frequent combination of start station and end station trip
    most_frequent_combo = df[['Start Station','End Station']].value_counts().iloc[0:1]
    print('\nAnd the following combination is the most frequent for start station and end station: \n{}'.format(most_frequent_combo.to_string(header=False))[0:-5]) #REFERENCE 3

    print("\n\n...This calculation took %s seconds." % round((time.time() - start_time),5))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The total duration of the trips is: {} seconds'.format(str(df['Trip Duration'].sum())))

    # display mean travel time
    mean = df['Trip Duration'].mean().round(decimals=2)
    print('The mean trip duration is: ~{} seconds, \nor approximately {} minutes and {} seconds'.format(str(mean),str(np.floor(mean / 60).astype('int64')),str((mean % 60).round(decimals=2))))

    print("\n...This calculation took %s seconds." % round((time.time() - start_time),5))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users. \n Only applies to certain cities."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('The user types are:\n' + df['User Type'].value_counts().to_string(header=False))

    if city.lower() == 'washington':
        print('\nThe data from Washington D.C. does not contain gender or birth year information.')
    else:
        # Display counts of gender and NaN values
        print(f'\nThere are {df["Gender"].isnull().sum()} unavailable gender values')
        print('The gender counts are:\n' + df['Gender'].value_counts().to_string(header=False))

        # Display birth year statistics, handling NaN values
        birth_years = df['Birth Year'].dropna()

        print(f'\nThere are {df["Birth Year"].isnull().sum()} unavailable birth year values')
        print(f'The earliest birth year is: {int(birth_years.min())}')
        print(f'The most recent birth year is: {int(birth_years.max())}')
        print(f'The most common birth year is: {int(birth_years.mode()[0])}')

    print(f"\n...This calculation took {round(time.time() - start_time, 5)} seconds.")
    print('-' * 40)
    
def raw_data(df):
    """
    Asks a user if they want to see raw data. If yes, displays raw data from the database
    5 rows(indices) at a time.
    
    Parameters
    ----------
    df : A pandas database describing the bikeshare data for a pre-chosen city.

    """
    raw = input('\nWould you like to see the raw data? Enter yes or no.\n')
    #Replace Spaces
    raw = raw.replace(' ','')
    if raw.lower() == 'yes':
        count = 5
        while True:
            print(df[count-5:count-4].to_dict('index'))
            print(df[count-4:count-3].to_dict('index'))
            print(df[count-3:count-2].to_dict('index'))
            print(df[count-2:count-1].to_dict('index'))
            print(df[count-1:count].to_dict('index'))
            n = input('Press Enter to see next set of data: ')
            if n != '': break
            count += 5
            
    return

def main():
    while True:
        city, month, day, filt = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
    
"""
REFERENCES:
    1) I found information on .mode() and .value_counts() from:
        https://www.tutorialspoint.com/how-to-display-most-frequent-value-in-a-pandas-series#:~:text=Another%20way%20to%20display%20the,count%20of%20each%20unique%20value.
    2) I found information on time-value scraping (i.e. day_name() and month_name() from:
        https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timestamp.html#pandas.Timestamp)  
    3) I found information on the to_string() method from:
        https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_string.html#pandas.DataFrame.to_string
    4) I found information on the astype() method from:
        https://www.geeksforgeeks.org/how-to-convert-float64-columns-to-int64-in-pandas/                                           
"""
