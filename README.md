# BetterDateTime

BetterDateTime provides a wrapper around the buildin python datetime module adding useful functions.
I was heavily inspired by the scala Joda-Time class and wanted to have similar ease in ptyhon working with datetimes and timezones.

## Features

Not sure its a sensible thing to do but BetterDateTime always sets the timezone attribute, if none is specified it will assume the current local timezone. It can be created the same as a regular datetime or by providing a datetime or from milliseconds
Timezones can easily be converted using the as_timezone command.

Some examples of what you are going to get:

```
In [1]: from BetterDateTime import BetterDateTime
In [2]: dt = BetterDateTime(2015, 3, 1, 15, 42, 11)
In [3]: dt.minus_months(5)
Out[3]: BetterDateTime(2014, 10, 1, 15, 42, 11)
In [4]: dt.plus_weeks(5)
Out[4]: BetterDateTime(2015, 4, 5, 15, 42, 11)
In [5]: dt.minus_month(1).with_end_of_month().with_start_of_day()
Out[5]: BetterDateTime(2015, 2, 28, 0, 0)
In [6]: dt.minus_month(1).with_start_of_month().with_end_of_day()
Out[6]: BetterDateTime(2015, 2, 1, 23, 59, 59, 999999)
```


## Support

Please feel free to contribute by opening Issues and PR for improvements.
I develop this in my free time so I might respond slowly.
