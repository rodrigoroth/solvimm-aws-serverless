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
was following this [tutorial](https://forums.aws.amazon.com/thread.jspa?threadID=309588):

- Start with Amazon Linux on EC2 instance with 
ssh -i <your-pem-file>.pem <your-instance-user>@<your-instance-public-dns>
- aws configure (and enter in your credentials)
- follow this commands:
```bash
sudo yum update -y
```
```bash
sudo su
```
```bash
cd /usr/lib64/python2.7/dist-packages/
```
```bash
rm -rf PIL
```
```bash
cd /home/ec2-user
```
```bash
sudo yum install gcc bzip2-devel ncurses-devel gdbm-devel xz-devel sqlite-devel openssl-devel tk-devel uuid-devel readline-devel zlib-devel libffi-devel
```
```bash
wget https://www.python.org/ftp/python/3.7.0/Python-3.7.0.tar.xz
```
```bash
tar -xJf Python-3.7.0.tar.xz
```
```bash
cd Python-3.7.0
```
```bash
./configure --enable-optimizations
```
```bash
make altinstall
```
```bash
export PATH=$PATH:/usr/local/bin
```
```bash
pip3.7 install pillow
```
```bash
mkdir -p /home/ec2-user/lambda_layers/python/lib/python3.7/site-packages
```
```bash
cd /usr/local/lib/python3.7/site-packages
```
```bash
cp -r * /home/ec2-user/lambda_layers/python/lib/python3.7/site-packages/
```
```bash
cd /home/ec2-user/lambda_layers
```
```bash
zip -r pill.zip *
```
```bash
aws s3 cp pill.zip s3://<your-bucket>/pill.zip
```
- In the Lambda console, I then created a Lambda Layer using the pill.zip from the s3 bucket and installed it
- I then added the layer to the Python 3.7 Lambda function and it worked
- PS: if any command fails, check your path with ls, since it can be different from my


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

