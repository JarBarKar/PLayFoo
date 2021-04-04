FROM python:3-slim
WORKDIR /usr/src/app
COPY http.reqs.txt sqlalchemy.reqs.txt amqp.reqs.txt ./
RUN pip install --no-cache-dir -r http.reqs.txt -r sqlalchemy.reqs.txt -r amqp.reqs.txt
COPY ./amqp_setup.py ./invokes.py ./error.py ./
CMD [ "python", "./error.py" ]