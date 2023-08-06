import random
import sys
import readchar
import argparse
import pyperclip
import webbrowser
from urllib.parse import urlparse
from colorama import Fore, Back, Style
__version__ = "1.1.1"

def encrypt(text: str, key: str = None):
    """
    Encrypts the text.

    :param text:Text to encrypt.
    :type text:str
    :param key:Key to use for encrypting.
    :type key:str
    :returns:Encrypted text.
    :rtype:str
    """
    text = text
    res = ""
    tmp = ""
    lkey = []
    if key is not None:
        lkey = list(key.encode("utf-8"))
    for i, c in enumerate(text.encode("utf-8")):
        if lkey:
            ri = lkey[i % len(lkey)]
        else:
            ri = random.randint(-9, 9)
        ec = c + ri
        tmp = ""
        if not lkey:
            tmp += ("0" if ri > 0 else "1") + str(abs(ri))
        tmp += str(abs(ec))
        res += str(len(tmp))+tmp
    return res


def decrypt(text: str, key: str = None):
    """
    Decrypts the encrypted text.

    :param text:Text to decrypt.
    :type text:str
    :param key:Key to use for encrypting.
    :type key:str
    :returns:Decrypted text.
    :rtype:str
    """
    if not text.isdecimal():
        raise ValueError("Encrypted text must contain only numbers.")
    tmpres = []
    lkey = []
    if key is not None:
        lkey = list(key.encode("utf-8"))
    i = 0
    counter = 0
    while i < len(text):
        l = int(text[i])
        tmp = text[i+1:i+l+1]
        i += l+1
        if not tmp:
            break
        if lkey:
            c = int(tmp) - lkey[counter % len(lkey)]
        else:
            pm = 1 if tmp[0] == "0" else -1
            ri = int(tmp[1])*pm
            c = int(tmp[2:]) - ri
        tmpres.append(c)
        counter += 1
    return bytes(tmpres).decode("utf8")


def main():
    parser = argparse.ArgumentParser(
        description='this script will encrypt/decrypt text.')
    parser.add_argument('text', help='Text to encrypt/decrypt.', nargs='?')
    group = parser.add_mutually_exclusive_group(required=len(sys.argv) > 1)
    group.add_argument('-e', '--encrypt', help="do encrypting.",
                       action='store_true')
    group.add_argument('-d', '--decrypt',
                       help="do decrypting.", action='store_true')
    parser.add_argument(
        '-k', '--key', help="key for encrypting/decrypting.", required=False)
    args = parser.parse_args()
    if args.text is None:
        sep = "======================================================="
        print(sep)
        print(("SCrypter Ver"+__version__).center(len(sep)))
        print(sep)
        print("Please input (e)ncrypt or (d)ecrypt: ", end="", flush=True)
        while True:
            c = readchar.readkey()
            if c.lower() in "ed":
                break
        print(c.lower())
        if c.lower() == "e":
            text = input("Please input text to encrypt: ")
            print("Do you want to use key?(y/n): ", end="", flush=True)
            while True:
                c = readchar.readkey()
                if c.lower() in "yn":
                    break
            print(c.lower())
            if c.lower() == "y":
                key = input("Please input key: ")
                res = encrypt(text, key)
            else:
                res = encrypt(text)
            print("The text has successfully encrypted.")
            print(res)
            print("Copy it to clipboard?(y/n): ", end="", flush=True)
            while True:
                c = readchar.readkey()
                if c.lower() in "yn":
                    break
            print(c.lower())
            if c.lower() == "y":
                pyperclip.copy(res)
                print("Encrypted text has successfully copied.")
            
        else:
            text = input("Please input encrypted text to decrypt: ")
            print("Did your encrypted text use key?(y/n): ", end="", flush=True)
            while True:
                c = readchar.readkey()
                if c.lower() in "yn":
                    break
            print(c.lower())
            if c.lower() == "y":
                key = input("Please input key: ")
                
                res = decrypt(text, key)
            else:
                
                res = decrypt(text)
            print("The text has successfully decrypted.")
            print(res)
            o = urlparse(res)
            if len(o.scheme) > 0:
                print("URL detected. Open it?(y/n): ", end="", flush=True)
                while True:
                    c = readchar.readkey()
                    if c.lower() in "yn":
                        break
                print(c.lower())
                if c.lower() == "y":
                    webbrowser.open(res)
                    print("The URL has successfully opened.")
                
    else:
        if args.encrypt:
            print(encrypt(args.text, args.key))
        elif args.decrypt:
            print(decrypt(args.text, args.key))


if __name__ == "__main__":
    main()
