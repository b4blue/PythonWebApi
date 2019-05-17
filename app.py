from flask import Flask
from config import client
from bson.objectid import ObjectId
from bson.json_util import dumps
from flask import request, jsonify
import json
import ast
import importlib

app = Flask(__name__)

# Select the database
db = client.restfulapi
# Select the collection
collection = db.users


@app.route('/data/<user_id>', methods=['GET'])
def get_data(user_id):
    try:
        record_fetched = collection.find_one({'_id': ObjectId(str(user_id))})
        if record_fetched:
            # Prepare the response
            return dumps(record_fetched)
        else:
            # No records are found
            return "Not found", 404
    except Exception as e:
        print(e)
        return "Bad request", 400


@app.route('/data', methods=['GET'])
def get_data_multiple():
    try:
        records_fetched = collection.find()
        if records_fetched.count() > 0:
            # Prepare the response
            return dumps(records_fetched)
        else:
            # No records are found
            return "No data", 404
    except:
        return "", 400


@app.route("/data", methods=['POST'])
def post_data():
    try:
        # Create new users
        try:
            body = ast.literal_eval(json.dumps(request.get_json()))
        except:
            # Bad request as request body is not available
            # Add message for debugging purpose
            return "", 400

        record_created = collection.insert(body)
        return dumps(collection.find_one({'_id': ObjectId(str(record_created))})), 201

    except:
        # Error while trying to create the resource
        # Add message for debugging purpose
        return "", 500


@app.route("/data/<user_id>", methods=['PUT'])
def update_data(user_id):
    try:
        # Get the value which needs to be updated
        try:
            body = request.get_json()
        except Exception as e:
            print(e)
            # Bad request as the request body is not available
            # Add message for debugging purpose
            return "", 400

        try:
            check = collection.find_one({'_id': ObjectId(str(user_id))})

            if check:
                print('everything is fine')
            else:
                return "Not found", 404
        except:
            return "Bad request", 400

        # Updating the user
        records_updated = collection.update_one({"_id": ObjectId(str(user_id))}, {"$set": {"data": body["data"]}})

        # Check if resource is updated
        if records_updated:
            # Prepare the response as resource is updated successfully
            record_fetched = collection.find_one({'_id': ObjectId(str(user_id))})
            return dumps(record_fetched)
        else:
            # Bad request as the resource is not available to update
            # Add message for debugging purpose
            return "Not found", 404
    except Exception as e:
        print(e)
        # Error while trying to update the resource
        # Add message for debugging purpose
        return "", 500


if __name__ == '__main__':
    app.run()
