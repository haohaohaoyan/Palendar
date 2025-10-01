from pyscript import document
import datetime

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

calendar_month = document.querySelector("#calendar-month")

def setup():
    calendar_month.innerText = MONTHS[int(datetime.date.today().month)-1]
    #Oh no
    

setup()