def string_between(original, string_from, string_to):    
    try:
        return original.split(string_from)[1].split(string_to)[0]
    except Exception as e:
        print(e)
        return None
        