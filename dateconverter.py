import datetime
from re import findall


class DateConverter:
    __rus_letters = 'абвгдеёжзиклмнопрстуфхцчшщьыъэюяАБВГДЕЁЖЗИКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ'
    __regex_symbols = r'''\.\!\"\#\$\%\&\'\(\)\*\+\,\-\/\\\:\;\<\=\>\?\@\[\]\^\_\`\{\|\}\~'''
    __date_regex = [
        r'(\d+' + rf')[\s{__regex_symbols}]*([а-яА-Яa-zA-Z]' + '{3,}' + rf')[\s{__regex_symbols}]*(\d' + '{2,4}' + rf')[\s{__regex_symbols}]*',
        # D Month Y

        r'(\d+' + rf')[\s{__regex_symbols}]+(\d' + '{1,2}' + rf')[\s{__regex_symbols}]+' + r'(\d{2,4})',
        # D M Y

        r'(\d' + '{4}' + rf')\s*[гy]*[\s{__regex_symbols}]+(\d+' + rf')[\s{__regex_symbols}]+([а-яА-Я]' + '{3,})',
        # Y D Month

        r'(\d' + '{2}' + rf')\s*[гy][\s{__regex_symbols}]+(\d+' + rf')[\s{__regex_symbols}]+([а-яА-Я]' + '{3,})',
        # Y D Month

        r'(\d' + '{2,4}' + rf')\s*[гy]*[\s{__regex_symbols}]+(\d+' + rf')[\s{__regex_symbols}]+(\d' + '{1,2})',
        # Y D M

        r'(\d+' + rf')[\s{__regex_symbols}]*([а-яА-Яa-zA-Z]' + '{3,}' + rf')[\s{__regex_symbols}]*',
        # D Month

        r'(\d+' + rf')[\s{__regex_symbols}]+(\d' + '{1,2})'
        # D M
    ]
    __rus_month_regex = ['янв', 'фев', 'мар', 'апр', 'май|мая', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']
    __eng_month_regex = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    __rus_month_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября',
                        'октября', 'ноября', 'декабря']
    __rus_month_list2 = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь',
                         'октябрь', 'ноябрь', 'декабрь']

    def __init__(self, date_string: str):
        self.date: datetime.date

        if findall(r'[а-яА-Я]', date_string):
            self.__lang = 'rus'
        elif findall(r'[a-zA-Z]', date_string):
            self.__lang = 'eng'
        else:
            self.__lang = None
        self.setdate(date_string)

    def setdate(self, date_string):
        for i, regex in enumerate(self.__date_regex, start=1):
            date_f = findall(
                regex,
                date_string
            )
            if date_f and len(date_f) == 1:
                try:
                    if i < 3:  # D M Y
                        year = self.__year_format(date_f[0][2])
                        month = self.__month_in_digit(date_f[0][1])
                        day = int(date_f[0][0])

                    elif 3 <= i <= 5:   # Y D M
                        year = self.__year_format(date_f[0][0])
                        month = self.__month_in_digit(date_f[0][2])
                        day = int(date_f[0][1])

                    elif i > 5:  # D M
                        year = datetime.date.today().year
                        month = self.__month_in_digit(date_f[0][1])
                        day = int(date_f[0][0])

                    try:
                        self.date = datetime.date(year, month, day)

                    except ValueError as ve:
                        if str(ve) == 'day is out of range for month':
                            self.date = datetime.date(year, month, 1) + datetime.timedelta(days=day-1)

                except TypeError:
                    pass
                break
            else:
                continue

    @staticmethod
    def __month_in_digit(month):
        try:
            return int(month)
        except ValueError:
            for m in DateConverter.__rus_month_regex:
                if findall(m, month.lower()):
                    return DateConverter.__rus_month_regex.index(m)+1
            for m in DateConverter.__eng_month_regex:
                if findall(m, month.lower()):
                    return DateConverter.__eng_month_regex.index(m)+1

    @staticmethod
    def __year_format(year):
        if len(year) == 4:
            return int(year)
        elif len(year) == 2:
            if 2000 + int(year) <= datetime.date.today().year + 10:
                return 2000 + int(year)
            elif 2000 + int(year) > datetime.date.today().year + 10:
                return 1900 + int(year)

    def __str__(self):
        if not self.__dict__.get('date'):
            return "None"
        return f"{self.date.day} {self.__rus_month_list[self.date.month - 1]} {self.date.year}"

    def __add_sub(self, other, mode: str) -> object:
        if isinstance(other, int):
            if mode == '+':
                self.date += datetime.timedelta(days=other)
            elif mode == '-':
                self.date -= datetime.timedelta(days=other)
        elif isinstance(other, str) and findall(r'^\d+[dmyдмгл]$', other):
            # ДЕНЬ
            if other.endswith('d') or other.endswith('д'):
                if mode == '+':
                    self.date += datetime.timedelta(days=int(other[:-1]))
                elif mode == '-':
                    self.date -= datetime.timedelta(days=int(other[:-1]))
            # МЕСЯЦ
            elif other.endswith('m') or other.endswith('м'):
                try:
                    if mode == '+':
                        months = self.date.month + int(other[:-1])  # текущий месяц + дополнительные
                        year = self.date.year + months // 12
                        month = months % 12
                    elif mode == '-':
                        months = abs(self.date.month - int(other[:-1]))  # текущий месяц - дополнительные
                        year = self.date.year - (months // 12 + 1)
                        month = 12 - (months % 12)
                    self.date = datetime.date(year, month, self.date.day)
                except ValueError as ve:
                    if str(ve) == 'day is out of range for month':
                        self.date = datetime.date(year, month, 1) + datetime.timedelta(days=self.date.day-1)
            # ГОД
            elif other.endswith('y') or other.endswith('л') or other.endswith('г'):
                if mode == '+':
                    self.date = datetime.date(self.date.year + int(other[:-1]), self.date.month, self.date.day)
                elif mode == '-':
                    self.date = datetime.date(self.date.year - int(other[:-1]), self.date.month, self.date.day)

        return self

    def __add__(self, other):
        return self.__add_sub(other, '+')

    def __radd__(self, other):
        return self.__add_sub(other, '+')

    def __iadd__(self, other):
        return self.__add_sub(other, '+')

    def __sub__(self, other):
        return self.__add_sub(other, '-')

    def __rsub__(self, other):
        return self.__add_sub(other, '-')

    def __isub__(self, other):
        return self.__add_sub(other, '-')

    def __getitem__(self, item):
        if item == 'day':
            return self.date.day
        elif item == 'month':
            return self.__rus_month_list2[self.date.month - 1]
        elif item == 'year':
            return self.date.year
