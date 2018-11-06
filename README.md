# dev
Website developed for the application process at BriteCore, done with Vue.js and Django Rest Framework

Demo at:
- http://britejonas2-s3bucket-1ph3quhb7a0x4.s3-website-sa-east-1.amazonaws.com (front)
- https://asi7stu0vk.execute-api.sa-east-1.amazonaws.com/dev/api/ (api)
- https://asi7stu0vk.execute-api.sa-east-1.amazonaws.com/dev/api/risktypes/ (risktypes api endpoint)

The general idea is that the customer defines their RiskTypes, by choosing an unique name (a string) and creating the fields, which are represented on the RiskType model by a reverse relationship (the RiskType being a ForeignKey of each field).

The fields can be a TextField, NumberField, DateField or EnumField, all of which inherit common properties from a GenericField. The EnumField has a special `choices` field, which is an `ArrayField` of django's TextField (no to be confused with our own `TextField` models) that represent the possible choices. Currently the other fields have no special properties because the project specification doesnt require it. The Entity Relationship Diagram below illustrates the model:
![ER Diagram](https://github.com/jonasfs/dev/raw/master/ERD.png "ER Diagram")

Note that the reverse relationship on the RiskType model will actually have a queryset of GenericFields. The django extension `django-model-utils` helps us by providing a model manager that automatically selects the proper subclasses by merely appending methods like `._select_subclasses()` or `.get_subclass()` to our querysets. We use this to, among other things, determine which field serializer to use (check `serializers.py`)

Fields are created by POSTing a (not necessarily unique) name and a field_type, the possible field_types being `number`, `date`, `text` and an "enum" type that should be presented as a list of strings (these strings being the possibles choices). Here's a serializable representation of a RiskType with all the possible fields:

```
{
	'name': 'Car',
	'fields': [
		{
			'name': 'owner',
			'field_type': 'text'
		},
		{
			'name': 'first_owner',
			'field_type': ['yes', 'no']
		},
		{
			'name': 'price',
			'field_type': 'number'
		},
		{
			'name': 'purchased_in',
			'field_type': 'date'
		}
	]
}
```

The RiskTypes table is responsible only for holding the types defined by the users. If this ever went to production or the project required that the user should be able to submit the form, I would define a Risks table to hold the actual instances of the types. The Risk model would then have a foreignkey for a risktype, and a counterpart to the RiskType.fields field (Risk.values?), to hold the actual fields data.


# Setup

First you must install all the packages in requirements.txt by running `pip install -r requirements.txt`. Then cd into the front/ folder and install all the npm packages in package.json by running `npm install` (this might take a while).

Then, make sure your aws credentials are properly configured, including the region key. For the deploy.py script to work properly (see below), **you must not have any other profile other than the [default] one** defined on your .aws/credentials file. This is a compromise in order to work with how the zappa cli deals with different credentials files (this could be worked around, but to avoid adding more unnecessary complexity to the deploy file I decided to not do it).

Only after that, run deploy.py with python3.6.

## Installing with the deploy.py script

The deploy script was tested under Debian Stretch, on a virtualenv, and on a terminal with bash, but it should be fine for other posix complying shells. I do not recommend trying it on Windows (even under msys), as I ran with too many issues even installing the libraries when I was checking for portability. 

Remember: **you must not have any other profile other than the [default] one defined on your .aws/credentials file or the script will fail**.

## Installing manually
If needed, you can do it without the script by following these steps:

- Create the CloudFormation stack using the cloudformation.yaml: `aws cloudformation create-stack --stack-name <stack name> --template-body file://./cloudformation.yaml --parameters ParameterKey=DBUSERNAME,ParameterValue=<db user> ParameterKey=DBPASSWORD,ParameterValue=<db password> ParameterKey=DBNAME,ParameterValue=<db name>` 
- Wait until the stack is created
- Run `aws cloudformation describe-stacks --stack-name <stack name>` and create a `env.yaml` file containing **ALL THE KEYS AND VALUES** under the `"Outputs"` section. This step is very important! (for example, for an OutputKey called FRONTENDURL, add `"FRONTENDURL":"your actual frontendurl value"` to the `env.yaml` file)
- Add to the `env.yaml` file a key called `"STACKNAME"` with the name of the stack you supplied previously
- Add to the `env.yaml` file a key called `"SECRETKEY"` with a random key of your choice. This will be the value used for the SECRET_KEY on the Django project settings (adding it to `env.yaml` will suffice, the app will load it from there) 
- Create your `zappa_settings.json` by running `zappa init` (point the settings file to `dev.settings`) 
- Add the key and value pair `"exclude": "front"` to your newly created `zappa_settings.json` so you dont upload the frontend code to the s3 bucket used to create the lambda function (if you dont this, zappa will upload much more than it needs to)
- Deploy it with `zappa deploy dev` and add the returned url to your `env.yaml` file under the key `"BACKENDURL"` (if for some reason it doesnt return the url, run `zappa status dev` to get it again)
- Run zappa again, now with `zappa update dev` so it updates your settings file with the url returned on the previous step
- Run `zappa manage dev migrate` to initiate the database
- Edit the file `front/config/prod.env.js` to substitute the value under the `ROOT_API` key with the BACKENDURL you set up previously on the `env.yaml` file
- Build your frontend files by going to the `front/` directory and running `npm run build`
- Upload your frontend by running `aws s3 sync ./dist s3://<your bucket name>`. You can find the bucket name on the `env.yaml` file under the key `"BUCKETNAME"`.
- Phew, you're done!

There's an example env.yaml file with all the required keys for reference on the repository (dont forget, all keys are required!)

# Populating the DB

After deploying, the database will be empty, so there will be nothing to render on the frontend. You can interact with the backend by using tools like curl, httpie, or by enabling the Django REST Framework browsable API (no auth needed).  

With curl, try the following for setting up a sample RiskType that contains all the possible field types (note that the content-type is `application/json`):

`curl -d '{"name": "Car", "fields": [{"name": "owner", "field_type": "text" }, {"name": "first_owner", "field_type": ["yes", "no"]}, {"name": "price", "field_type": "number"}, {"name": "purchased_in", "field_type": "date" }]}' -H "Content-Type: application/json" -X POST <backend url>/api/risktypes/`

You can find your backend url on the env.yaml file that is generated after deploying. Note that the api is only available on the '/api' route. The list of risktypes can be accessed on the `/api/risktypes/` endpoint, while individual risktypes can be accessed on the `/api/risktypes/:risktypeId` endpoint, where `:risktypeId` is a positive integer.

# Updating the application

For any change to the backend after deploying, simply run `zappa update dev` and zappa will take care of everything.

For any change to the frontend run the `update_frontend.py` script, which will build the Vue.js app and sync it with your S3 bucket using aws cli tools (it will pick the bucket name from the env.yaml file that is generated after the first deploy). Alternatively, you can just build and deploy it manually by going to the `front/` directory and running `npm run build` and then `aws s3 sync ./dist s3://<your bucket name>`

# Testing

Make sure your env.yaml file is setup properly for development (for example, if everything is being hosted locally, use 127.0.0.1 as the hostname for all the url related keys), and your DBUSER has the CREATEDB permission on your database.

## API

Run `manage.py test`

The tests are defined under api/tests.py

## FRONTEND

cd into front/ and run `npm run test`
