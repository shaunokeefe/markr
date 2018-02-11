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
TODO(shauno)
