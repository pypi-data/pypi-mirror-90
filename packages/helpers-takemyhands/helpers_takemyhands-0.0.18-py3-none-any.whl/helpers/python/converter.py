# conver string to byte array
def string_to_bytearray(string):
    if string is None:
        return None                    
    b = bytearray()
    b.extend(map(ord, string))
    return b
    