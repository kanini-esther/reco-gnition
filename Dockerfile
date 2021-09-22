FROM python:3.8
ADD . /
WORKDIR /
RUN python3 -m pip install -r requirements.txt
CMD [ "python", "app.py" ]
