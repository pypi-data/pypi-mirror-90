import requests
from urllib.request import urlopen
def request(url):
  return requests.get(url)
def content(url):
  return urlopen(url).read()
def response(url):
  return requests.get(url)