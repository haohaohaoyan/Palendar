from pyscript import document, window, when
from pyodide.ffi.wrappers import add_event_listener
import datetime, calendar, json, random
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
day_modal_title = document.querySelector(".day-modal > .title")
event_create_name = document.querySelector("#event-create-name")
event_create_description = document.querySelector("#event-create-description")
date_storage = document.querySelector("#day-storage")
#Event view modal
event_view_modal = document.querySelector(".event-view-modal")
event_view_title = document.querySelector(".event-view-modal > .title")
event_view_description = document.querySelector("#event-view-description")
event_date_storage = document.querySelector("#event-date-storage")

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
    event_view_modal.style.display = "none"
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
                    document.querySelector("#" + event["date"]).insertAdjacentHTML("beforeend", "<div class='event' title='" + event["description"] + "'><p>" + event["name"] + "</p></div>")
                except AttributeError:
                    pass
    except FileNotFoundError:
        raise(FileNotFoundError)
        #placeholder
    #add all event listeners
    for day in document.querySelectorAll(".calendar-day"):
        add_event_listener(day, "click", day_open_modal)
    for event in document.querySelectorAll(".event"):
        add_event_listener(event, "click", event_open_modal)

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

def event_open_modal(event):
    #can't believe this actually works, thanks stackoverflow nerds
    event.stopPropagation()
    event_view_modal.style.display = "flex"
    event_view_modal.style.top = str(event.clientY) + "px"
    event_view_modal.style.left = str(event.clientX) + "px"
    event_view_title.innerText = event.currentTarget.innerText
    event_view_description.innerText = event.currentTarget.title
    #For later
    event_date_storage.innerText = event.currentTarget.parentNode.id

@when("click", ".close")
def close_modal(event):
    event.currentTarget.parentNode.style.display = "none"

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
                description = event_create_description.value,
            )
            json.dump(out, event_file)
            event_file.write("\n")
            event_file.close()
            setup(current_month, current_year)
            #Clear
            event_create_name.value = ""
            event_create_description.value = ""
        except FileNotFoundError:
            pass
            #Not needed yet until localstorage implement

@when("click", "#event-delete-button")
def delete_event():
    if window.confirm("Are you sure you want to delete this event? \n This may also delete exact duplicate events."):
        try:
            events_file = open("events.txt", "r")
            lines = events_file.readlines()
            lineout = []
            for line in lines:
                event = json.loads(line)
                if not (event["name"] == event_view_title.innerText and event["date"] == event_date_storage.innerText and event["description"] == event_view_description.innerText):
                    lineout.append(line)
            #wipes file *gasp*
            events_file = open("events.txt", "w")
            events_file.writelines(lineout)
            events_file.close()
            setup(current_month, current_year)
        except FileNotFoundError:
            window.alert("Did you delete the events file in your cache?")
            #Impossible to actually get a FileNotFoundError here but just in case

add_event_listener(button_month_left, "click", setup_wrapper)
add_event_listener(button_month_right, "click", setup_wrapper)
add_event_listener(calendar_selector, "change", setup_wrapper)

setup(current_month, current_year)