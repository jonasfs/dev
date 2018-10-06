# dev
Website developed for the application process at BriteCore, done with Vue.js and Django Rest Framework

# Setup

First you must install all the packages in requirements.txt by running `pip -r requirements.txt`. Then cd into the front/ folder and install all the npm packages in package.json by running `npm install` (this might take a while).

Then, make sure your aws credentials are properly configured, including the region key.

Only after that, run deploy.py with python3.6.

## Installing with the deploy.py script

The deploy script was tested under Debian Stretch, on a virtualenv, and on a terminal with bash, but it should be fine for other posix complying shells. I do not recommend trying it on Windows (even under msys), as I ran with too many issues even installing the libraries when I was checking for portability. 

## Installing manually
If needed, you can do it without the script by following these steps:

- Create the CloudFormation stack using the cloudformation.yaml: `aws cloudformation create-stack --stack-name <stack name> --template-body file://./cloudformation.yaml --parameters ParameterKey=DBUSERNAME,ParameterValue=<db user> ParameterKey=DBPASSWORD,ParameterValue=<db password> ParameterKey=DBNAME,ParameterValue=<db name>` 
- Wait until the stack is created
- Run `aws cloudformation describe-stacks --stack-name <stack name>` and create a `env.json` file containing ALL THE KEYS AND VALUES under the `"Outputs"` section. This step is very important! (for example, for an OutputKey called FRONTENDURL, add `"FRONTENDURL":"your actual frontendurl value"` to the `env.json` file)
- Add to the `env.json` file a key called `"STACKNAME"` with the name of the stack you supplied previously
- Add to the `env.json` file a key called `"SECRETKEY"` with a random key of your choice. This will be the value used for the SECRET_KEY on the Django project settings (adding it to `env.json` will suffice, the app will load it from there) 
- Create your `zappa_settings.json` by running `zappa init` (point the settings file to `dev.settings`) 
- Add the key and value pair `"exclude": "front"` to your newly created `zappa_settings.json` so you dont upload the frontend code to the s3 bucket used to create the lambda function (if you dont this, zappa will upload much more than it needs to)
- Deploy it with `zappa deploy dev` and add the returned url to your `env.json` file under the key `"BACKENDURL"` (if for some reason it doesnt return the url, run `zappa status dev` to get it again)
- Run zappa again, now with `zappa update dev` so it updates your settings file with the url returned on the previous step
- Run `zappa manage dev migrate` to initiate the database
- Edit the file `front/config/prod.env.js` to substitute the value under the `ROOT_API` key with the BACKENDURL you set up previously on the `env.json` file
- Build your frontend files by going to the `front/` directory and running `npm run build`
- Upload your frontend by running `aws s3 sync ./dist s3://<your bucket name>`. You can find the bucket name on the `env.json` file under the key `"BUCKETNAME"`.
- Phew, you're done!

# Populating the DB

After deploying, the database will be empty, so there will be nothing to render on the frontend. You can interact with the backend by using tools like curl, httpie, or by enabling the Django REST Framework browsable API.  

With curl, try the following for setting up a sample RiskType that contains all the possible field types. Note that the content-type must be valid json, and that enum fields are defined with valid json too (parsable by python's `json.loads` function):

`curl -d '{"name":"Car", "fields": {"owner": "text", "price": "number",        "purchased_in": "date", "first_owner": "[\"yes\",\"no\"]"}}' -H "Content-Type: application/json" -X POST <backend url>/api/risktypes/`

You can find your backend url on the env.json file that is generated after deploying. Note that the api is only available on the '/api' route. Individual risktypes can be accessed on the `/api/risktypes/:risktypeId` endpoint.

# Updating the application

For any change to the backend after deploying, simply run `zappa update dev` and zappa will take care of everything.

For any change to the frontend run the `update_frontend.py` script, which will build the Vue.js app and sync it with your S3 bucket using aws cli tools (it will pick the bucket name from the env.json file that is generated after the first deploy). Alternatively, you can just build and deploy it manually by going to the `front/` directory and running `npm run build` and then `aws s3 sync ./dist s3://<your bucket name>`
