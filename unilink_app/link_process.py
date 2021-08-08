# This is the heart of the UNILink where
#  all the links processing takes place.
# These functions extract all the SEO meta Tags that contains teh site's title, description
# and other infos .

import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import string

def normalize(x):
  t = re.sub(r'\n\s*\n', r'\n\n', x.strip(), flags=re.M)
  return t.replace('\n', " ")


def get_content(url):
    session = requests.Session()
    session.headers["User-Agent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    html = session.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    return soup
      
def get_random_str(n):
  chars = string.ascii_lowercase + string.digits
  return ''.join(random.choice(chars) for i in range(n))

def extract_info(url):
    soup = get_content(url)
    title = "__title__"
    image_url = ""
    desc = ""
    favicon_url = ""
    host_name = ""

    if url[-1] == '/':
      url = url[:-1]

    try:
      uri = urlparse(url)
      title = soup.title.get_text()
      image_url = soup.find("meta", attrs={"property": "og:image"}).attrs["content"]
      favicon_url = soup.find("link", attrs={"rel": "icon"}).attrs["href"]

      host_name = uri.netloc
      if not uri.scheme in image_url:
        image_url = url + "/" + image_url

      if not uri.scheme in favicon_url:
        if favicon_url[0] == "/":
          favicon_url = uri.scheme + "://" + uri.netloc + favicon_url 
        else:
          favicon_url = url + "/" + favicon_url     
    
      desc = soup.find("meta", attrs={"property": "og:description"}).attrs["content"]
    except:
      pass
    return title, image_url, desc, favicon_url, host_name