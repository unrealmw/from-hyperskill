import requests
import json

cache = {}

def get_request(cur_code):
    url = 'http://www.floatrates.com/daily/' + cur_code + '.json'
    request = requests.get(url)
    return request.text


def add_to_cache(cur_code, data_base):
    for k,v in data_base.items():
        if k == cur_code:
            cache.update({k: v["rate"]})


def cur_code_check(cur_code, cache_db):
    print("Checking the cache...")
    if cur_code in cache_db.keys():
        print("Oh! It is in the cache!")
        return True
    else:
        print("Sorry, but it is not in the cache!")
        return False


def print_answer(money, receive_cur_code, cache_db):
    for key, value in cache_db.items():
        if key == receive_cur_code:
            out_money = money * value
            return print(f"You received {out_money} {receive_cur_code.upper()}.")


if __name__ == '__main__':
    inp_cur_code = str(input()).lower()
    db = json.loads(get_request(inp_cur_code))
    add_to_cache("usd", db)
    add_to_cache("eur", db)
    while True:
        out_cur_code = str(input()).lower()
        amount_of_money = int(input())
        if out_cur_code == "" or amount_of_money == "":
            break
        if cur_code_check(out_cur_code, cache):
            print_answer(amount_of_money, out_cur_code, cache)
        else:
            add_to_cache(out_cur_code, db)
            print_answer(amount_of_money, out_cur_code, cache)



