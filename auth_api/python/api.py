from os import getenv
from dotenv import load_dotenv, find_dotenv
from flask import Flask, request, jsonify
from flask.helpers import make_response
from methods import Token, Restricted

load_dotenv(find_dotenv())
app = Flask(__name__)
login = Token()
protected = Restricted()


# Just a health check
@app.route("/")
def url_root():
    return {"Status": "OK"}

# Just a health check


@app.route("/_health")
def url_health():
    return {"Status": "OK"}


# e.g. http://127.0.0.1:8000/login
@app.route("/login", methods=['POST'])
def url_login():

    try:
        username = request.form['username']
        password = request.form['password']

        token = login.generate_token(username, password)

        if token:
            response = make_response(
                jsonify({
                    "message": "Succcess",
                    "data": token}), 200,
            )
            response.headers["Content-Type"] = "application/json"

        else:
            response = make_response(
                jsonify({"message": "Access Denied"}), 403,
            )
            response.headers["Content-Type"] = "application/json"

        return response

    except Exception as e:
        response = make_response(
            jsonify({"message": "Access Denied",
                     "error": str(e)}), 403,
        )
        response.headers["Content-Type"] = "application/json"
        return response


# # e.g. http://127.0.0.1:8000/protected
@app.route("/protected")
def url_protected():
    auth_token = request.headers.get('Authorization')

    access_data = protected.access_data(auth_token)

    print(access_data)

    if access_data:
        response = make_response(
            jsonify({"data": access_data}), 200)
        response.headers["Content-Type"] = "application/json"
    else:
        response = make_response(
            jsonify({"data": "Access denied"}), 403)
        response.headers["Content-Type"] = "application/json"

    return response


if __name__ == '__main__':
    app.run(debug=True, host=getenv('API_HOST'), port=getenv('PORT'))
