# api documentation at https://api.rawg.io/docs/ and https://rawg.io/apidocs
import requests 
  
# example api-endpoint 
URL = "https://api.rawg.io/api/games?"
  
# my api key
key = '572701901525413e985956e1112b7191'
  
# defining a params dict for the parameters to be sent to the API 
PARAMS = {
    'key':key,
    'page':'1',
    'page_size':'1',
    'genres':'5',
    'platforms':'4'
    } 
  
# sending GET request and saving the response as response object 
r = requests.get(url = URL, params = PARAMS)

# getting data in json format
data = r.json()

# results = data['results']

print(data)