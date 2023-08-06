import getflaggg.py
import hashlib

name = "fuckchq"

def hacksatellite():
    return "Congratulations!\nhack satellite successfully!"

def hackwebsite():
    return "Congratulations!\nHack website successfully!\namdin = \"chq\"\npassword = \"fuckchq\""

def hackpentagon():
    return "Congratulations!\nhack the Pentagon successfully!"

def getflag(a):
    if "\\" or "/" not in a:
        flag = hashlib.md5(a.encode("utf-8")).hexdigest()
    else:
        flag = get_file(a)
    return "flag{"+flag+"}"