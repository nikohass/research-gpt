import requests
from parse import parse_response

def lookup(url: str) -> str:
    # Lookup a file on the web and return a ChatGPT readable text
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        print(url, e)
        error_msg = f"While looking up the url {url}, the following error occured: {e}"
        print(error_msg)
        return error_msg
    status_code = response.status_code
    print(url, status_code)
    if status_code != 200:
        error_msg = f"While looking up the url {url}, the following error occured: {status_code}"
        return error_msg

    return parse_response(response)
