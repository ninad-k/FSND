### Motivation

This is my work on the final project (Capstone) for the Full Stack Nanodegree of Udacity. It utilizes everything learned
during the program, from the python language to the deployment on heroku, through auth0 authentification and relational
databases.

### Postman

Included in the project folder is a postman collection of endpoint tests with the bearer token for the Executive
Producer authorization.

### Installation of requirements

Installation requires the following steps:

1. Download Pyhton from https://www.python.org/downloads/ and install.
2. Open a console, such as command promt or git bash.
3. Python installation should come with pip. Use "pip --version" to check if it is indeed installed. 4.a If pip is not
   installed, download it from https://pypi.org/project/pip/#files
   4.b If/Once pip is installed, run "python -m pip install –upgrade pip" to upgrade pip to the latest version.
5. Use the chosen console to navigate to the project directory.
6. Once in the project directory, run "pip install -r requirements.txt" to install the project requirements.
7. Run setup.sh to set up the environment variables.
8. Run "export FLASK_APP=app".
9. Run "flask run" to deploy the server. To run the tests, run "python -m unittest test_app.py"

### Endpoints

GET '/movies' GET '/actors' POST '/movies' POST '/actors' PATCH '/movies/<int:id>'
PATCH '/actors/<int:id>'
DELETE '/movies/<int:id>'
DELETE '/actors/<int:id>'

GET '/movies'

- Fetches a list of all movies in the databases.
- Required Authorization: Casting Assistant or Casting Director or Executive Producer.
- Request Arguments: None.
- Returns a JSON object containing a list of all movie objects and "success: True":
  [{
  'title': 'Movie 1',
  'movie_date': '2020-01-01T00:00:00',
  'actors': [{
  'name': 'Actor 1',
  'age': 22,
  'gender': 'Unkown' }],
  'success': True }]

GET '/actors'

- Fetches a list of all actors in the database
- Required Authorization: Casting Assistant or Casting Director or Executive Producer.
- Request Arguments: None.
- Returns a JSON object containing a list of all actor objects and "success: True":
  {{
  'name': 'Actor 1',
  'age': 22,
  'gender': 'Unkown' }]

POST '/movies'

- Adds a new movie to the database.
- Required Authorization: Executive Producer.
- Request Arguments: <varchar:title>, <datetime:date>; date must be of format: YYYY-MM-DDTHH:MM:SS
- Returns a JSON object containing "success: True" and the new movie title:
  {
  "success": True,
  "Movie": "Movie 1"
  }

POST '/actors'

- Adds a new actor to the database.
- Required Authorization: Casting Director or Executive Producer.
- Request Arguments: <varchar:name>, <int:age>, <varchar:gender>.
- Returns a JSON object containing "success: True" and the new actor's name:
  {
  "success": True,
  "Actor": "Actor 1"
  }

PATCH '/movies/<int:id>'

- Updates an existing movie entry of id id.
- Required Authorization: Casting Director or Executive Producer.
- Request Arguments: <varchar:title>, <datetime:date>, <List<Actor>:actors>; date must be of format: YYYY-MM-DDTHH:MM:
  SS; actors must be a list of actors.
- Returns a JSON object containing "success: True" and the updated movie's title:
  {
  "Success": True,
  "Movie": "Movie 1a"
  }

PATCH '/actors/<int:id>'

- Updates an existing actor entry of id id.
- Required Authorization: Casting Director or Executive Producer.
- Request Arguments: <varchar:name>, <int:age>, <varchar:gender>.
- Returns a JSON object containing "success: True" and the updated actor's title:
  {
  "Success": True,
  "Actor": "Actor 1 a"
  }

DELETE '/movies/<int:id>'

- Removes the movie of id id.
- Required Authorization: Executive Producer.
- Request Arguments: None.
- Returns a JSON object containing "success: True"
  {
  "Sucess": True }

DELETE '/actors/<int:id>'

- Removes the actor of id id.
- Required Authorization: Executive Producer.
- Request Arguments: None.
- Returns a JSON object containing "success: True"
  {
  "Sucess": True }

### Error handlers

- 404 Not Found {
  'error': 404,
  'message': "Not Found"
  }

- 400 Bad Request {
  'error': 400,
  'message': "Bad Request"
  }

- 401 Unauthorized {
  'error': 401,
  'message': "Unauthorized"
  }

### heroku URL

https://aas-capstone.herokuapp.com/

### Bearer token valid as of time of submission:

eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkpDUFB4bUYzOWFhWTAyNUt2aWlrQSJ9.eyJpc3MiOiJodHRwczovL2Rldi15MjV3ZTU0aS5ldS5hdXRoMC5jb20vIiwic3ViIjoiMTJRVzhocFBkQnpsdEZ6OWFhU3kwVWQ5WENtcFRqMGJAY2xpZW50cyIsImF1ZCI6IlppQ2Fwc3RvbmUiLCJpYXQiOjE1OTA1ODMzMTgsImV4cCI6MTU5MDY2OTcxOCwiYXpwIjoiMTJRVzhocFBkQnpsdEZ6OWFhU3kwVWQ5WENtcFRqMGIiLCJzY29wZSI6ImdldDptb3ZpZXMgZ2V0OmFjdG9ycyBwb3N0Om1vdmllcyBwb3N0OmFjdG9ycyBwYXRjaDptb3ZpZXMgcGF0Y2g6YWN0b3JzIGRlbGV0ZTptb3ZpZXMgZGVsZXRlOmFjdG9ycyIsImd0eSI6ImNsaWVudC1jcmVkZW50aWFscyIsInBlcm1pc3Npb25zIjpbImdldDptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwicG9zdDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBhdGNoOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIl19.MfKt9hk4IqbA5z9x6t1Ypi11XxYqSDcCBlQE54WHOCTXYmQ-DCKsC5WNaFB60se1OWNvKHzvj8YMCCIAyITu9zXgC4MwnVclusZiq73EKnxfBtIuG7VGqMoAwgWEHiQb9GCx_CGfJVTrcAIESwvne0UbIpEQXD07oSpeVeS2l7-tt8UKf8-aO95JdVPxad6FV1bT35UVscj94d_6a-jfkWLkJuhJlt4Q0QMsyVdg2UbRzGU7nmEiLDpkZb3k_VlIYpTMoDs8nBXW_pmjDOuu2x4r7EcilwynUZ7VjTqzWBfl6L-g5-cejNHSwOCZottoV67j7FPFbaLpgyWvbOi-9A
