# Bootleg-Beatsaver (formerly 'Beatsaver-search')

## Intro

A static website ([bootleg-beatsaver.com](http://bootleg-beatsaver.com)) for doing semi-sophisticated searching of the content contained within parent site [beatsaver.com](https://beatsaver.com/)

Born out of a lack of existing search capability and desire to experiment with serverless web hosting, this is the result.

Powered by [Amazon Web Services](https://aws.amazon.com/) (AWS): API  Gateway, Lambda, Relational Database Service (RDS) & Simple Storage Service (S3)

If you're interested in creating a similar kind of serverless website, I can highly recommend the AWS tutorial upon which a lot of this is based: [https://aws.amazon.com/getting-started/projects/build-serverless-web-app-lambda-apigateway-s3-dynamodb-cognito/](https://aws.amazon.com/getting-started/projects/build-serverless-web-app-lambda-apigateway-s3-dynamodb-cognito/)


## Contributing

If you'd like to contribute to the site by adding features or changing / fixing html or javascript etc. feel free to raise a pull request - if it's anywhere half-decent I'll be open to merging/deploying it.


## Development Requirements

* An IDE to debug in ([IntelliJ Community Edition](https://www.jetbrains.com/idea/download/) is my IDE of choice)


### For testing html/javascript changes

* Recommend Firefox for testing purposes, as it is more flexible with allowing cross-site ajax calls (chrome doesn't allow this), allowing you to run the index/songs html's locally when testing html/javascript changes.
* NOT Internet Explorer - due to unsupported javascript functions (specifically 'ForEach') this flat out doesn't work in IE


### For testing database / backend changes

* Python 3.0+
* Python plugin (if you're using IntelliJ Community Edition)
* A postgres SQL database with a corresponding settings.json file, with username, password, database (name), db_endpoint (database endpoint) and db_port (database port) parameters defined (as per what you see at the start of run-search.py)


## Quick Start

### HTML / Javascript Development

It should be as simple as loading up the index.html (firefox recommended!), and then modifying it and any associated files e.g.

* songs.html
* authors.html
* about.html
* blackstars.png
* starssmall.png


### Backend Database Development

1. Install the python libraries as per the requirements.txt (pip install -r requirements.txt)
2. Run an initial scrape of the data:
```
update.py bbs
```
This will populate the 'songs' table (see `create_table.sql` file) in the db by pulling the data off beatsaver.com and into your database, or update it if it has changed.

3. Then run
```
update.py bar
```
which will populate the 'authorstats' table of the db by compiling what has already been collected in the songs table

Once this is done you should able to ad-hoc run most/all of the python functions found inside `run-search.py` to do things like retrieve song/author data etc locally.

Due to the fact that the implementation of the API / lambda function is stored in AWS, it's not possible to make testing/debugging completely end-to-end (or at least, not that I have so far figured out).

If you want to go down the rabbit-hole of setting this up end-to-end, [this is a good starting point](https://aws.amazon.com/getting-started/projects/build-serverless-web-app-lambda-apigateway-s3-dynamodb-cognito/](https://aws.amazon.com/getting-started/projects/build-serverless-web-app-lambda-apigateway-s3-dynamodb-cognito/), however I'm not willing (or really qualified) to do a step-by-step of the process.


## Feedback / Questions

If you've got any questions, want to give feedback or have suggestions on what can be improved, leave me a message on discord: Zeekin#1824

