#bash

# generate the API code using docker + codegen
docker run --rm -v ${PWD}:/local swaggerapi/swagger-codegen-cli generate \
    -i "https://esi.tech.ccp.is/_latest/swagger.json" \
    -l python \
    -o /local/API

virtualenv venv

. venv/bin/activate

pip install -U setuptools pip wheel

if [ -e API/requirements.txt ]; then
    pip install -r API/requirements.txt -U
fi

if [ -e requirements.txt ]; then
    pip install -r requirements.txt -U
fi

echo "Copy config.example.py to config.py, and edit to have the right values for"
echo "your application.   ^Z this and come back when you are done."
echo "Hit return when ready to continue"
read garbage

# export FLASK_APP sso.py
python sso.py

echo "To run the app without using this script:  FLASK_APP=sso.py flask run"
