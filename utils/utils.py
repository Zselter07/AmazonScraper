def string_between(original, string_from, string_to):    
    try:
        return original.split(string_from)[1].split(string_to)[0]
    except Exception as e:
        print(e)
        
        return None

def remove_html_tags(text):
    from bs4 import BeautifulSoup

    return BeautifulSoup(text, "lxml").text
# def string_by_removing_html_texts():





# try: 
#     os.makedirs(path, exist_ok = True) 
#     print("Directory '%s' created successfully" %directory) 
# except OSError as error: 
#     print("Directory '%s' can not be created") 