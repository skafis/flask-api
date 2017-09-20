# flask-api
a api implementation with flask

# Usage
* to use or test the api, you first need to clone the remote repo to you local
  by ''' $git clone https://github.com/skafis/flask-api.git '''

  * setup a virtual enviroment and install the packages by running
     ''' $ pip install -r requirements.txt '''

 ### runing the app
* to run the app, in your terminal run
   * ''' $ export FLASK_APP="run.py" '''
   * ''' $ export APP_SETTINGS="development" '''
   * ''' $ export DATABASE_URL="postgresql://postgres:admin@localhost/test_db" '''
   * ''' $ export SECRET="this-is-the-secret-sauce"
 * then run 
   ''' $ flask run '''

### testing using post man or curl 

* to test in your terminal paste the curls 
	the endpoints are 
	/auth/register/
	/auth/login/
	/shopinglists/
	/shopinglists/1/

#/auth/register

*   '''$ curl -H "Accept: application/json" \
-H "Content-type: application/json" -X POST \
-d '{"email": "test@test.com", "password": "test"}' \
http://localhost:5000/auth/register'''

#/auth/login 
* '''$ curl -H "Accept: application/json" \
-H "Content-type: application/json" -X POST \
-d '{"email": "test@test.com", "password": "test"}' \
http://localhost:5000/auth/login'''

#/shopinglists/

* '''$ curl -H "Accept: application/json" \
-H "Content-type: application/json" -X POST \
-d '{"title": "Fruits"}' \
http://localhost:5000//shopinglists/'''

#/shopinglists/1/
* '''$ curl -H "Accept: application/json" \
-H "Content-type: application/json" -X POST \
-d '{"title": "Fruits"}' \
http://localhost:5000//shopinglists/'''