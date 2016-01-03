import datetime
import calendar
import math


class BetterDateTime(datetime.datetime):

    @classmethod
    def from_datetime(cls, dt):
        return cls(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond, dt.tzinfo)

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

    def convert(self, timezone):
        pass

    def get_timezone(self):
        return self.time().tzname()


def test_wrapper():
    before = BetterDateTime(2015, 3, 4)
    dt = BetterDateTime(2015, 3, 5, 15, 42, 11)
    after = BetterDateTime(2015, 4, 4)
    assert(dt.minus_months(1) == BetterDateTime(2015, 2, 5, 15, 42, 11))
    assert(dt.minus_months(5) == BetterDateTime(2014, 10, 5, 15, 42, 11))
    assert(dt.with_start_of_day() == BetterDateTime(2015, 3, 5, 0, 0, 0))
    assert(dt.with_start_of_month() == BetterDateTime(2015, 3, 1, 0, 0, 0))
    assert(dt.with_end_of_day() == BetterDateTime(2015, 3, 5, 23, 59, 59, 999999))
    assert(dt.with_end_of_month() == BetterDateTime(2015, 3, 31, 23, 59, 59, 999999))
    assert(dt.between(before, after))
    assert(not dt.between(before, before))

if __name__=='__main__':
    test_wrapper()
