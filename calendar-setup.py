from pyscript import document
from pyscript.web import *
import datetime, calendar
#no way there's literally an entire module dedicated to this *surprise*

#Constants in caps
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
#Document objects
calendar_month = document.querySelector("#calendar-month")
calendar_body = document.querySelector(".calendar-body")

def setup(day,month,year):
    calendar_month.innerText = str(MONTHS[month-1] + " " + str(year))    
    index = 0
    for i in range(1,(calendar.monthrange(year,month)[0]+2)%7):
        calendar_body.innerHTML += "<div class='calendar-day-past'>" + str(i) + "</div>"
        index += 1
    for i in range(1,calendar.monthrange(year,month)[1]+1):
        calendar_body.innerHTML += "<div class='calendar-day' id=" + str(i).zfill(2) + "-" + str(month).zfill(2) + "-" + str(year) + ">" + str(i) + "</div>"
        index += 1
    while index % 7 != 0:
        calendar_body.innerHTML += "<div class='calendar-day-past'>" + str(i) + "</div>"
        index += 1

                                         

setup(datetime.date.today().day, datetime.date.today().month, datetime.date.today().year)