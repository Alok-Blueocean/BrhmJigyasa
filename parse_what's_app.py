# !pip install bs4
#!pip install phonenumbers
import phonenumbers
from bs4 import BeautifulSoup
import re


def get_phone_numbers(in_file,out_file):
    soup = BeautifulSoup(open(in_file), "html.parser")
    spans = soup.findAll("span", {"dir" : "auto"})

    def is_phone_number(text):
        try:
            z = phonenumbers.parse(text, None)
        except:
            return False
        return phonenumbers.is_valid_number(z)

    fl = open(out_file,'w')
    phone_numbers=[]
    for span in spans:
        phone_num = span.text
        if(is_phone_number(span.text)):
            phone_num = re.sub(' ','',phone_num)
            phone_num = re.sub('\+91','',str(phone_num))
            phone_numbers.append(phone_num)
            fl.write(phone_num)
            fl.write('\n')
    fl.close()

in_file = '/home/nitayananda/Downloads/promo/WhatsApp.html'
out_file = '/home/nitayananda/Downloads/promo/group_phonenumbers.csv'
get_phone_numbers(in_file,out_file)