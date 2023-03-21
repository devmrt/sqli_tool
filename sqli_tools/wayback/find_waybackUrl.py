import os
import requests
from bs4 import BeautifulSoup
#color
from colorama import init, Fore, Back, Style
#from urllib.parse import urlparse

#def is_part_of_domain(url,doamin):
#    return urlparse("http://"+domain).netloc == urlparse(url).netloc

#starting_url = "http://example.com"
#domain_name = input("enter domain name \n like: domain.com ")
#domain_name="testphp.vulnweb.com"
# Send HTTP GET request to the starting URL
#response = requests.get("http://"+domain_name)

# Parse the HTML code using BeautifulSoup
#soup = BeautifulSoup(response.text, "html.parser")

# Find all links in the HTML code
#links = soup.find_all("a")

# Loop through all links and extract the URLs
#for link in links:
#    url = link.get("href")
#    print(url)

def get_all_urls_from_page(url,list_of_urls):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    domain_name=url.split("//")[1].split("/")[0]
#    list_of_urls = []
# Find all links in the HTML code
    for link in soup.find_all('a'):
# Loop through all links and extract the URLs
        url = link.get('href')
# take only the uniq URLs
        if url not in list_of_urls and ("/" in url or "." in url):
# check if the url is part of our domain
            if "//" in url and url.split("//")[1]==domain_name or "//" not in url:
#        if is_part_of_domain(url,domain_name):
                list_of_urls.append(url)
                print(url)
    return list_of_urls   
        

    
def get_endpoints_from_urlList(list_of_urls,endpoints,dir_2_fuzz):
#change color            
    print(Fore.RED + "found endpoints")
    for endpoint in list_of_urls:
        if "." in endpoint and endpoint.split(".")[-1] and endpoint not in endpoints:
            endpoints.append(endpoint)
            print(endpoint) 
#else appaned it to directoryies to fuzz  
        else:
            if endpoint not in dir_2_fuzz:
                dir_2_fuzz.append(endpoint) 
    return endpoints,dir_2_fuzz
            
#main_url="http://localhost/vulnerable-sites/basic_college_management/"            
main_url="http://testphp.vulnweb.com/"
list_of_urls =get_all_urls_from_page(main_url,[])
endpoints,dir_2_fuzz=get_endpoints_from_urlList(list_of_urls,[],[])    
print(Fore.YELLOW +"get other liks from endpoints")   
for endpoint in endpoints:
    print(Fore.GREEN+"get urls from "+endpoint)
    list_of_urls=get_all_urls_from_page(main_url+endpoint,list_of_urls)
    endpoints,dir_2_fuzz=get_endpoints_from_urlList(list_of_urls,endpoints,dir_2_fuzz)  
print(Fore.YELLOW +"list of uniq liks")
print(list_of_urls) 

#make dir to out data in it
dir_name=main_url.split("//")[1].split("/")[0]
try:
    os.makedirs(dir_name)
except FileExistsError:
    # directory already exists
    pass
    
    
all_urls=open(dir_name+"/list_of_urls","w")
for url in list_of_urls:
    all_urls.write(url+"\n")
all_urls.close()


list_of_endpoints=open(dir_name+"/list_of_endpoints","w")
for url in endpoints:
    list_of_endpoints.write(url+"\n")
list_of_endpoints.close()


dir_2_fuzz=open(dir_name+"/dir_2_fuzz","w")
for url in dir_2_fuzz:
    dir_2_fuzz.write(url+"\n")
dir_2_fuzz.close()

