import time
import pandas as pd
import os
os.path.abspath(os.path.dirname('bikeshare.py'))
CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """    
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nHello! Let\'s explore some US bikeshare data!')
    while True:
        try:
            city = input(
                "\nWould you like to see data for Chicago, New York City, or Washington?\n\tPlease write your choice here --> "
            )
            if city.strip().lower() in ['chicago', 'new york city', 'washington']:
                city = city.strip().lower()
                break
            else:
                print(
                    "\nInvalid input or No input taken!\n"
                )
        except KeyboardInterrupt:
            print("\nInvalid input or No input taken!\n")
    while True:
        try:
            month = input(
                "\nWould you like to see data for a certain month from 'January' to 'June' or data for all the six months?\n\tPlease write your 'Month' of choice or write 'All' here--> "
            )
            month_list_choice = ['january', 'february',
                                 'march', 'april', 'may', 'june', 'all']
            if month.strip().lower() in month_list_choice:
                month = month.strip().lower()
                break
            else:
                print(
                    "\nInvalid input or No input taken!\n"
                )
        except KeyboardInterrupt:
            print("\nInvalid input or No input taken!\n")
    while True:
        try:
            day = input(
                "\nWould you like to see data for a certain 'day of the week'?\n\tPlease write your 'Day' of choice or write 'All' here--> "
            )
            days_to_show = ['sunday', 'monday', 'tuesday',
                            'wednesday', 'thursday', 'friday', 'Saturday', 'all']
            if day.strip().lower() in days_to_show:
                day = day.strip().lower()
                break
            else:
                print(
                    "\nInvalid input or No input taken!\n"
                )
        except KeyboardInterrupt:
            print("\nInvalid input or No input taken!\n")
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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(
        df['Start Time'], format='%Y.%m.%d %H:%M')
    df['End Time'] = pd.to_datetime(
        df['End Time'], format='%Y.%m.%d %H:%M')
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(
        df['Start Time'], format='%Y.%m.%d %H:%M')
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    popular_month = df['month'].mode()[0]
    popular_day = df['day_of_week'].mode()[0]
    popular_hour = df['hour'].mode()[0]
    popular_months = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June'
    }
    for key, value in popular_months.items():
        if key == popular_month:
            popular_month = value
    print('Most Frequent Month:', popular_month)
    print('Most Frequent Day Of The Week:', popular_day)
    print('Most Frequent Start Hour: {}:00'.format(popular_hour))
    print("\nThis took %s seconds." % (round(time.time() - start_time, 5)))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    popular_start_station = df['Start Station'].mode()[0]
    popular_end_station = df['End Station'].mode()[0]
    popular_stations = (df['Start Station'] + ' (to) ' +
                        df['End Station']).mode()[0]

    print('Most Commonly Used Start Station:', popular_start_station)
    print('Most Commonly Used End Station:', popular_end_station)
    print('Most Commonly Trip: \n\t(from)', popular_stations)
    print("\nThis took %s seconds." % (round(time.time() - start_time, 5)))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    print(
        'Total Travel Time:', df['Trip Duration'].sum(
        ), 'seconds for', df['Trip Duration'].count(), 'Trips'
    )
    print(
        'Average Trip Duration:', round(
            df['Trip Duration'].mean()), 'seconds'
    )
    print("\nThis took %s seconds." % (round(time.time() - start_time, 5)))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    print('Counts of Users\' Types:')
    type_count = df['User Type'].value_counts()
    type_name = df['User Type'].value_counts().index
    for x in type_name:
        print("\t{}(s): {}".format(x, type_count[x]))
    try:
        print('\nCounts of Users\' Genders:')
        gender_count = df['Gender'].value_counts()
        gender_name = df['Gender'].value_counts().index
        for x in gender_name:
            print("\t{}(s): {}".format(x, gender_count[x]))
    except KeyError:
        print('\tNo Gender Data Available for This City.\n')
    try:
        print('\nUsers\' Birth Years Count:')
        print("\tThe Earliest User's Birth Year:", int(df['Birth Year'].min()))
        print("\tThe Most Recent User's Birth:", int(df['Birth Year'].max()))
        print("\tThe Most Common User's Birth Year:",
              int(df['Birth Year'].mode()))
    except KeyError:
        print('\tNo Birth Year Data Available for This City.\n')
    print("\nThis took %s seconds." % (round(time.time() - start_time, 5)))
    print('-'*40)


def display_data(df, city):
    view_display = input(
        "\nDo you want to see the first 5 rows of data?\n Enter (Yes) or (No), here --> "
    )
    start_loc = 0
    while view_display.strip().lower() not in ['yes', 'no']:
        print('\nInvalid Input!\n')
        view_display = input(
            "Do you want to see the first 5 rows of data?\n Enter (Yes) or (No), here --> "
        )
    while view_display.strip().lower() == 'yes':
        pd.set_option("display.precision", 0)
        columns_to_show = ['Start Time', 'End Time', 'Trip Duration',
                           'Start Station', 'End Station', 'User Type']
        if city == 'washington':
            columns_to_show = columns_to_show
        else:
            columns_to_show.append('Gender')
            columns_to_show.append('Birth Year')
        df_column = df[columns_to_show]
        pd.set_option('display.max_columns', 12)
        pd.set_option("max_colwidth", 70)
        print(df_column.fillna('not available').iloc[start_loc:start_loc+5])
        start_loc += 5
        view_display = input(
            "Do you want to see the next 5 rows of data?\n Enter (Yes) or (No), here --> "
        )
        while view_display.strip().lower() not in ['yes', 'no']:
            print('\nInvalid Input!\n')
            view_display = input(
                "Do you want to see the next 5 rows of data?\n Enter (Yes) or (No), here --> "
            )
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df, city)
        restart = input(
            '\nWould you like to restart?\n Enter (yes) or (no), here --> '
        )
        while restart.lower().strip() not in ['yes', 'no']:
            print('\nInvalid Input!\n')
            restart = input(
                'Would you like to restart?\n Enter (yes) or (no), here --> '
            )
        if restart.lower().strip() != 'yes':
            break


if __name__ == "__main__":
    main()
