FROM python:3-slim
WORKDIR /usr/src/app
COPY ../http.reqs.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY ./message.py ./
CMD [ "python", "./message.py" ]