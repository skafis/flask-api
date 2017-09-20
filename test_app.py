import unittest
import os
import json
from app import create_app, db

class ShoppingList(unittest.TestCase):

    def setUp(self):
        """initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.shopinglist = {'name': 'Grocery'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_list_creation(self):
        """Test API can create a shoppinglist (POST request)"""
        res = self.client().post('/shopinglist/', data=self.shopinglist)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Grocery, str(res.data))

    def test_get_all_list(self):
        """Test API can get evrything in shopping list (GET request)."""
        res = self.client().post('/shoppinglists/', data=self.shopinglist)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/shoppinglists/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Grocery', str(res.data))

    def test_api_get_by_id(self):
        """Test API can get list by using it's id."""
        rv = self.client().post('/shoppinglists/', data=self.shoppinglist)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/shoppinglists/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Grocery', str(result.data))

    def test_list_is_editable(self):
        """Edit shopping list. (PUT request)"""
        rv = self.client().post(
            '/shoppinglists/',
            data={'name': 'meaty things'})
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put(
            '/shoppinglists/1',
            data={
                "name": "sweet meaty objects"
            })
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/shoppinglists/1')
        self.assertIn('meaty', str(results.data))

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()