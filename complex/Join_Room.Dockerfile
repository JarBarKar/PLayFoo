FROM python:3-slim
WORKDIR /usr/src/app
COPY ../requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ../simple/amqp_setup.py ./invokes.py ./Join_Room.py ./
CMD [ "python", "./Join_Room.py" ]