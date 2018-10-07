# dev
Website developed for the application process at BriteCore, done with Vue.js and Django Rest Framework

Demo at:
- http://britecoretest5-s3bucket-3c3aep3xs79y.s3-website-sa-east-1.amazonaws.com/ (front)
- https://1yaby9bccg.execute-api.sa-east-1.amazonaws.com/dev/api/ (api)

The general idea is that the customer defines their RiskTypes, by choosing an unique name (a string) and setting up the fields (a [JSONField](https://docs.djangoproject.com/en/2.1/ref/contrib/postgres/fields/#django.contrib.postgres.fields.JSONField)).

The fields are defined by name and type, the possible types being `number`, `date`, `text` and an "enum" type that should be presented as a serializable json list of strings (these strings being the possibles choices). Here's an example of a RiskType with all the fields:
```
{
  "name": "Car",
  "fields": {
    "owner": "text",
    "price": "number",
    "first_owner": "[\"yes\",\"no\"]",
    "purchased_in": "date"
  }
}
```

Any special behavior the fields could have would be serialized inside the value as list of attributes (for example, besides a " type" attribute, fields could have a "unique": "true", or "blank": "true" and so forth). Validation would be done then on the RiskType serializer and any omitted attributes would have a default value. Since the project specification didnt require any of this, I didnt provide a specification and assumed that no extra information would be required, there would be no defaults, etc, but it would be easy to change the structure of `fields` to adapt to whatever would be the case (no schema changes would be needed after all, we just would need to migrate the data to a new format).

The RiskTypes table is responsible only for holding the types defined by the users, and since this is what the project specification asked, there is no need for any other table or model. If this ever went to production or the project required that the user should be able to submit the form, I would define a Risks table to hold the actual instances of the types. The model would then have a foreignkey for a risktype, and a field to hold the data (which would be also a JSONField, that would hold a list of json objects with the field name for keys and naturally their values).


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
- Run `aws cloudformation describe-stacks --stack-name <stack name>` and create a `env.json` file containing **ALL THE KEYS AND VALUES** under the `"Outputs"` section. This step is very important! (for example, for an OutputKey called FRONTENDURL, add `"FRONTENDURL":"your actual frontendurl value"` to the `env.json` file)
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

After deploying, the database will be empty, so there will be nothing to render on the frontend. You can interact with the backend by using tools like curl, httpie, or by enabling the Django REST Framework browsable API (no auth needed).  

With curl, try the following for setting up a sample RiskType that contains all the possible field types. Note that the content-type must be valid json, and that enum fields are defined with valid json too (parsable by python's `json.loads` function):

`curl -d '{"name":"Car", "fields": {"owner": "text", "price": "number",        "purchased_in": "date", "first_owner": "[\"yes\",\"no\"]"}}' -H "Content-Type: application/json" -X POST <backend url>/api/risktypes/`

You can find your backend url on the env.json file that is generated after deploying. Note that the api is only available on the '/api' route. Individual risktypes can be accessed on the `/api/risktypes/:risktypeId` endpoint.

# Updating the application

For any change to the backend after deploying, simply run `zappa update dev` and zappa will take care of everything.

For any change to the frontend run the `update_frontend.py` script, which will build the Vue.js app and sync it with your S3 bucket using aws cli tools (it will pick the bucket name from the env.json file that is generated after the first deploy). Alternatively, you can just build and deploy it manually by going to the `front/` directory and running `npm run build` and then `aws s3 sync ./dist s3://<your bucket name>`
