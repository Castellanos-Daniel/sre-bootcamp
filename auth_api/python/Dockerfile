FROM python:3-alpine

# Add your instructions to dockerize the application
# App must run on port 8000

COPY ./requirements.txt /requirements.txt

RUN pip install -r requirements.txt

COPY ./ /

# Change this part to point to the right python script
CMD [ "python", "/api.py" ]