import datetime
import unittest
from dateconverter.dateconverter import DateConverter


class TestDateConverter(unittest.TestCase):
    """ Тесты dateconverter"""

    def test_raises(self):
        with self.assertRaises(ValueError):
            DateConverter(123)
        with self.assertRaises(ValueError):
            DateConverter(['123'])
        with self.assertRaises(ValueError):
            DateConverter({'123'})
        with self.assertRaises(OverflowError):
            DateConverter('421 may 2031') - 111111111111111
        with self.assertRaises(OverflowError):
            DateConverter('11111111111 may 2031')

    def test_date_convert(self):
        # D Month Y
        self.assertEqual(str(DateConverter('Jy ghbt[fk r yfv 12 мая')), '12 мая 2022')
        self.assertEqual(str(DateConverter('Jy ghbt[fk r yfv 12мая')), '12 мая 2022')
        self.assertEqual(str(DateConverter('09:12:11 12мая')), '12 мая 2022')
        self.assertEqual(str(DateConverter('Jy yfv:12мая')), '12 мая 2022')
        self.assertEqual(str(DateConverter('k;jhj 23 asd 11 ')), 'None')
        self.assertEqual(str(DateConverter('12.. мая.. 2020')), '12 мая 2020')
        self.assertEqual(str(DateConverter('12.. мая.. 2020')), '12 мая 2020')
        self.assertEqual(str(DateConverter('k;jhj12 may 20 ')), '12 мая 2020')
        self.assertEqual(str(DateConverter('k;jhj 12 may 20 ')), '12 мая 2020')
        self.assertEqual(str(DateConverter('k;jhj12may201')), '12 мая 201')
        self.assertEqual(str(DateConverter('k;jhj12may20111q')), '12 мая 2011')
        self.assertEqual(str(DateConverter('2011 12 may')), '12 мая 2011')
        self.assertEqual(str(DateConverter('k;jhj12may1')), '12 мая '+str(datetime.date.today().year))
        self.assertEqual(str(DateConverter('52 мая')), '21 июня '+str(datetime.date.today().year))
        self.assertEqual(str(DateConverter('k;jhj12.may1.201')), '12 мая 2022')
        self.assertEqual(str(DateConverter('k;jhj:12:may:2021')), '12 мая 2021')
        self.assertEqual(str(DateConverter('k;jhj_12_may_2021_')), '12 мая 2021')
        self.assertEqual(str(DateConverter('13 МАЯ')), '13 мая 2022')
        self.assertEqual(str(DateConverter('2022Г 13 ИЮНЯ')), '13 июня 2022')
        self.assertEqual(str(DateConverter('2022-12-05')), '5 декабря 2022')

        self.assertEqual(str(DateConverter('23 апреля 20г')), '23 апреля 2020')
        self.assertEqual(str(DateConverter('23 апреля 20')), '23 апреля 2020')
        self.assertEqual(str(DateConverter('23 апреля 55')), '23 апреля 1955')
        self.assertEqual(str(DateConverter('23 апреля 33')), '23 апреля 1933')
        self.assertEqual(str(DateConverter('23 апреля 94')), '23 апреля 1994')

        # D M Y
        self.assertEqual(str(DateConverter('%12_05_2021%')), '12 мая 2021')
        self.assertEqual(str(DateConverter('2022-05-29')), '29 мая 2022')
        self.assertEqual(str(DateConverter('(12/ 5 / 21)/21/30')), 'None')

    def test_eq_datetime(self):
        self.assertEqual(DateConverter('2022-05-29').date, datetime.date(year=2022, month=5, day=29))
        self.assertNotEqual(DateConverter('2022-05-29').date, datetime.datetime(year=2022, month=5, day=29))
        self.assertEqual(DateConverter('12 янв 2020'), datetime.date(2020, 1, 12))
        self.assertEqual(DateConverter('сегодня'), datetime.date.today())
        self.assertEqual(DateConverter('today'), datetime.date.today())
        self.assertEqual(DateConverter('now'), datetime.date.today())
        # Empty
        self.assertEqual(DateConverter(), datetime.date.today())

    def test_add(self):
        self.assertEqual(str(DateConverter('12 jun 2020') + '1m'), '12 июля 2020')
        self.assertEqual(str(DateConverter('12 jun 2020') + '1ы'), '12 июня 2020')
        self.assertEqual(str(DateConverter('12 jun 2020') + '112ф'), '12 июня 2020')
        self.assertEqual(str(DateConverter('1 jan 2020') + '364'), '30 декабря 2020')
        self.assertEqual(str(15 + DateConverter('12 jun 2020')), '27 июня 2020')
        self.assertEqual(str(DateConverter('12 jun 2020') + 20), '2 июля 2020')
        self.assertEqual(str(DateConverter('12 jun 2020') + '15d'), '27 июня 2020')
        self.assertEqual(str(DateConverter('12 jun 2020') + '2m'), '12 августа 2020')
        self.assertEqual(str('12м' + DateConverter('12 jun 2020')), '12 июня 2021')
        self.assertEqual(str(DateConverter('12 jun 2020') + '12y'), '12 июня 2032')
        self.assertEqual(str('200 л' + DateConverter('12 jun 2020')), '12 июня 2220')
        self.assertEqual(str(DateConverter('12 jun 2020') + '200y'), '12 июня 2220')

    def test_sub(self):
        self.assertEqual(str(DateConverter('12 jul 2020') - '1m'), '12 июня 2020')
        self.assertEqual(str(DateConverter('12 jul 2020') - '1ы'), '12 июля 2020')
        self.assertEqual(str(DateConverter('12 jul 2020') - '112ф'), '12 июля 2020')
        self.assertEqual(str(DateConverter('1 янв 2020') - '365'), '1 января 2019')
        self.assertEqual(str(DateConverter('12 jul 2020') - 15), '27 июня 2020')
        self.assertEqual(str(DateConverter('12 янв 2020') - 20), '23 декабря 2019')
        self.assertEqual(str(DateConverter('12 jul 2020') - '15d'), '27 июня 2020')
        self.assertEqual(str(DateConverter('12 jun 2020') - '2m'), '12 апреля 2020')

    def test_sub_year_edge(self):
        self.assertEqual(str(DateConverter('12 янв 2020') - '2м'), '12 ноября 2019')
        self.assertEqual(str(DateConverter('12 jul 2020') - '12м'), '12 июля 2019')
        self.assertEqual(str(DateConverter('12 jul 2020') - '14м'), '12 мая 2019')
        self.assertEqual(str(DateConverter('12 янв 2020') - '48м'), '12 января 2016')
        self.assertEqual(str(DateConverter('12 янв 2020') - '2м'), '12 ноября 2019')
        self.assertEqual(str(DateConverter('12 jul 2020') - '12y'), '12 июля 2008')
        self.assertEqual(str(DateConverter('12 jul 2020') - '200 л'), '12 июля 1820')
        self.assertEqual(str(DateConverter('12 jul 2020') - '200y'), '12 июля 1820')

    def test_compare(self):
        self.assertTrue(DateConverter('12 янв 2020') < datetime.datetime.now())
        self.assertTrue(DateConverter('12 янв 2020') < datetime.date.today())
        self.assertTrue(datetime.date.today() > DateConverter('12 янв 2020'))
        self.assertTrue(datetime.datetime.now() > DateConverter('12 янв 2020'))
        self.assertTrue(DateConverter('1 января 2020') + 20 > DateConverter('12 янв 2020'))
        self.assertTrue(DateConverter('1 января 2020') + 11 == DateConverter('12 янв 2020'))
        self.assertTrue('1 января 2020' < DateConverter('12 янв 2020'))
        self.assertTrue('12 января 2020' == DateConverter('12 янв 2020'))

    def test_get_attr(self):
        self.assertTrue(DateConverter('12 янв 2020').day == 12)
        self.assertTrue(DateConverter('12 янв 2020').month == 'январь')
        self.assertTrue(DateConverter('12 янв 2020').year == 2020)


if __name__ == '__main__':
    unittest.main()
