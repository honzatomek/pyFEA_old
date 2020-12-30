import unittest
import random
import logging

from misc.misc import *


class HelpFunctions(unittest.TestCase):
    def test_eng_default(self):
        vals = [random.random() * 10. ** random.uniform(-5.0, 5.0) for i in range(100)]
        for val in vals:
            self.assertTrue(abs((float(eng(val)) - val) / val) < 0.001)

    def test_eng_list(self):
        reply = '[[[ 1.0000E+00, 2.0000E+00, 3.0000E+00], [ 4.0000E+00, 5.0000E+00, 6.0000E+00]], [[ 7.0000E+00, 8.0000E+00, 9.0000E+00], [ 10.0000E+00, 11.0000E+00, 12.0000E+00]], 13.0000E+00]'
        vals = eval(reply)
        self.assertEqual(eng(vals, oneline=True), reply)
        reply = '[[ 1.0000E+00, 2.0000E+00, 3.0000E+00], [ 4.0000E+00, 5.0000E+00, 6.0000E+00], [ 7.0000E+00, 8.0000E+00, 9.0000E+00], [ 10.0000E+00, 11.0000E+00, 12.0000E+00], 13.0000E+00]'
        vals = eval(reply)
        self.assertEqual(eng(vals, oneline=True), reply)
        reply = '''     1.0000E+00     2.0000E+00     3.0000E+00
     4.0000E+00     5.0000E+00     6.0000E+00
     7.0000E+00     8.0000E+00     9.0000E+00
    10.0000E+00    11.0000E+00    12.0000E+00
    13.0000E+00'''
        self.assertEqual(eng(vals, oneline=False), reply)


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
        Data.set_locks(id_lock='unique', label_lock=None)
        d1 = Data(id=1, label='test data')
        with self.assertRaises(DuplicateIDError):
            d2 = Data(id=d1.id, label='test data 2')
        Data.set_locks(id_lock=None, label_lock=None)

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
        DataSet.set_locks(id_lock='unique', label_lock='unique')
        ds1 = DataSet(Data)
        self.assertTrue(ds1.id > 0)
        self.assertTrue(ds1.label != '')
        with self.assertRaises(DuplicateIDError):
            ds2 = DataSet(Data, id=ds1.id)
        with self.assertRaises(DuplicateLabelError):
            ds3 = DataSet(Data, label=ds1.label)
        DataSet.set_locks(id_lock=None, label_lock=None)

    def test_collect(self):
        ds1 = DataSet(Data)
        ds2 = DataSet(Data)
        for i in range(10):
            ds1._add_object(Data(i + 1))
            ds2._add_object(Data(i + 11))
        ds3 = DataSet.collect()
        del ds1
        del ds2
        self.assertEqual(ds3.count(), 20)

    def test_add_object(self):
        ds = DataSet(Data)
        num = 10
        for i in range(num):
            ds._add_object(Data(id=i + 1))
        self.assertEqual(ds.count(), num)

    def test_create_object(self):
        ds = DataSet(Data)
        num = 10
        for i in range(num):
            ds._create_object(Data, id=i+1)
        self.assertEqual(ds.count(), num)

        with self.assertRaises(TypeError):
            ds._create_object(int)

        dss = DataSet(Data)
        dss._create_object(DataSet, DataSet, id=num + 1)
        self.assertEqual(dss.count(), 1)

        dss2 = DataSet(DataSet)
        with self.assertRaises(TypeError):
            dss2._create_object(Data, id=num + 2)

    def test_get_objects_by_type(self):
        dss = DataSet(Data)
        numd = 5
        numds = 6
        for i in range(numd):
            dss._add_object(Data(i + 1))

        for i in range(numds):
            dss._add_object(DataSet(Data))

        objects = dss._get_objects_by_type()
        self.assertEqual(len(objects.keys()), 2)
        self.assertEqual(len(objects['Data']), numd)
        self.assertEqual(len(objects['DataSet']), numds)

    def test_repr(self):
        ds = DataSet(Data, id=1, label='test')
        num = 10
        for i in range(num):
            ds._add_object(Data(id=i + 1))
        expected_reply = '''DataSet(id=1, label='test')
DataSet.getID(1)._add_object(Data(id=1))
DataSet.getID(1)._add_object(Data(id=2))
DataSet.getID(1)._add_object(Data(id=3))
DataSet.getID(1)._add_object(Data(id=4))
DataSet.getID(1)._add_object(Data(id=5))
DataSet.getID(1)._add_object(Data(id=6))
DataSet.getID(1)._add_object(Data(id=7))
DataSet.getID(1)._add_object(Data(id=8))
DataSet.getID(1)._add_object(Data(id=9))
DataSet.getID(1)._add_object(Data(id=10))'''
        self.assertEqual(repr(ds), expected_reply)

    def test_str(self):
        ds = DataSet(Data)
        num = 10
        for i in range(num):
            ds._add_object(Data(id=i + 1))
        expected_reply = '''$GENERIC TYPE = Data
            1
            2
            3
            4
            5
            6
            7
            8
            9
           10
'''
        self.assertEqual(str(ds), expected_reply)

    def test_iterator(self):
        ds = DataSet(Data)
        num = 10
        for i in range(num):
            ds._add_object(Data(id=i + 1))

        for i, data in enumerate(ds):
            self.assertEqual(data.id, i + 1)

    def test_get(self):
        ds = DataSet(Data)
        ds._add_object(Data(id=1, label='test1'))
        ds._add_object(Data(id=2, label='test2'))
        self.assertEqual(ds.get(1).label, 'test1')
        self.assertEqual(ds.get('test2').id, 2)


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.disabled = True
    logging.disable(logging.FATAL)
    unittest.main(verbosity=2)
