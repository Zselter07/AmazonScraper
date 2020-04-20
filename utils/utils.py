def string_between(original, string_from, string_to):    
    try:
        return original.split(string_from)[1].split(string_to)[0]
    except Exception as e:
        print(e)
        
        return None

def remove_html_tags(text):
    from bs4 import BeautifulSoup

    return BeautifulSoup(text, "lxml").text

def secondsToText(secs):
    days = secs//86400
    hours = (secs - days*86400)//3600
    minutes = (secs - days*86400 - hours*3600)//60
    seconds = secs - days*86400 - hours*3600 - minutes*60

    hours_str = str(hours).zfill(2)
    minutes_str = str(minutes).zfill(2)
    seconds_str = str(seconds).zfill(2)
    result = '{}:{}:{}'.format(hours_str,minutes_str,seconds_str)
    return result

# def string_by_removing_html_texts():





# try: 
#     os.makedirs(path, exist_ok = True) 
#     print("Directory '%s' created successfully" %directory) 
# except OSError as error: 
#     print("Directory '%s' can not be created") 