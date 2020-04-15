import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, DataProvider, Dataset

def make_request_with_auth(self, endpoint, method='GET', jwt=None, data=None):
    methods = {
        'GET': self.client().get,
        'POST': self.client().post,
        'PATCH': self.client().patch,
        'DELETE': self.client().delete
    }

    header = {'Authorization': jwt}

    if method in ['POST', 'PATCH']:
        header['Content-Type'] = 'application/json'


    if data is None:
        res = methods[method](endpoint, headers=header)
    else:
        res = methods[method](endpoint, headers=header, json=data)

    return res
    

class StrutTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.normalJWT = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkhNZXZuT2ZCdzVpbkJ3R0Eza1NNWiJ9.eyJpc3MiOiJodHRwczovL25vbWFkZGF0YS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU5MzM4Y2IxNWRmOGEwYzU2ZWE4NjQ4IiwiYXVkIjoiU3RydXQgQmFja2VuZCBBUEkiLCJpYXQiOjE1ODY5ODEwODAsImV4cCI6MTU4NzA1MzA4MCwiYXpwIjoiQUNSWmJQbE5PU1BKNEhOMno2NnY2NzBnNTY4UU95RXAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbInJlYWQ6cHJvdmlkZXItZGV0YWlscyIsInJlYWQ6cHJvdmlkZXItbGlzdCJdfQ.P4dGcIPk2SJtpVNpIlV85NtUVAEa3sOIcZZIdrVGfdRsMOssoNH-X4IFahZPkF6gGiD8JeWnzX-XIAQpHjblEjBr8GbD8k-VT3XUYdZkxX1iQp6FqwUlFd7YGPO-01WblgPfnacrfxkbfsebs67fHsWnOpIsEajrFZyRNs8qjJbthZIaf9ZVnfNBr7BU-4VTPz7oxQEsoyuWFRKbO6RE0lCd-wUBX7MIla2a3sy-p3gmNSEc2GKlHStn3p34MDlN4Qf4gG4q_HeQ1ydFhpi3xOYQU41391E0rkxjWGKmLSav4OX0JKlF-cBWIdqiJK0HyD5_J5MpKD6XVZcnRQ_C-w'
        self.adminJWT =  'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkhNZXZuT2ZCdzVpbkJ3R0Eza1NNWiJ9.eyJpc3MiOiJodHRwczovL25vbWFkZGF0YS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU4ZmQ4OGVhNTU0ZGYwYzA0OTdmZWJhIiwiYXVkIjoiU3RydXQgQmFja2VuZCBBUEkiLCJpYXQiOjE1ODY5NzkzNDksImV4cCI6MTU4NzA1MTM0OSwiYXpwIjoiQUNSWmJQbE5PU1BKNEhOMno2NnY2NzBnNTY4UU95RXAiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImNyZWF0ZTpkYXRhc2V0IiwiY3JlYXRlOnByb3ZpZGVyIiwiZGVsZXRlOnByb3ZpZGVyIiwicGF0Y2g6cHJvdmlkZXIiLCJyZWFkOnByb3ZpZGVyLWRldGFpbHMiLCJyZWFkOnByb3ZpZGVyLWxpc3QiXX0.p3wTv--l1QLkp0M2prOKQOofUYPhZRi-Vji-OkofRdBfoYnN5knuUeMrvwo0GupIm65DRTiJfHFcc2QH1e_T10H7RotBPf-Cz4eFxU3wUprDoflkFGru1LN4An6MSr6FtdBIqW2MGiBybNj2V7VDPNy6DrPnqrl-4m_gEdjIKVUpxa0EpfVzLQ7NN-GCAuAktq8XeEbCBjMbPq5ForAHnFm9-smmDObV9qofJaWc1MoIS2JDe7i_klIHJwpF9fVNSO5z19-qzmBc6TtbUj7G2lAq3wy6iytSGj6A7hGvtrG6D-JTbaCI3Uuaft82yo709Lu8DNd6UO0qvT0a9dboqA'
        
        self.database_path = os.environ['DATABASE_URL']
        
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_providers(self):
        res = make_request_with_auth(self, '/providers', method='GET')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['providers'])
        self.assertNotEqual(len(data['providers']), 0)

    def test_get_provider_details_auth(self):
        # Test without logging in
        res = make_request_with_auth(self, '/providers/1', method='GET')
        data = json.loads(res.data)

        # Test logged in as normal user
        res = make_request_with_auth(self, '/providers/1', method='GET', jwt=self.normalJWT)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['provider'])

        # Test error case
        res = make_request_with_auth(self, '/providers/10000', method='GET', jwt=self.normalJWT)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

        # Test as admin
        res = make_request_with_auth(self, '/providers/1', method='GET', jwt=self.adminJWT)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['provider'])

    def test_add_provider(self):
        bodydata = {
                    'name': 'Money Dashboard 2',
                    'description': 'Test Description',
                    'biases': 'No biases.'
                }
        
        # Test without logging in
        res = make_request_with_auth(self, '/providers', method='POST', data=bodydata)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

        # Test logged in as normal user
        res = make_request_with_auth(self, '/providers', method='POST', data=bodydata, jwt=self.normalJWT)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

        # Test logged in as an admin
        res = make_request_with_auth(self, '/providers', method='POST', data=bodydata, jwt=self.adminJWT)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['provider_id'])

        # Test error case missing name field
        bodydata = {
                    'description': 'Test Description',
                    'biases': 'No biases.'
                }
        
        res = make_request_with_auth(self, '/providers', method='POST', data=bodydata, jwt=self.adminJWT)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_add_dataset(self):
        bodydata = {
                    'name': 'Test Dataset',
                    'description': 'Test Description',
                    'type': 'No type',
                    'provider_id': 5
                }
        
        # Test without logging in
        res = make_request_with_auth(self, '/datasets', method='POST', data=bodydata)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

        # Test logged in as normal user
        res = make_request_with_auth(self, '/datasets', method='POST', data=bodydata, jwt=self.normalJWT)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

        # Test logged in as an admin
        res = make_request_with_auth(self, '/datasets', method='POST', data=bodydata, jwt=self.adminJWT)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['dataset_id'])

        # Test error case missing fields
        bodydata = {
                    'description': 'Test Description',
                    'name': 'Name'
                }
        
        res = make_request_with_auth(self, '/datasets', method='POST', data=bodydata, jwt=self.adminJWT)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_update_provider(self):
        provider = DataProvider.query.order_by(DataProvider.id.desc()).first()
        provider_id = str(provider.id)

        bodydata = {
                    'name': 'patched name',
                    'description': 'patched Description',
                    'biases': 'patched biases'
                }
        
        # Test without logging in
        res = make_request_with_auth(self, '/providers/' + provider_id, method='PATCH', data=bodydata)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

        # Test logged in as normal user
        res = make_request_with_auth(self, '/providers/' + provider_id, method='PATCH', data=bodydata, jwt=self.normalJWT)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

        # Test logged in as an admin
        res = make_request_with_auth(self, '/providers/' + provider_id, method='PATCH', data=bodydata, jwt=self.adminJWT)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['provider_id'], provider.id)

        # Test error case missing fields
        bodydata = {
                    'description': 'Test Description'
                }
        
        res = make_request_with_auth(self, '/providers/' + provider_id, method='PATCH', data=bodydata, jwt=self.adminJWT)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

    def test_delete_provider(self):
        provider = DataProvider.query.order_by(DataProvider.id.desc()).first()
        provider_id = str(provider.id)

        # Test without logging in
        res = make_request_with_auth(self, '/providers/' + provider_id, method='DELETE')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

        # Test logged in as normal user
        res = make_request_with_auth(self, '/providers/' + provider_id, method='DELETE', jwt=self.normalJWT)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

        # Test logged in as an admin
        res = make_request_with_auth(self, '/providers/' + provider_id, method='DELETE', jwt=self.adminJWT)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['deleted'])

        # Test error case with incorrect id
        res = make_request_with_auth(self, '/providers/10000', method='DELETE', jwt=self.adminJWT)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
