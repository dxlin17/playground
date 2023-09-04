import argparse
import datetime
import enum


WEEK_IN_DAYS = 7

class DaysOfTheWeek(enum.Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


def get_day_prior(tgt: datetime.date):
    return tgt - datetime.timedelta(days=1)


def first_friday_date_of_month(year: int = datetime.datetime.now().year, month: int = datetime.datetime.now().month) -> int:
    first_of_the_month = datetime.date(year, month, 1)
    first_day_weekday = first_of_the_month.isoweekday()
    tgt_dow = DaysOfTheWeek.FRIDAY.value
    days_delta = days_until_next(first_day_weekday, tgt_dow)
    return first_of_the_month + datetime.timedelta(days=days_delta)


def days_until_next(day1: int, day2: int) -> int:
    if day2 - day1 >= 0:
        return day2 - day1
    else:
        return day2 + WEEK_IN_DAYS - day1


if __name__ == '__main__':
    curr_year = datetime.datetime.today().year
    parser = argparse.ArgumentParser(
                        prog="road-sweeper",
                        description="Finds the date prior to the first Friday of the month for a specified month and/or year.")
    
    parser.add_argument('-m', '--month', type=int)
    parser.add_argument('-y', '--year', type=int, default=curr_year, help="Applicable year. Defaults to current year.")
    args = parser.parse_args()

    print(get_day_prior(first_friday_date_of_month(args.year, args.month)))
