FROM python:3-slim
WORKDIR /usr/src/app
COPY ../http.reqs.txt ../activity_error.reqs.txt ./
RUN pip install --no-cache-dir -r http.reqs.txt -r activity_error.reqs.txt
COPY ./amqp_setup.py ./invokes.py ./error.py ./
CMD [ "python", "./error.py" ]