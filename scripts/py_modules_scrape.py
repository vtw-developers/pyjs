import requests
from bs4 import BeautifulSoup

# URL of the Python module index page
url = "https://docs.python.org/3/py-modindex.html"

# Send a request to fetch the page content
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the anchor tags
module_tags = soup.find_all('a')

# Extract the text inside the <code> tag
for module_tag in module_tags:
  if module_tag.find('code', class_='xref') is not None:
    print(f"'{module_tag.text}', ", end='')
