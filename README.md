# Strut Data Provider Search

Strut is a data search engine to make it easier for people to find datasets which will add value to their businesses. The system stores data on Data Providers and the Data Sets which those data providers sell. 

All included files constitute the beginnings of a backend for this application.

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### PIP Dependencies

All required Python libraries are located within the included requirements.txt file and can be installed by typing the following command:

```bash
pip install -r requirements.txt
```

## Database Setup
When running for the first time, uncomment line 21 in models.py "db.create_all()" to create the initial database tables. After the inital run it can be commented again.

## Running the server

To run the server, execute:

```bash
export FLASK_APP=app
export FLASK_ENV=development
export DATABASE_URL="postgres://username:password@host:port/database"
flask run
```

## Obtaining user credentials
Use the following link to log into the site:
https://nomaddata.auth0.com/authorize?audience=Strut%20Backend%20API&response_type=token&client_id=ACRZbPlNOSPJ4HN2z66v670g568QOyEp&redirect_uri=http://localhost:5000/login
The required JWT will be returned in the URL bar. The site you are redirected to will display nothing or an error. This is expecting since in a real deployment there would be a front-end to redirect to.

Two test users have been created
Admin User - Can perform all actions
admin@strut.com
udacityABC123

Normal User - Can only list data providers along with data provider details
normal@strut.com
udacityABC123

### Production site

The production site is hosted on Heroku at https://strutdata.herokuapp.com/

### API Usage details

A postman collection for this API can be downloaded at: https://www.getpostman.com/collections/4159a67a1ff9db8e430a
Documentation is located at: https://web.postman.co/collections/1771427-193f6bf1-96a9-495b-b6f0-a6551e21fa64?version=latest&workspace=8dfa1d5e-6e8c-4a86-8777-dddbc222615f

## Testing
To run the tests, run
```
python test_endpoints.py
```