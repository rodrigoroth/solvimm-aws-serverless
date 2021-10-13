# Solvimm Serverless Challenge

This project consists on a serverless operation, that everytime an image is uploaded on s3 bucket
it has its metadata extracted and stored on dynamodb (so it can be used later), and generates a
endpoint via aws api gateway to check data from the object stored.

## Installation

The serverless.yml plugin sometimes doesn't work, so you have to install it manually:

```bash
serverless plugin install -n serverless-python-requirements
```

Since it uses Pillow to read the image extracted, the only way that I finded to deploy it as a layer
was following this [tutorial](https://forums.aws.amazon.com/thread.jspa?threadID=309588).



## Usage

For deploy and lambda function usage, run the following command:

```bash
serverless deploy
```

To use the info_images function to get data from the database, run:

```bash
python handler.py 
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Author

[Rodrigo Roth Vasconcellos](https://www.linkedin.com/in/rodrigo-roth-vasconcellos-815377106/)

