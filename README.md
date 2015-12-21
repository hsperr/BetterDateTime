# BetterTime

BetterTime provides a wrapper around the buildin python datetime module adding useful functions.
I was heavily inspired by the scala Joda-Time class and wanted to have similar ease in ptyhon working with datetimes and timezones.

Some examples of what you are going to get:

```
> dt = DateTime(2015, 3, 1, 15, 42, 11)
2015-03-01 15:42:11
> print(dt.minus_month(1))
2014-11-01 15:42:11
> print(dt.plus_weeks(5))
2015-04-05 15:42:11
> print(dt.with_end_of_month().with_start_of_day())
2015-02-28 00:00:00
> print(dt.with_start_of_month().with_end_of_day())
2015-03-01 23:59:59.999999
```


## Support

Please feel free to contribute by opening Issues and PR for improvements.
I develop this in my free time so I might respond slowly.
