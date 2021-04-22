import os
import unittest

from flask_sqlalchemy import SQLAlchemy

from app import create_app

database_filename = "testing.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))


class Tests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True

        with self.app.app_context():
            self.client = self.app.test_client
            self.app.config["SQLALCHEMY_DATABASE_URI"] = database_path
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.drop_all()
            self.db.create_all()

        self.director = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkpDUFB4bUYzOWFhWTAyNUt2aWlrQSJ9.eyJpc3MiOiJodHRwczovL2Rldi15MjV3ZTU0aS5ldS5hdXRoMC5jb20vIiwic3ViIjoiMTJRVzhocFBkQnpsdEZ6OWFhU3kwVWQ5WENtcFRqMGJAY2xpZW50cyIsImF1ZCI6IlppQ2Fwc3RvbmUiLCJpYXQiOjE1OTA1ODMzMTgsImV4cCI6MTU5MDY2OTcxOCwiYXpwIjoiMTJRVzhocFBkQnpsdEZ6OWFhU3kwVWQ5WENtcFRqMGIiLCJzY29wZSI6ImdldDptb3ZpZXMgZ2V0OmFjdG9ycyBwb3N0Om1vdmllcyBwb3N0OmFjdG9ycyBwYXRjaDptb3ZpZXMgcGF0Y2g6YWN0b3JzIGRlbGV0ZTptb3ZpZXMgZGVsZXRlOmFjdG9ycyIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsInBlcm1pc3Npb25zIjpbImdldDptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwicG9zdDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBhdGNoOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIl19.MfKt9hk4IqbA5z9x6t1Ypi11XxYqSDcCBlQE54WHOCTXYmQ-DCKsC5WNaFB60se1OWNvKHzvj8YMCCIAyITu9zXgC4MwnVclusZiq73EKnxfBtIuG7VGqMoAwgWEHiQb9GCx_CGfJVTrcAIESwvne0UbIpEQXD07oSpeVeS2l7-tt8UKf8-aO95JdVPxad6FV1bT35UVscj94d_6a-jfkWLkJuhJlt4Q0QMsyVdg2UbRzGU7nmEiLDpkZb3k_VlIYpTMoDs8nBXW_pmjDOuu2x4r7EcilwynUZ7VjTqzWBfl6L-g5-cejNHSwOCZottoV67j7FPFbaLpgyWvbOi-9A'

        self.headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.director}

        self.newMovie = {
            'title': 'Movie 1',
            'movie_date': '2020-01-01T00:00:00'
        }
        self.newActor = {
            'name': 'Actor 1',
            'age': 22,
            'gender': 'Unkown'
        }
        self.otherMovie = {
            'title': 'Movie 1',
            'movie_date': '2020-01-01T00:00:00',
            'actors': [self.newActor]
        }
        self.otherActor = {
            'name': 'Actor 1',
            'age': 23,
            'gender': 'Still Unkown'
        }
        pass

    def tearDown(self):
        pass

    def testGET(self):
        res = self.client().get('/movies')
        self.assertEqual(res.status_code, 401)

        res = self.client().get(
            '/movies',
            headers=self.headers)
        self.assertEqual(res.status_code, 200)

        res = self.client().get('/actors')
        self.assertEqual(res.status_code, 401)

        res = self.client().get(
            '/actors',
            headers=self.headers)
        self.assertEqual(res.status_code, 200)

    def testPOST(self):
        res = self.client().post('/movies', json=self.newMovie)
        self.assertEqual(res.status_code, 401)

        res = self.client().post('/actors', json=self.newActor)
        self.assertEqual(res.status_code, 401)

        res = self.client().post(
            '/movies',
            headers=self.headers,
            json=self.newMovie)
        self.assertEqual(res.status_code, 200)

        res = self.client().post(
            '/actors',
            headers=self.headers,
            json=self.newActor)
        self.assertEqual(res.status_code, 200)

    def testPATCH(self):
        self.client().post(
            '/movies',
            headers=self.headers,
            json=self.newMovie)

        self.client().post(
            '/actors',
            headers=self.headers,
            json=self.newActor)

        res = self.client().patch('/movies/1', json=self.otherMovie)
        self.assertEqual(res.status_code, 401)

        res = self.client().patch('/actors/1', json=self.otherActor)
        self.assertEqual(res.status_code, 401)

        res = self.client().patch(
            '/movies/1',
            headers=self.headers,
            json=self.otherMovie)
        self.assertEqual(res.status_code, 200)

        res = self.client().patch(
            '/actors/1',
            headers=self.headers,
            json=self.otherActor)
        self.assertEqual(res.status_code, 200)

        res = self.client().patch(
            '/movies/5',
            headers=self.headers,
            json=self.otherMovie)
        self.assertEqual(res.status_code, 404)

        res = self.client().patch(
            '/actors/5',
            headers=self.headers,
            json=self.otherActor)
        self.assertEqual(res.status_code, 404)

    def testDELETE(self):
        res = self.client().delete('/movies/1')
        self.assertEqual(res.status_code, 401)

        res = self.client().delete('/actors/1')
        self.assertEqual(res.status_code, 401)

        res = self.client().delete(
            '/movies/5',
            headers=self.headers)
        self.assertEqual(res.status_code, 404)

        res = self.client().delete(
            '/actors/5',
            headers=self.headers)
        self.assertEqual(res.status_code, 404)

        res = self.client().delete(
            '/movies/1',
            headers=self.headers)
        self.assertEqual(res.status_code, 200)

        res = self.client().delete(
            '/actors/1',
            headers=self.headers)
        self.assertEquals(res.status_code, 200)


if __name__ == '__main__':
    unittest.main()
