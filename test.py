import unittest
from dateconverter.dateconverter import DateConverter


class TestDateConverter(unittest.TestCase):

    def test_date_convert(self):
        # D Month Y
        self.assertEqual(str(DateConverter('Jy ghbt[fk r yfv 12 мая')), '12 мая 2022', 'Должно быть 12 мая')
        self.assertEqual(str(DateConverter('Jy ghbt[fk r yfv 12мая')), '12 мая 2022', 'Должно быть 12 мая')
        self.assertEqual(str(DateConverter('09:12:11 12мая')), '12 мая 2022', 'Должно быть 12 мая')
        self.assertEqual(str(DateConverter('Jy yfv:12мая')), '12 мая 2022', 'Должно быть 12 мая')
        self.assertEqual(str(DateConverter('k;jhj 23 asd 11 ')), 'None', 'Должно быть ')
        self.assertEqual(str(DateConverter('12.. мая.. 2020')), '12 мая 2020', 'Должно быть 12 мая')
        self.assertEqual(str(DateConverter('12.. мая.. 2020')), '12 мая 2020', 'Должно быть 12 мая')
        self.assertEqual(str(DateConverter('k;jhj12 may 20 ')), '12 мая 2020', 'Должно быть ')
        self.assertEqual(str(DateConverter('k;jhj 12 may 20 ')), '12 мая 2020', 'Должно быть ')
        self.assertEqual(str(DateConverter('k;jhj12may201')), '12 мая 201', 'Должно быть ')
        self.assertEqual(str(DateConverter('k;jhj12may20111q')), '12 мая 2011', 'Должно быть ')
        self.assertEqual(str(DateConverter('k;jhj12may1')), '12 мая 2022', 'Должно быть ')
        self.assertEqual(str(DateConverter('k;jhj12.may1.201')), '12 мая 2022', 'Должно быть ')
        self.assertEqual(str(DateConverter('k;jhj:12:may:2021')), '12 мая 2021', 'Должно быть ')
        self.assertEqual(str(DateConverter('k;jhj_12_may_2021_')), '12 мая 2021', 'Должно быть ')
        self.assertEqual(str(DateConverter('13 МАЯ')), '13 мая 2022', 'Должно быть ')
        self.assertEqual(str(DateConverter('2022Г 13 ИЮНЯ')), '13 июня 2022', 'Должно быть ')

        # D M Y
        self.assertEqual(str(DateConverter('%12_05_2021%')), '12 мая 2021', 'Должно быть ')
        self.assertEqual(str(DateConverter('2022-05-29')), '29 мая 2022', 'Должно быть ')
        self.assertEqual(str(DateConverter('(12/ 5 / 21)/21/30')), 'None', 'Должно быть ')


if __name__ == '__main__':
    unittest.main()
