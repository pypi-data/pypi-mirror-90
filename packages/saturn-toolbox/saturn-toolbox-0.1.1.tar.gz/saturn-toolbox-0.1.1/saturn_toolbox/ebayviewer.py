import random
import requests
import time
from fake_headers import Headers

def start():
    print("Saturn eBay View Bot")
    print("--------------------")
    print("Saturn eBay view bot has 2 modes")
    print("Mode 1- Doesnt use proxies, if you send to many requests your ip will get banned ")
    print("Mode 2- Uses proxies, free proxies from https://www.proxyscrape.com work fine! ")


    def view(use_proxies: bool, proxies=None): 
        listing_url = input("What is your listing link? ")
        view_number = int(input("How many views would you like to send? "))


    
        for i in range(view_number):
            if use_proxies:
                headers = Headers(os="win", headers=True).generate()
                r = requests.get(listing_url, proxies=proxies, headers=headers)
                if r.status_code == 200:
                    print('View sent')
                elif r.status_code == 400:
                    print('Error')
                elif r.status_code == 401:
                    print('Ip banned')
                elif r.status_code == 403:
                    print('Ip banned')
                elif r.status_code == 404:
                    print('The link you sent was invalid! ')
                else:
                    print('error')
            else:
                headers = Headers(os="mac", headers=True).generate()
                r = requests.get(listing_url, headers=headers)
                if r.status_code == 200:
                    print('View sent')
                elif r.status_code == 400:
                    print('Error')
                elif r.status_code == 401:
                    print('Ip banned')
                elif r.status_code == 403:
                    print('Ip banned')
                elif r.status_code == 404:
                    print('The link you sent was invalid! ')
                else:
                    print('error')

        print("Successfully sent", view_number, "views")



    while True:
        x_mode = input("Which mode would you like to use? (1/2) ")

        if x_mode == '1':
            print('Starting')
            view(use_proxies=False)
            break
        elif x_mode == '2':  
            proxy_file = input("What is the PATH of your proxy file? ")
            print('Starting')
            proxy = set()

            with open(proxy_file, "r") as f:
                proxy = f.read().splitlines() 

            proxies = {
                'http': 'http://' + random.choice(list(proxy))
            }

            
            view(use_proxies=True, proxies=proxies)
            break
        else:
            print("Please only enter either 1 or 2!\n")