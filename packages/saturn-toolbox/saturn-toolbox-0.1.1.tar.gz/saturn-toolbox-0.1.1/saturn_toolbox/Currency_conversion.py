import requests
from bs4 import BeautifulSoup

def currency_convert():
    print('Currency names:')
    print('USD: US Dollar')
    print('EUR: Euro')
    print('CAD: Canadian dollar')
    print('PHP: Philippine peso')
    print('JPY: Japanese Yen')
    print('AUD: Australian Dollar')
    print('GPB British Pound')
    convert_from = input('What currency would you like to convert from? ')
    convert_to = input('What currency would you like to convert too? ')
    convert_amount = input('How much of that currency would you like to convert? ')
    url = f"https://www.x-rates.com/calculator/?from={convert_from}&to={convert_to}&amount={convert_amount}"
    r = requests.get(url).text
    soup1 = BeautifulSoup(r, 'lxml')
    final_ammount = soup1.find('span', class_='ccOutputRslt').text
    print(convert_amount, convert_from, 'is', final_ammount)


