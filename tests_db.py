import unittest
import asyncio
import aiohttp
import datetime
import sys

#я проиграл директориям
sys.path.insert(0,'..')

import db

class Test(unittest.TestCase):
    def setUp(self):
        pass
 
    def tearDown(self):
        db.session.rollback()

    def test_insert(self):
        test_list = [{'number':60, 'text':'testtext'}]
        db.Result.upload(test_list)
        saved_result = db.session.query(db.Result).filter(db.Result.number == 60).filter(db.Result.text == 'testtext').first()
        self.assertEqual(saved_result.__dict__.pop('text'), test_list.pop().pop('text'))

    def test_closest(self):
        test_closest = [{'number':90, 'text':'90test'}]
        db.Result.upload(test_closest)
        rows_closest = db.Result.get_closest(91, 0, 1)
        self.assertEqual(rows_closest.pop().__dict__.pop('text'), test_closest.pop().pop('text'))
        
    def test_viewer(self):
        test_result = db.Result(text='testtest', number=100, ins_date=datetime.datetime(2017,10,16))
        viewer = db.ResultViewer([test_result])
        output = viewer.output_json(1)
        self.assertEqual(type(output).__name__, 'dict')
        
    
if __name__ == "__main__":
    unittest.main()
