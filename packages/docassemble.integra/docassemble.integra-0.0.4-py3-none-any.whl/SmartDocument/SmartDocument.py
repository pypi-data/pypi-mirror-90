import requests
import json

def generate(file, payload):
  headers = { "Content-Type": "application/x-www-form-urlencoded" }
  file.set_attributes(private=False)
  data = { "file": file.url_for(external=True), "meta_form": json.dumps(payload) }
  response = requests.post("https://integraapi.azurewebsites.net/docassemble", data=data, headers=headers)
  return response.json()['url']