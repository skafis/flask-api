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

### testing using post man

* in your postman app, use this link 
  ''' http://127.0.0.1:5000/shopinglists '''

  now you can add items to list 
  by adding 
  {
  	'title': 'Fruits'
  }
