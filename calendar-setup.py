from pyscript import document
import datetime

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

calendar_date = document.querySelector("#calendar-date")

def setup():
    calendar_date.innerText = MONTHS[int(datetime.date.today().month)-1]

setup()