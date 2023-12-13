

def snake_to_camel_case(word):
    parts = word.split('_')
    return parts[0] + ''.join(x.title() for x in parts[1:])