import unittest
import datetime
import sys

sys.path.insert(0, '..')

import db

class Test(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        db.session.rollback()

    def test_insert(self):
        test_list = [{'number': 60, 'text': 'testtext'}]
        db.Result.upload(test_list)
        saved_result = db.session.query(db.Result).filter(db.Result.number == 60).filter(db.Result.text == 'testtext').first()
        self.assertEqual(saved_result.text, 'testtext')

    def test_closest(self):
        test_closest = [{'number': 90, 'text': '90test'}]
        db.Result.upload(test_closest)
        rows_closest = db.Result.get_closest(91, 0, 1)
        self.assertEqual(rows_closest[0].text, '90test')

    def test_viewer(self):
        test_result = db.Result(text='testtest', number=100, ins_date=datetime.datetime(2017, 10, 16))
        viewer = db.ResultViewer([test_result])
        output = viewer.output_json(1)
        self.assertIsInstance(output, dict)

    def test_multiple_inserts(self):
        test_list = [{'number': 60, 'text': 'testtext1'}, {'number': 61, 'text': 'testtext2'}]
        db.Result.upload(test_list)
        saved_result1 = db.session.query(db.Result).filter(db.Result.number == 60).filter(db.Result.text == 'testtext1').first()
        saved_result2 = db.session.query(db.Result).filter(db.Result.number == 61).filter(db.Result.text == 'testtext2').first()
        self.assertEqual(saved_result1.text, 'testtext1')
        self.assertEqual(saved_result2.text, 'testtext2')

    def test_no_closest(self):
        test_closest = [{'number': 90, 'text': '90test'}]
        db.Result.upload(test_closest)
        rows_closest = db.Result.get_closest(100, 0, 1)
        self.assertEqual(len(rows_closest), 0)

if __name__ == "__main__":
    unittest.main()
