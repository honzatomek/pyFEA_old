import unittest
import random
import logging

from misc.misc import *


class HelpFunctions(unittest.TestCase):
    def test_format_eng_default(self):
        vals = [random.random() * 10. ** random.uniform(-5.0, 5.0) for i in range(100)]
        for val in vals:
            self.assertTrue(abs((float(format_eng(val)) - val) / val) < 0.001)


class TestData(unittest.TestCase):
    def test_init(self):
        d1 = Data(id=1, label='test data')
        self.assertEqual(d1.id, 1)
        self.assertEqual(d1.label, 'test data')
        with self.assertRaises(AttributeError):
            d2 = Data(id='test')

    def test_add_del(self):
        d = Data(id=1, label='test data')
        self.assertEqual(Data.count(), 1)
        self.assertTrue(Data.id_exists(1))
        del d
        self.assertEqual(Data.count(), 0)
        self.assertFalse(Data.id_exists(1))

    def test_duplicate(self):
        d1 = Data(id=1, label='test data')
        with self.assertRaises(DuplicateIDError):
            d2 = Data(id=d1.id, label='test data 2')

    def test_next_free_id(self):
        d = Data(id=100, label='test data')
        self.assertEqual(Data.next_free_id(), 101)

    def test_get_id(self):
        d1 = Data(id=1, label='test data')
        d2 = Data.getID(d1.id)
        self.assertIs(d1, d2)

    def test_id_exists(self):
        d = Data(id=100, label='test data')
        self.assertTrue(Data.id_exists(100))
        self.assertFalse(Data.id_exists(101))

    def test_next_free_label(self):
        d = Data(id=100, label=f'{Data._command:10s}'.strip(' ') + '_00001')
        self.assertEqual(Data.next_free_label(), f'{Data._command:10s}'.strip(' ') + '_00002')

    def test_get_label(self):
        d1 = Data(label='steel')
        d2 = Data.getLabel(d1.label)
        self.assertIs(d1, d2)

    def test_label_exists(self):
        d = Data(label='steel')
        self.assertTrue(Data.label_exists(d.label))
        self.assertFalse(Data.label_exists('dummy'))

    def test_get_type(self):
        d1 = Data(id=100, label='test data')
        d2 = list(Data.getType(type(d1)))[0]
        self.assertIs(d1, d2)

    def test_repr(self):
        d1 = Data(id=100, label='test data')
        self.assertEqual(repr(d1), "Data(id=100, label='test data')")
        d2 = Data(id=101)
        self.assertEqual(repr(d2), "Data(id=101)")

    def test_str(self):
        d1 = Data(id=100, label='test data')
        self.assertEqual(str(d1).rstrip(' '), "          100 'test data'")
        d2 = Data(id=101, label='test_data')
        self.assertEqual(str(d2).rstrip(' '), "          101 test_data")
        d3 = Data(id=102)
        self.assertEqual(str(d3).rstrip(' '), "          102")


class TestDataSet(unittest.TestCase):
    def test_init(self):
        ds = DataSet(Data)
        print(ds.id)
        print(ds.label)
        ds._add_object(Data(id=100))
        ds._add_object(Data(id=101))
        ds._add_object(Data(id=102))
        ds._add_object(Data(id=104))
        print(repr(ds))
        print(str(ds))


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.disabled = True
    unittest.main(verbosity=2)
