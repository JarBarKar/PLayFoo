# How to run the frontend

# Change Chrome header to allow CORS
## Step 1 - Create a Chrome app shortcut in your Desktop.
## Step 2 - Right Click and click on "Properties".
## Step 3 - Copy the path below and Change the "Target" (Remember to set the correct path to Chrome.exe): 
## "[PATH_TO_CHROME]\chrome.exe" --disable-web-security --disable-gpu --user-data-dir=~/chromeTemp
## Step 4 - Apply changes.

# Building Docker Images and Running Kubernetes Deployments
## Step 1 - In Docker Desktop, go to Settings -> Kubernetes -> check "Enable Kubernetes" to start Kubernetes
## Step 2 - In the folder with the docker-compose.yml file, run the command "docker-compose build" to build the required images
## Step 3 - Once the images have been built, run the "kubectl apply -f kubemanifest.yaml" command to run the kubernetes deployments

# Setting Up Databases
## Step 1 - In your web browser, go to "http://localhost:8082" to access the phpMyAdmin interface for the MySQL database. Log in using username: "root" and password: "admin".
## Step 2 - Click on "User Accounts" and click on the "admin" account.
## Step 3 - Under Edit Privileges, check the box for "Data" and click "Go" to allow Data permissions.
## Step 4 - Under Edit Privileges, click on "Change password", then click on "No password", then click on "Go" to ensure that the "admin" account is accessible with a password
## Step 5 - Click on "Import" and click "Choose File", then select the file at "PlayFoo/database/playfoo.sql" and click "Go"

# Setting Up API Gateway
## Step 1 - In your web browser, go to "http://localhost:1337" to access the Konga interface.
## Step 2 - create a konga account and sign in with that account
## Step 3 - In the welcome page, set up a connection to Kong Admin using "default" for Name and "http://kong:8001" for Kong Admin URL
## Step 4 - In Konga, go to "Services". For each of the Kong Services listed below:
## Step 4a - click on "Add New Service". Fill in the "Name" and "Url" for each service by copying and pasting the respective name and url provided in the list below, then click on "Submit Service" at the end of the page
## Step 4b - Click on the newly added service, then the "Routes" tab and click "Add Route". Copy and paste the respective path for the service in "Paths" and method in "Methods", making sure to press enter after adding each one. Click on "Submit Route" at the end of the page.
# Make sure Step 4, 4a and 4b are done for each of the 12 services below to fully set up the Kong API Gateway.
# Apologies in advance for the amount of setup required!

# Kong Service 1
name = Create_Room
url = http://10.98.31.90:5100/create_room
path = /create_room
method = POST

# Kong Service 2
name = Join_Room
url = http://10.98.31.91:5101/join
path = /join_room
method = POST

# Kong Service 3
name = Leave_Room
url = http://10.98.31.92:5102/leave
path = /leave_room
method = DELETE

# Kong Service 4
name = message_listener
url = http://10.98.32.93:5003/message_listener
path = /ping_message
method = POST

# Kong Service 5
name = Send_Message
url = http://10.98.31.93:5103/send_message
path = /send_message
method = POST

# Kong Service 6
name = Get_Game_ID_Room_Details
url = http://10.98.32.91:5001/game_id_room_detail
path = /game_id_room_detail
method = POST

# Kong Service 7
name = Get_Room_ID_Room_Details
url = http://10.98.32.91:5001/room_id_room_detail
path = /room_id_room_detail
method = POST

# Kong Service 8
name = Get_Banner
url = http://10.98.32.92:5002/banner
path = /banner
method = GET

# Kong Service 9
name = Get_Top_Rated
url = http://10.98.32.92:5002/toprated
path  = /toprated
method = GET

# Kong Service 10
name = Get_Games
url = http://10.98.32.92:5002/games
path = /games
method = GET

# Kong Service 11
name = Get_Game_Details
url = http://10.98.32.92:5002/gamedetails
path = /gamedetails
method = GET

# Kong Service 12
name = Login
url = http://10.98.32.90:5000/user
path = /user
method = POST
###### end of Kong Services ######
# Thank you for your patience in setting up our database and Kong API Gateway!

# How to run React App
## Step 1 - Build the dependency
```bash
npm build
```

## Step 2 - Start the frontend
```bash
npm start
```

## Step 3 - Run on testing
```bash
npm test
```

## Step 4 - Build for Production
```bash
npm run build
```