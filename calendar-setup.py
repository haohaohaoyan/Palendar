from pyscript import document
from pyscript.web import *
import datetime, calendar
#no way there's literally an entire module dedicated to this *surprise*

#Constants in caps
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
#Document objects
calendar_month = document.querySelector("#calendar-month")
calendar_body = document.querySelector(".calendar-body")

#Very initial setup
calendar.setfirstweekday(calendar.SUNDAY)

def setup(day,month,year):
    calendar_month.innerText = str(MONTHS[month-1] + " " + str(year))    
    for i in range(1,calendar.monthrange(year,month)[0]+1):
        calendar_body.innerHTML += "<div class='calendar-day-past'>" + str(i) + "</div>"
                                         

setup(datetime.date.today().day, datetime.date.today().month, datetime.date.today().year)