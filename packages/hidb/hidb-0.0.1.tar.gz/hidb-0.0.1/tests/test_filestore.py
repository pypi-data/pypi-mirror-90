import os
import time
import unittest
import tempfile

from hidb import fileStoreDB

test_data = {
    "test1": "value",
    "test2": 12,
    "test3": [12, 23, 34],
}


class TestFilestoreDB(unittest.TestCase):
    def test_one(self):
        # Test for create, read
        with tempfile.TemporaryDirectory() as tempdir:
            db = fileStoreDB(tempdir)
            db.create("test_data", test_data)
            self.assertEqual(db.read("test_data"), test_data)
            self.assertIsInstance(db.read("test_data"), dict)
            with self.assertRaises(KeyError):
                db.read("test_data2")

    def test_two(self):
        # Test for delete
        with tempfile.TemporaryDirectory() as tempdir:
            db = fileStoreDB(tempdir)
            db.create("test_data", test_data)
            self.assertEqual(db.read("test_data"), test_data)
            db.delete("test_data")
            with self.assertRaises(KeyError):
                db.read("test_data")

    def test_three(self):
        # Test for save data
        with tempfile.TemporaryDirectory() as tempdir:
            db = fileStoreDB(tempdir)
            db.create("test_data", test_data)
            db.saveData("testfile.pk")
            self.assertTrue(os.path.isfile("testfile.pk"))

    def test_four(self):
        # Test for save data and load data
        with tempfile.TemporaryDirectory() as tempdir:
            db = fileStoreDB(tempdir)
            db.create("test_data", test_data)
            db.saveData("testfile.pk")
            self.assertTrue(os.path.isfile("testfile.pk"))
            db2 = fileStoreDB(tempdir)
            db2.loadData("testfile.pk")
            self.assertEqual(db2.read("test_data"), test_data)

    def test_five(self):
        # Test for time to live parameter
        with tempfile.TemporaryDirectory() as tempdir:
            db = fileStoreDB(tempdir)
            db.create("test_data", test_data, 10)
            db.create("test_data2", test_data, 20)
            self.assertEqual(db.read("test_data"), test_data)
            self.assertEqual(db.read("test_data2"), test_data)
            time.sleep(10)
            with self.assertRaises(KeyError):
                db.read("test_data")
            self.assertEqual(db.read("test_data2"), test_data)
            time.sleep(10)
            with self.assertRaises(KeyError):
                db.read("test_data2")
