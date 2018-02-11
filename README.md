# Markr

## Quickstart
Ensure you're using Python 3.6. If using virtualenv + virtualenvwrapper then
```
mkvirtualenv -p $(which python3.6) markr

```

Set up your environment using:
```
pip install -r requirements.txt
```

Set up serverless:
```
npm install -g serverless
npm install
brew install docker
export AWS_PROFILE="<your aws profile>" && export AWS_REGION=ap-southeast-2
```

Deploy
```
cd serverless
serverless deploy
```

## Testing
Run the following from the top level directory
```
python -m  pytest
```

## Development
Test your lambdas locally using the following:
```
cd serverless
serverless invoke local -f import -p import_event.json
serverless invoke local -f results -p results_event.json
```

This will directly execute the Python code for your lambdas on your system. Note that you'll need to be in an active virtualenv with requirements.txt installed for this to work

Similar commands can be used to test deployed lambdas
```
cd serverless
serverless invoke -f import -p import_event.json
serverless invoke -f results -p results_event.json
```

You will need to have already deployed your stack for this to work.

`serverless deploy` will redeploy your entire stack (infrastructure included). To just update a lambda function use:

```
cd serverless
serverless deploy function -f import
serverless deploy function -f results
```
