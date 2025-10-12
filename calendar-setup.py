from pyscript import document, window, when
from pyodide.ffi.wrappers import add_event_listener
import datetime, calendar, json
#no way there's literally an entire module dedicated to this *surprise*

#Constants in caps
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
#Document objects
#Calendar
calendar_selector = document.querySelector("#calendar-selector")
calendar_body = document.querySelector(".calendar-body")
button_month_left = document.querySelector("#button-month-left")
button_month_right = document.querySelector("#button-month-right")
#Event create modal
day_modal = document.querySelector(".day-modal")
day_modal_title = document.querySelector(".day-modal > #title")
event_create_name = document.querySelector("#event-create-name")
date_storage = document.querySelector("#day-storage")

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
    day_modal.style.display = "none"
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
                    document.querySelector("#" + event["date"]).insertAdjacentHTML("beforeend", "<div class='event'><p>" + event["name"] + "</p></div>")
                except AttributeError:
                    pass
    except FileNotFoundError:
        raise(FileNotFoundError)
        #placeholder
    #add all event listeners
    for day in document.querySelectorAll(".calendar-day"):
        add_event_listener(day, "click", day_open_modal)

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
    date_list = event.currentTarget.id.split("-")
    #For later
    date_storage.innerText = event.currentTarget.id
    day_modal_title.innerText = MONTHS[int(date_list[1])-1] + " " + date_list[0].lstrip("d0") + ", " + date_list[2]

@when("click", ".day-modal > #close")
def close_modal():
    day_modal.style.display = "none"

@when("click", "#event-create-save")
def save_event():
    if event_create_name.value == "":
        window.alert("No name for event!")
    else:
        try:
            event_file = open("events.txt", "a+")
            out = dict(
                name = event_create_name.value, 
                date = date_storage.innerText,
                priority = 0
            )
            event_file.write("\n")
            json.dump(out, event_file)
            #I have no clue how this below line makes it work, even while doing nothing. DON'T TOUCH IT.
            event_file.readlines()
            setup(current_month, current_year)
            #Clear
            event_create_name.value = ""
        except FileNotFoundError:
            pass
            #Not needed yet until localstorage implement

setup(current_month, current_year)

add_event_listener(button_month_left, "click", setup_wrapper)
add_event_listener(button_month_right, "click", setup_wrapper)
add_event_listener(calendar_selector, "change", setup_wrapper)