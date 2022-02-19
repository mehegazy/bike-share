import time
import pandas as pd
import numpy as np
from pandas.core.algorithms import mode

CITY_DATA = { '1': 'chicago.csv',
              '2': 'new_york_city.csv',
              '3': 'washington.csv' }
long_month=['january', 'february', 'march','april','may','june']
short_month=['jan', 'feb', 'mar','apr','may','jun']

long_day=['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
short_day=['mon','tue','wed','thu','fri','sat','sun']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print("\n 1. chicago \n 2. new york city \n 3. washington")
    
    while True:
        city=input("please select a number of the city you wish to review: ")
        if city not in ['1','2','3']:
            print("please select 1 or 2 or 3")
        else:
            break

    # get user input for month (all, january, february, ... , june)


    while True:
        fav_month=(input("\n write the month you want to revise or write 'all' if you want to check them all: ")).lower()
        if fav_month=="all":
            month=""
            break
        elif not fav_month.isalpha():
            if int(fav_month) in range(1,7):
                month=int(fav_month)
                break
            else:
                print("\n please write valid month like jan or january or 1")
        elif fav_month in long_month:
            month=long_month.index(fav_month)+1
            break
        elif fav_month in short_month:
            month=short_month.index(fav_month)+1
            break
        else:
            print("\n please write valid month like jan or january or 1")

    while True:
        fav_day=(input(" \n write the day you want to revise or write 'all' \n (ps monday is first day of the week): ")).lower()
        if fav_day=="all":
            day=""
            break
        elif not fav_day.isalpha() :
            if int(fav_day) in range(1,8):
                day=int(fav_day)-1
                break
            else:
                print("\n please write valid day like tue or tuesday or 2")
        elif fav_day in long_day:
            day=long_day.index(fav_day)
            break
        elif fav_day in short_day:
            day=short_day.index(fav_day)
            break
        else:
            print("\n please write valid day like tue or tuesday or 2")



    # get user input for day of week (all, monday, tuesday, ... sunday)

    
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
    df=pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    if month:
        df_m_filtered=df.loc[df['month']==month]
    else:
        df_m_filtered=df
    if day:
        df_d_filtered=df_m_filtered.loc[df_m_filtered['day_of_week']==day]
    else:
        df_d_filtered=df_m_filtered

    df_filtered=df_d_filtered.copy()
    

    return df_filtered


def time_stats(df):
    
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    time_stat=[]

    # display the most common month
    
    
    time_stat.append(long_month[df['month'].mode().tolist()[0]-1])

    # display the most common day of week
    time_stat.append(long_day[df['day_of_week'].mode().tolist()[0]])

    # display the most common start hour
    time_stat.append(df['Start Time'].dt.hour.mode().tolist()[0])

    time_common=pd.Series(time_stat,index=['most common month','most common day of week','most common start hour'])

    print(time_common)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    station_stat=[]
    # display most commonly used start station
    station_stat.append(df['Start Station'].mode().tolist()[0])

    # display most commonly used end station
    station_stat.append(df['End Station'].mode().tolist()[0])

    # display most frequent combination of start station and end station trip
    df['Start End']=df['Start Station']+' to '+df['End Station']
    station_stat.append(df['Start End'].mode().tolist()[0])

    station_common=pd.Series(station_stat,index=['most common used start station','most common used end station','most common trip'])
    print(station_common)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    trip_duration_stat=[]
    # display total travel time
    trip_duration_stat.append(df['Trip Duration'].sum())


    # display mean travel time
    trip_duration_stat.append(df['Trip Duration'].mean())

    trip_stat=pd.Series(trip_duration_stat,index=['total travel time','mean travel time'])

    print(trip_stat)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    s1=df['User Type'].value_counts()
    

    # Display counts of gender
    if 'Gender' in df:
        s2=df['Gender'].value_counts()
        # Display earliest, most recent, and most common year of birth
        s3=df['Birth Year'].apply([np.max,np.min])
        s4=df['Birth Year'].mode()
        s=pd.concat([s1,s2,s3,s4])
        s.rename(index={'amax':'most recent year of birth','amin':'earliest year of birth',0:'most common year of birth'},inplace=True)
        print(s)
    else:
        print(s1)






    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw(city):
    """[Display raw data  upon request by the user ]

    Args:
        city ([int]): [integer for the city choise above]
    """
    with open(CITY_DATA[city])as f:
        answer=input('\n Do you want to see raw data: ')
        print('\n')
        while answer.lower()=='yes':
            for i in range(5):
                print(f.readline())

            answer2=input('\n Do you want to see more as a raw data: ')
            print('\n')
            if answer2.lower() != 'yes':
                break   





def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        if df.empty:
            print("no record in your specified filter")
        else:
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
        raw(city)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
        

if __name__ == "__main__":
	main()
