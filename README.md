# dev
Website developed for the application process at BriteCore, done with Vue.js and Django Rest Framework

# Setup

Install the Pipfile and package.json (under the front/ folder), then make sure your aws credentials are setup properly and finally run deploy.py.

# Populating the DB

After deploying, the database will be empty, so there will be nothing to render on the frontend. You can interact with the backend by using tools like curl, httpie, or by enabling the Django REST Framework browsable API.  

With curl, try the following for setting up a sample RiskType that contains all the possible field types. Note that the content-type must be valid json, and that enum fields are defined with valid json too (parsable by python's `json.loads` function):

`curl -d '{"name":"Car", "fields": {"owner": "text", "price": "number",        "purchased_in": "date", "first_owner": "[\"yes\",\"no\"]"}}' -H "Content-Type: application/json" -X POST <backend url>/api/risktypes/`

You can find your backend url on the env.json file that is generated after deploying. Note that the api is only available on the '/api' route. Individual risktypes can be accessed on the `/api/risktypes/:risktypeId` endpoint.

# Updating the application

For any change to the backend after deploying, simply run `zappa update dev` and zappa will take care of everything.

For any change to the frontend run the `update_frontend.py` script, which will build the Vue.js app and sync it with your S3 bucket using aws cli tools (it will pick the bucket name from the env.json file that is generated after the first deploy)
