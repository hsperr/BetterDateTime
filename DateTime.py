import datetime
import math
import calendar


class DateTime(datetime.datetime):

    @classmethod
    def from_datetime(cls, dt):
        return cls(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond, dt.tzinfo)

    def minus_weeks(self, weeks):
        return self.minus_days(weeks*7)

    def plus_weeks(self, weeks):
        return self.plus_days(weeks*7)

    def plus_month(self, months):
        return self.minus_month(-months)

    def minus_month(self, months):
        yeardiff = math.floor(months/12)
        monthdiff = months%12

        result_month = self.month-monthdiff
        if result_month <= 0:
            result_month += 12
            yeardiff += 1

        elif result_month >= 13:
            result_month += 12
            yeardiff -= 1

        return DateTime(self.year-yeardiff, result_month, self.day, self.hour, self.minute, self.second, self.microsecond, self.tzinfo)

    def plus_days(self, days):
        return self.minus_days(-days)

    def minus_days(self, days):
        return DateTime.from_datetime(self - datetime.timedelta(days=days))

    def plus_hours(self, hours):
        return self.minus_hours(-hours)

    def minus_hours(self, hours):
        return DateTime.from_datetime(self - datetime.timedelta(hours=hours))

    def plus_seconds(self, seconds):
        return self.minus_seconds(-seconds)

    def minus_seconds(self, seconds):
        return DateTime.from_datetime(self - datetime.timedelta(seconds=seconds))

    def with_start_of_month(self):
        return DateTime(self.year, self.month, 1, 0, 0, 0, 0, self.tzinfo)

    def with_start_of_day(self):
        return DateTime(self.year, self.month, self.day, 0, 0, 0, 0, self.tzinfo)

    def with_end_of_day(self):
        return DateTime(self.year, self.month, self.day, 23, 59, 59, 999999, self.tzinfo)

    def with_end_of_month(self):
        month_range = calendar.monthrange(self.year, self.month)
        return DateTime(self.year, self.month, month_range[1], 23, 59, 59, 999999, self.tzinfo)

    def between(self, startdate, enddate):
        return startdate < self < enddate


def test_wrapper():
    dt = DateTime(2015, 3, 5, 15, 42, 11)
    assert(dt.minus_month(1) == DateTime(2015, 2, 5, 15, 42, 11))
    assert(dt.minus_month(5) == DateTime(2014, 10, 5, 15, 42, 11))
    assert(dt.with_start_of_day() == DateTime(2015, 3, 5, 0, 0, 0))
    assert(dt.with_start_of_month() == DateTime(2015, 3, 1, 0, 0, 0))
    assert(dt.with_end_of_day() == DateTime(2015, 3, 5, 23, 59, 59, 999999))
    assert(dt.with_end_of_month() == DateTime(2015, 3, 31, 23, 59, 59, 999999))

if __name__=='__main__':
    test_wrapper()
