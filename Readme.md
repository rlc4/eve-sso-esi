### Example SSO & API usage for ESI

A short example in python using Flask and ESI swagger_client

#### Requirements

* Python set up with pip available
* Docker set up and ready to run docker instances

#### Instructions

* Once the requirements have been met, run setup.py.  This will do a bunch of
work for you:
  * Generate the swagger_client for python using docker (the methods listed on the page
    you've likely been reading are currently all broken).
  * Create a virtualenv to keep dependencies and other stuff off of your global Python
    installation
  * Install all of the requirements for the swagger_client and for the sample application
  * Run the application for the first time so you can see it going
* Point a browser at localhost:8888 (or if you've changed the port number
  in config, to that port number)
* Play with it!

After the initial demonstration, to re-run the application from the command
line on your own, you will want to do the following:

1. . venv/bin/activate  
2. FLASK_APP=sso.py flask run  # do this as many times as you want as you test things out
3. deactivate   # ends your virtualenv session

#### Comments

Please provide feedback if there are ways that this can be simplified for clarity.
