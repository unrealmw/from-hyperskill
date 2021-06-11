import requests
import json

"""Objective of this programm is transfering your amount of money in one currency to another. 
It recieves exchanging rates from www.floatrates.com  (json string), than converts it in python dictinary.
Some of this data stores in "cache" for fast access to it. If we need another exchange rate we address to our dictionary, get and save it in the cache."""

cache = {}                                                          #cache with exchanging rates

def get_request(cur_code):
    """Make a request to the URL to get exchange rates data for incoming currency code."""
    url = 'http://www.floatrates.com/daily/' + cur_code + '.json'
    request = requests.get(url)
    return request.text


def add_to_cache(cur_code, data_base):
    """Add currency code and exchange rate to cache from the received data base."""
    for k,v in data_base.items():
        if k == cur_code:
            cache.update({k: v["rate"]})


def cur_code_check(cur_code, cache_db):
    """Checks existing currency in cache."""
    print("Checking the cache...")
    if cur_code in cache_db.keys():
        print("Oh! It is in the cache!")
        return True
    else:
        print("Sorry, but it is not in the cache!")
        return False


def print_answer(money, receive_cur_code, cache_db):
    """Receives data from cache - exchange rate, and then calculates received amount of money."""
    for key, value in cache_db.items():
        if key == receive_cur_code:
            out_money = money * value
            return print(f"You received {out_money} {receive_cur_code.upper()}.")


if __name__ == '__main__':
    inp_cur_code = str(input()).lower()                             #currency code for incoming amount of money
    db = json.loads(get_request(inp_cur_code))                      #converting json string to Python dictionary
    add_to_cache("usd", db)                                         #add USD exchange rates for our currency code
    add_to_cache("eur", db)                                         #add USD exchange rates for our currency code
    while True:
        out_cur_code = str(input()).lower()                         #currency code for exchange
        if out_cur_code == "":                                      #breaking infinite loop
            break
        amount_of_money = int(input())                              #amount of money that we want to exchange
        if cur_code_check(out_cur_code, cache):                     #checking that currency code to exchange in cache 
            print_answer(amount_of_money, out_cur_code, cache)      #printing answer with exchanged amount of money
        else:
            add_to_cache(out_cur_code, db)                          #adding exchange rates for currency code if it not in cache
            print_answer(amount_of_money, out_cur_code, cache)      #printing answer with exchanged amount of money






