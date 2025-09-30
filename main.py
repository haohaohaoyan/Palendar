import datetime
import document

date = datetime.datetime.now()

def refreshdate(event):
    datetext = document.querySelector("dateoutput")
    date = datetime.datetime.now()
    datetext.innerText = date
    

