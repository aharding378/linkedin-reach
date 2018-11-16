# linkedin-reachWord guessing game for Linkedin REACH apprenticeship
By Alex Harding
Created 11/14/18

<h2>Setup</h2>

Please copy and paste these commands in your terminal to get the app up and running.

TIP: Create a virtual environment before proceeding. Visit http://flask.pocoo.org/docs/0.12/installation/ for instructions 

 1. pip install -r requirements.txt
 2. export FLASK_APP=app.py
 3. export FLASK_ENV=development
 4. export FLASK_DEBUG=1

You will then need to create a database table
 To do so, use an interactive python shell where you have this app loaded and type
 1. from app import db
 2. db.create_all()
 
This will create your new database

 That's it! now type: "flask run" in your commandline to start the application and go to http://127.0.0.1:5000/ in your browser to view the app
 
 This is what the app should look like:
 <img src="https://s3-us-west-1.amazonaws.com/my-media/images/Screen+Shot+2018-11-16+at+10.48.55+AM.png" />
 
 
 
 <h2>Tests</h2>
 The tests are written using unittest 
 
 to run the tests from the root directory use: python tests.py
 
 
