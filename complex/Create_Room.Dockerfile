FROM python:3-slim
WORKDIR /usr/src/app
COPY ../requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ../simple/amqp_setup.py ./invokes.py ./Create_Room.py ./
CMD [ "python", "./Create_Room.py" ]