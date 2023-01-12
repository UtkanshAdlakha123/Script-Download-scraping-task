import requests
from bs4 import BeautifulSoup
import json
import os
import pandas as pd

def download_file(url, directory):
  # create the directory if it does not exist in your parent directory
  if not os.path.exists(directory):
    os.makedirs(directory)

  # download the file of the current link you have passed just
  response = requests.get(url)

  # store the file name in it
  file_name = os.path.basename(url)

  # save the file to the directory
  with open(os.path.join(directory, file_name), 'wb') as f:
    f.write(response.content)

data_req= requests.get("https://www.manageengine.com/products/desktop-central/script-templates/latest-script.html")
soup= BeautifulSoup(data_req.content, 'html.parser')

# print(soup.prettify)

# now we have to select all those links which have class of text-dot
infor=soup.find_all("a" , class_="text-dot")

links=[]

# now we store them in a list
for i in infor:
    links.append("https://www.manageengine.com/products/desktop-central/script-templates/"+i.get("href"))

# now we have to extract the information for each script & store it in a text file
for link in links:
    
    url = link
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    table = soup.find("table")
    rows = table.find_all("tr")
    data = {}
    
    for row in rows:
        cols = row.find_all("td")
        cols = [col.text for col in cols]
        data[cols[0]] = cols[1:]

    json_string = json.dumps(data, indent=4)
    # print(data)
    with open("example.txt", "a") as fd:
        fd.write(json_string+"\n\n")


down_list=[]

# now we have to traverse through all links on main website 
for link in links:

    url2=link
    html=requests.get(url2)
    soup = BeautifulSoup(html.content, 'html.parser')

    # Find the 'a' tag with the desired title
    data_link = soup.find("a", title="Download the code.")

    # Extract the href attribute
    href = data_link['href']
    down_list.append(href)

# print(down_list)

directory_name = "script_dir"

try:
    os.mkdir(directory_name)
    print(f"{directory_name} created.")
except OSError:
    print(f"Creation of the directory {directory_name} failed.")

directory_path=os.path.abspath(directory_name)
# print(directory_path)

# you have to traverse through all the links of download
for url in down_list:
  download_file(url, directory_path)
