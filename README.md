# date converter

Преобразует различные форматы дат к единому


```python
from dateconverter import DateConverter

date1 = DateConverter('12 мар 21')

date1           # 12 марта 2021
type(date1)     # <class 'dateconverter.DateConverter'>

date1['day']    # 12
date1['month']  # март
date1['year']   # 2021

# Также возвращает дату в виде объекта класса datetime
date1.date          # 2021-03-12
type(date1.date)    # <class 'datetime.date'>
```
### Сложение дат

```python
from dateconverter import DateConverter

date = DateConverter('1 mar 21')  # 1 марта 2021
date += '2m'  # 1 мая 2021
date += 12    # 13 мая 2021
date -= '1y'  # 13 мая 2020
```

### Примеры преобразований

    1 мар. 2001г. -> 1 марта 2001
    
    01.10.2021    -> 1 октября 2021
    
    1\mar 2021    -> 1 марта 2021
    
    2021г. 1 мая  -> 1 мая 2021
    
    2021 1 мая    -> 1 мая 2021
    
    21г 1 мая     -> 1 мая 2021
    
    31г 1 мая     -> 1 мая 2031
    
    32г 1 мая     -> 1 мая 1932

    1,мар20       -> 1 марта 2020
    
    2021.01.12    -> 13 июля 2017
    
    01.12         -> 1 декабря 2021
    
    14 июля       -> 14 июля 2021
    
    23 JUN        -> 23 июня 2021
    
    32 JaN        -> 1 февраля 2021

При превышении количества дней в месяце осуществляется перенос на следующий
    
    232 авг       -> 20 марта 2022
    
    2021г.111 мая -> 19 августа 2021
    
    441.10.2021   -> 15 декабря 2022
    
    21г 111 мая   -> 19 августа 2021
    
    111,мар20     -> 19 июня 2020
