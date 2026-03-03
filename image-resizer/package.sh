#!/bin/bash

cd lambda

pip install -r requirements.txt -t .
zip -r ../lambda.zip .

cd ..
