# RoBERTSaiKwan (Backend)

Backend for RoBERTSaiKwan News Summarizer (Extractive).

## Prerequisites

We tested the application to work well on python 3.7.10. Upper versions are likely to work properly but lower version may not. This is because fastAPI make use of async/await in Python 3.7+

All of the packages required are listed in `requirements.txt` please do
```sh
python3 -m pip install -r requirements.txt
```
or
```sh
make install
```
to install all packages.

## Deployment

Running command are listed in `Makefile`. Please refer to it for running information ex.`make run`

We opened CORS on `localhost:3000` (react development server). Please refer to `app/main.py` to change CORS configuration if you want to deploy this application.

The model(s) are in `app/model/{model_name}.py`. These are taken from [this repo]. Currently, there is only 1 model and an interface was not written to be model-independent.


[this repo]: https://www.google.com
