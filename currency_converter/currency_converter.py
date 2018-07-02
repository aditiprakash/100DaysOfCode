from flask import Flask, render_template, request
import urllib.request
from bs4 import BeautifulSoup
import bs4

APP = Flask(__name__)

@APP.route('/', methods = ['POST','GET'])
def index():
    f_form = t_form = []
    address = "https://www.xe.com/currencyconverter/"
    soup = BeautifulSoup(urllib.request.urlopen(address).read(), "html.parser")
    fromcurr = "Enter From Currency"
    tocurr = "Enter To Currency"

    from_form = soup.find("select",attrs={"id":"from"}).contents
    for _ in from_form:
        if type(_) is not bs4.element.NavigableString:
            f_form.append(_.string)

    to_form = soup.find("select", attrs={"id":"to"}).contents
    for _ in to_form:
        if type(_) is not bs4.element.NavigableString:
            t_form.append(_.string)

    if request.method == 'GET':
        amount = ""
        amount_final = ""
    else :

        amount = "".join(request.form.getlist('Amount'))
        fromcurr = "".join(request.form.getlist('From'))
        tocurr = "".join(request.form.getlist('To'))
        new_address = "https://www.xe.com/currencyconverter/convert/?Amount="+amount+"&From="+fromcurr+"&To="+tocurr
        new_soup = BeautifulSoup(urllib.request.urlopen(new_address).read(), "html.parser")
        amount_final = str(new_soup.find("span",{"class":"uccResultAmount"}).contents[0])
        
    
    return render_template("index.html", answer=amount_final, amount=amount, from_form=f_form, to_form=t_form , from_select=fromcurr, to_select=tocurr)

if __name__ == '__main__':
    APP.debug=True
    APP.run()