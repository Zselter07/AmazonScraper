import time, requests

def request(url, headers=None, max_request_try_count=10, sleep_time = 2.5, debug=False):
    current_try_count = 0

    while current_try_count < max_request_try_count:
        current_try_count += 1
        resp = __request(url, headers=headers, debug=debug)

        if resp is not None:
            return resp
        
        time.sleep(sleep_time)
    
    return None

def __request(url, headers=None, debug=False):
    if headers is None:
        headers = {}
    
    headers = __headers_by_optionally_setting(headers, {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:74.0) Gecko/20100101 Firefox/74.0',
        'Accept':'*/*',
        'Cache-Control':'no-cache',
        'Accept-Encoding':'gzip, deflate, br',
        'Connection':'keep-alive'
    })

    try:
        resp = requests.get(url, headers=headers)

        if resp is None:
            if debug:
                print('ERROR: Resp is None')
            
            return None

        if resp.status_code != 200:
            if debug:
                print('ERROR:', resp)
            
            return None
        
        return resp
    except Exception as e:
        if debug:
            print('ERROR:', e)

        return None

def __headers_by_optionally_setting(headers, keys_values):
    for key, value in keys_values.items():
        if key not in headers:
            headers[key] = value
    
    return headers