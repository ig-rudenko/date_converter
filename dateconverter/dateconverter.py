import datetime
from re import findall


class DateConverter:
    __rs = r'\.\,\-\/\\\_'
    __date_regex = [
        # D Month Y
        r'(\d+)'+rf'[{__rs}:]'+r'{0,2}\s*([а-яА-Яa-zA-Z]{3,})'+rf'[{__rs}:]'+r'{0,2}\s*(\d{2,4})',

        # D M Y or (D M Y)
        r'(?<!\d)\(?(\d{1,2})'+rf'[\s{__rs}]'+r'{1}\s*(\d{1,2})'+rf'[\s{__rs}]'+r'{1}\s*(\d{2,4})\)?',

        # Y D Month
        r'(\d' + '{4}' + rf')\s*[гy]*[\s{__rs}]+(\d+' + rf')[\s{__rs}]+([а-яА-Яa-zA-Z]' + '{3,})',

        # Y[гy] D Month
        r'(\d' + '{2}' + rf')\s*[гy][\s{__rs}]+(\d+' + rf')[\s{__rs}]+([а-яА-Яa-zA-Z]' + '{3,})',

        # Y M D
        r'(?<!\d)(\d{4})' + rf'\s*[гy]*[\s{__rs}](\d+' + rf')[\s{__rs}]+(\d' + '{1,2})',

        # D Month
        r'(\d+' + rf')[{__rs}]*\s*([а-яА-Яa-zA-Z]' + '{3,})',

        # D M
        r'\s(\d+' + rf')[{__rs}]*\s*(\d' + '{1,2})' + rf'[{__rs}]\s*'

    ]
    __rus_month_regex = ['янв', 'фев', 'мар', 'апр', 'май|мая', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']
    __eng_month_regex = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    __rus_month_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября',
                        'октября', 'ноября', 'декабря']
    __rus_month_list2 = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь',
                         'октябрь', 'ноябрь', 'декабрь']

    def __init__(self, date_string: str = ''):
        if not isinstance(date_string, str):
            raise ValueError('Необходимо передавать только строки')

        if not date_string:
            self.date = datetime.date.today()
            return

        self.date: datetime.date
        self.day = None
        self.month = None
        self.year = None

        if findall(r'[а-яА-Я]', date_string):
            self.__lang = 'rus'
        elif findall(r'[a-zA-Z]', date_string):
            self.__lang = 'eng'
        else:
            self.__lang = None
        self.setdate(date_string)

    def setdate(self, date_string):
        if date_string == 'now' or date_string == 'today' or date_string == 'сегодня':
            self.date = datetime.date.today()

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

                    elif 3 <= i <= 4:   # Y D M
                        year = self.__year_format(date_f[0][0])
                        month = self.__month_in_digit(date_f[0][2])
                        day = int(date_f[0][1])

                    elif i == 5:   # Y M D
                        year = self.__year_format(date_f[0][0])
                        month = self.__month_in_digit(date_f[0][1])
                        day = int(date_f[0][2])

                    else:  # D M
                        year = datetime.date.today().year
                        month = self.__month_in_digit(date_f[0][1])
                        day = int(date_f[0][0])

                    try:
                        self.day = day
                        self.month = self.__rus_month_list2[month - 1]
                        self.year = year
                        self.date = datetime.date(year, month, day)

                    except ValueError as ve:
                        if str(ve) == 'day is out of range for month':
                            self.date = datetime.date(year, month, 1) + datetime.timedelta(days=day-1)
                except TypeError:
                    pass
                break

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
        if len(year) >= 3:
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
        if isinstance(other, int) or (isinstance(other, str) and other.isdigit()):
            other = int(other)
            if mode == '+':
                self.date += datetime.timedelta(days=other)
            elif mode == '-':
                self.date -= datetime.timedelta(days=other)
        elif isinstance(other, str) and findall(r'^\d+\s*[dmyдмгл]$', other):
            # ДЕНЬ
            if other.endswith('d') or other.endswith('д'):
                if mode == '+':
                    self.date += datetime.timedelta(days=int(other[:-1]))
                elif mode == '-':
                    self.date -= datetime.timedelta(days=int(other[:-1]))
            # МЕСЯЦ
            elif other.endswith('m') or other.endswith('м'):

                if mode == '+':
                    month = self.date.month + int(other[:-1])  # текущий месяц + дополнительные
                    year = self.date.year + month // 12
                    month = month % 12
                else:
                    month = self.date.month - int(other[:-1])  # текущий месяц - дополнительные

                    if month < 0:
                        month = abs(month) + 1
                        year = self.date.year - (month // 12 or 1)
                        month = 13 - (month % 12 or 12)
                    else:
                        year = self.date.year

                try:
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

    def __measure(self, other, p):
        if isinstance(other, datetime.datetime):
            return eval(f"self.date {p} datetime.date(other.year, other.month, other.day)")
        elif isinstance(other, datetime.date):
            return eval(f"self.date {p} other")
        elif isinstance(other, str):
            return eval(f"self.date {p} DateConverter(other).date")
        elif isinstance(other, DateConverter):
            return eval(f"self.date {p}other.date")
        else:
            raise ValueError(f'Нельзя сравнивать дату с "{other.__class__.__name__}"')

    def __eq__(self, other):
        return self.__measure(other, '==')

    def __lt__(self, other):
        return self.__measure(other, '<')

    def __le__(self, other):
        return self.__measure(other, '<=')

    def __gt__(self, other):
        return self.__measure(other, '>')

    def __ge__(self, other):
        return self.__measure(other, '>=')

    def __ne__(self, other):
        return self.__measure(other, '!=')

