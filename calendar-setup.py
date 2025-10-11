from pyscript import document, window
from pyodide.ffi.wrappers import add_event_listener
import datetime, calendar, json
#no way there's literally an entire module dedicated to this *surprise*

#Constants in caps
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
#Document objects
calendar_selector = document.querySelector("#calendar-selector")
calendar_body = document.querySelector(".calendar-body")
button_month_left = document.querySelector("#button-month-left")
button_month_right = document.querySelector("#button-month-right")
day_modal = document.querySelector(".day-edit-modal")

#variable
current_month = datetime.date.today().month
current_year = datetime.date.today().year

#Set first weekday from Mon to Sun
calendar.setfirstweekday(calendar.SUNDAY)

def setup(month,year):
    global current_month, current_year
    calendar_body.innerHTML = ""
    calendar_selector.value = str(year) + "-" + str(month).zfill(2)
    current_month = month
    current_year = year
    #Am i just bad at logic *kill me now*
    index = 0
    after_index = 1
    for i in range(1,(calendar.weekday(year,month,1)+2)):
        #+2 because 1 for the range exclusion and 1 for pushing the index from 0
        calendar_body.innerHTML += "<div class='calendar-day calendar-day--past'>" + str(i) + "</div>"
        index += 1
    for i in range(1,calendar.monthrange(year,month)[1]+1):
        calendar_body.innerHTML += "<div class='calendar-day' id=d" + str(i).zfill(2) + "-" + str(month).zfill(2) + "-" + str(year) + ">" + str(i) + "</div>"
        index += 1
    while index % 7 != 0:
        calendar_body.innerHTML += "<div class='calendar-day calendar-day--past'>" + str(after_index) + "</div>"
        index += 1
        after_index += 1
    #find current date and highlight hhhggkghkgkhghkghkg
    document.querySelector("#d" + str(datetime.date.today().day).zfill(2) + "-" + str(datetime.date.today().month).zfill(2) + "-" + str(datetime.date.today().year).zfill(2)).className = "calendar-day calendar-day--today"
    #put events loader here ig
    #placeholder events.txt loaded into virtual filesystem
    try:
        with open("events.txt", "r") as events_file:
            for event_raw in events_file:
                event = json.loads(event_raw)
                try:
                    document.querySelector("#d" + event["date"]).insertAdjacentHTML("beforeend", "<div class='event'><p>" + event["name"] + "</p></div>")
                except AttributeError:
                    pass
    except FileNotFoundError:
        raise(FileNotFoundError)
        #placeholder

def setup_wrapper(event):
    if event.currentTarget.id == button_month_left.id:
        #i am so stupid
        if current_month == 1:
            setup(12, current_year - 1)
        else:
            setup(current_month - 1, current_year)
    if event.currentTarget.id == button_month_right.id:
        #once again restating my idiocy
        if current_month == 12:
            setup(1, current_year + 1)
        else:
            setup(current_month + 1, current_year)
    if event.currentTarget.id == calendar_selector.id:
        setup(int(event.currentTarget.value.split("-")[1]), int(event.currentTarget.value.split("-")[0]))

def day_open_modal(event):
    day_modal.style.display = "flex"
    day_modal.style.top = str(event.clientY) + "px"
    day_modal.style.left = str(event.clientX) + "px"
    day_modal.innerText = event.target.id

setup(current_month, current_year)

add_event_listener(button_month_left, "click", setup_wrapper)
add_event_listener(button_month_right, "click", setup_wrapper)
add_event_listener(calendar_selector, "change", setup_wrapper)
for day in document.querySelectorAll(".calendar-day"):
    add_event_listener(day, "click", day_open_modal)