# ptimedelta

Convert time periods represented by strings to timedelta objects and vice versa. 

## Features
1. Supports Python2.7, Python3+.
2. Supports time periods with days, hours, minutes, seconds, milliseconds.

## Installation
```shell script
$ pip install ptimedelta
```

## Examples
```pydocstring
>>> import ptimedelta as ptd
>>> ptd.to_timedelta("12m34s")
datetime.timedelta(seconds=754)
>>> ptd.to_seconds("3h23m4s", as_int=True)
12184
>>> ptd.to_seconds("3.96ms")
0.00396
```
