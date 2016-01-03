from dateutil import tz
import datetime
import pytz
import calendar
import math


class BetterDateTime(datetime.datetime):

    def __new__(cls, *args, **kwargs):
        if not 'timezone' in kwargs and (not 'tzinfo' in kwargs or not kwargs['tzinfo']) and len(args)<8:
            kwargs['tzinfo'] = BetterDateTime.get_local_timezone()
        elif 'timezone' in kwargs:
            kwargs['tzinfo'] = BetterDateTime.get_timezone(kwargs['timezone'])
            del kwargs['timezone']

        return datetime.datetime.__new__(cls, *args, **kwargs)

    @classmethod
    def from_millis(ms):
        return BetterDateTime.from_datetime(datetime.datetime.fromtimestamp(ms/1000.0))

    @classmethod
    def from_datetime(cls, dt, timezone=None):
        if timezone:
            tzinfo = BetterDateTime.get_timezone(timezone)
        elif not dt.tzinfo:
            tzinfo = BetterDateTime.get_local_timezone()
        else:
            tzinfo = dt.tzinfo
        return cls(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond, tzinfo)

    @staticmethod
    def get_timezone(timezone):
        return pytz.timezone(timezone)

    @staticmethod
    def get_local_timezone():
        return tz.tzlocal()

    def as_timezone(self, timezone_name):
        tzone = BetterDateTime.get_timezone(timezone_name)
        return BetterDateTime.from_datetime(self.astimezone(tzone))

    def as_local_timezone(self):
        local_timezone = BetterDateTime.get_local_timezone()
        return self.astimezone(local_timezone)

    def minus_years(self, years):
        return self.plus_years(-years)

    def plus_years(self, years):
        return self.plus_months(12*years)

    def minus_weeks(self, weeks):
        return self.minus_days(weeks*7)

    def plus_weeks(self, weeks):
        return self.plus_days(weeks*7)

    def plus_months(self, months):
        return self.minus_months(-months)

    def minus_months(self, months):
        yeardiff = math.floor(months/12)
        monthdiff = months%12

        result_month = self.month-monthdiff
        if result_month <= 0:
            result_month += 12
            yeardiff += 1

        elif result_month >= 13:
            result_month += 12
            yeardiff -= 1

        result_year = self.year-yeardiff

        days_per_month = calendar.monthrange(result_year, result_month)
        result_day = min(days_per_month[1], self.day)
        return BetterDateTime(result_year, result_month, result_day, self.hour, self.minute, self.second, self.microsecond, self.tzinfo)

    def plus_days(self, days):
        return self.minus_days(-days)

    def minus_days(self, days):
        return BetterDateTime.from_datetime(self - datetime.timedelta(days=days))

    def plus_hours(self, hours):
        return self.minus_hours(-hours)

    def minus_hours(self, hours):
        return BetterDateTime.from_datetime(self - datetime.timedelta(hours=hours))

    def plus_seconds(self, seconds):
        return self.minus_seconds(-seconds)

    def minus_seconds(self, seconds):
        return BetterDateTime.from_datetime(self - datetime.timedelta(seconds=seconds))

    def with_start_of_month(self):
        return BetterDateTime(self.year, self.month, 1, 0, 0, 0, 0, self.tzinfo)

    def with_start_of_day(self):
        return BetterDateTime(self.year, self.month, self.day, 0, 0, 0, 0, self.tzinfo)

    def with_end_of_day(self):
        return BetterDateTime(self.year, self.month, self.day, 23, 59, 59, 999999, self.tzinfo)

    def with_end_of_month(self):
        month_range = calendar.monthrange(self.year, self.month)
        return BetterDateTime(self.year, self.month, month_range[1], 23, 59, 59, 999999, self.tzinfo)

    def between(self, startdate, enddate):
        return startdate < self < enddate

    def equals(self, datetime):
        return (self.year == datetime.year and
                self.month == datetime.month and
                self.day == datetime.day and
                self.second == datetime.second and
                self.microsecond == datetime.microsecond and
                self.tzinfo == datetime.tzinfo)

    def time_equals(self, datetime):
        return (self.year == datetime.year and
                self.month == datetime.month and
                self.day == datetime.day and
                self.second == datetime.second and
                self.microsecond == datetime.microsecond)



def test_month_changes():
    dt = BetterDateTime(2015, 3, 5, 15, 42, 11)
    assert(dt.minus_months(1).equals(BetterDateTime(2015, 2, 5, 15, 42, 11)))
    assert(dt.minus_months(5).equals(BetterDateTime(2014, 10, 5, 15, 42, 11)))

    assert(dt.plus_months(100).minus_months(100).equals(dt))
    assert(dt.plus_years(1).equals(BetterDateTime(2016, 3, 5, 15, 42, 11)))
    assert(dt.plus_years(1000).minus_years(1000).equals(dt))

    assert(dt.with_start_of_day().equals(BetterDateTime(2015, 3, 5, 0, 0, 0)))
    assert(dt.with_start_of_month().equals(BetterDateTime(2015, 3, 1, 0, 0, 0)))

    assert(dt.with_end_of_day().equals(BetterDateTime(2015, 3, 5, 23, 59, 59, 999999)))
    assert(dt.with_end_of_month().equals(BetterDateTime(2015, 3, 31, 23, 59, 59, 999999)))

def test_between():
    dt = BetterDateTime(2015, 3, 5, 15, 42, 11)
    before = BetterDateTime(2015, 3, 4)
    after = BetterDateTime(2015, 4, 4)
    assert(dt.between(before, after))
    assert(not dt.between(before, before))

def test_from_datetime_with_timezone():
    real_dt = datetime.datetime(2016, 1, 3, 22, 21, 10)
    better_dt = BetterDateTime.from_datetime(real_dt)
    better_dt_utc = BetterDateTime.from_datetime(real_dt, timezone='UTC')

    assert better_dt.time_equals(real_dt)
    assert better_dt_utc.time_equals(real_dt)
    assert not better_dt_utc.equals(better_dt)
    assert not better_dt_utc.equals(real_dt)

def test_plus_months_need_change_days():
    dt = BetterDateTime(2016, 1, 30, 18, 33)
    assert dt.plus_months(1).equals(BetterDateTime(2016, 2, 29, 18, 33))

def test_convert_timezones():
    dt = BetterDateTime(2016, 1, 3, 18, 33, timezone='UTC')
    assert dt.as_timezone('Europe/Berlin').time_equals(dt.plus_hours(1))
    print('Timestamp UTC', dt)
    print('As Local:', dt.as_local_timezone())
    print('Again as utc', dt.as_timezone('UTC'))
    print('Berlin', dt.as_timezone('Europe/Berlin'))
    print('first utc then local', dt.as_timezone('UTC').as_local_timezone())

if __name__ == "__main__":
    test_month_changes()
    test_between()
    test_from_datetime_with_timezone()
    test_plus_months_need_change_days()
    test_convert_timezones()
