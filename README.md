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

# List of assumptions
- Users would be accessing from Australia. There are no accommodations around speed etc. for users accessing from overseas.
- No authentication required. This was mostly for expedience. It is likely that in a real product that ingests data that users would autheticate before they are able to add data to the system. This could be implemented using AWS API Gateway's API keys without too much trouble.
- All results for a given test arrive in a single xml document. Basically once we accept a document we assume that no more documents will arrive. This made the ingestion to S3  lot simpler, and it seemed to be consistent with the spec. Assume that we will neither see a resend of an accepted test, nor will we see a single test split over multiple documents.
- A single document contains only one test. Similar to above, this makes things a lot simpler. TODO(shauno): add this as a validation
- Files are relatively small. This assumption was necessary as we will run into issues with Lambda max memory (512MB in the current configuration) as the files are loaded straight into memory and also not streamed. We will also run into execution time limits with Lambda if we are doing long running jobs (>5 mins) which should be considered. Memory limits could be avoided by streaming files (although it wasn't immedately obvious how to accept a file stream from API Gateway. Job length issues could be fixed by splitting up jobs into batches although this would complicate things, and it'd be probably be easier to give up on Lambda at that point.
- Figures in the results endpoint can be rounded to two decimal places. This seemed reasonable.

# Notes on implementation, and possible improvements
## Choice of tools
Went with Serverless on AWS Lambda for a few resons
- Markr were having trouble with their bills so it seemed like a great way to save them a few dollars using AWS Lambda rather than using long-lived ec2 instances
- Great way to have both infrastructure and code up and running without doing much work
- Framework is very popular, and has both good development velocity and active support channels.
- Well suited to small, simple APIs leveraging a lot of AWS infrastructure (infrastructure management built in)
- Chose Serverless over Chalice/Zappa. The latter two choices are far stronger for defining API endpoints and views with nice, succinct Flask-like sytax, and would likely be stronger for larger projects with more complicated APIs (coupled with something like Terraform to manage supporting resources such as IAM roles, VPC, S3 etc.). The downside to choosing Serverless here is that, out of the box, it doesn't have a nice built-in way of handling web requests and routing and requires a bit more boilerplate. 

Used Python as it was my strongest language that was compatible with Lambda.

## Approach

Originally planned to have the `import` endpoint simply dump contents into S3 and then have other dependant lambdas trigger on s3 put events to actually do the processing so that we could respond to the post nice and quickly. This would also make pre-computation of the results data (i.e. calcuating results as the data arrives in the system

Given that we have to give the user a response as to whether their request was valid, though, it means we've got to have at least a little look inside the file before we hand off to S3. Figured, in addition to doing validation, it'd also be worth pulling out some metadata from the file (test number) to make our s3 storage a bit easier. At this point, was getting a bit time poor so decided to skip pre-computation and just calculate results live from the files in S3.

Performance wasn't too bad, and we can always come back around and re-use the code for querying (which was kept separate from the actual lambda function) in an intermediate precalculation lambda, which then stores results to either an object store as JSON (which is then exposed by the `results` endpoint), or if the analytics dashboard is going to be a bit more wizz-bang, into an RDS instance so that queries can be made across tests/ cut along dimensions.

## Things left un-done
- Offline processing of data
- Limit IAM Role for each lambda to just specific permissions it needs
- Document functions
- Limit number of files being rolled into the Lambdas
- Raise 404's on missing paths instead of API Gateway's mysterious error about missing API keys
- Validations - this is a big one. Ran out of time before we could do things like validate the markr header, document contents etc.
- Bucket name definition should be configured using an ENV variable and a central settings.py file. I feel very bad about this.
- Testing of `results_function`. Skipped this as I ran out of time. Unforgiveable.
- Authentication (although we don't have https so :/)
- Expressing scores as percentages of totals

## Things that didn't go great
- managing the xml inside the Markr document wasn't a great idea
- adding numpy was definitely overkill given the build time/size, but was the best way to get this done in a short time
- blessed method for installing python requirements in Serverless make things go a bit slow
