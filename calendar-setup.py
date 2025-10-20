from pyscript import document, window, when
from pyodide.ffi.wrappers import add_event_listener
import datetime, calendar, json, random, ast
#no way there's literally an entire module dedicated to this *surprise*

#api key: AIzaSyCNUX7mhETUC1lQgoK14J_OQSB10oXvnsI

#Constants in caps
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
#Document objects
#Calendar
calendar_selector = document.querySelector("#calendar-selector")
calendar_main = document.querySelector(".calendar-main")
calendar_body = document.querySelector(".calendar-body")
button_month_left = document.querySelector("#button-month-left")
button_month_right = document.querySelector("#button-month-right")
#Event create modal
day_modal = document.querySelector(".day-modal")
day_modal_title = document.querySelector(".day-modal > .title")
event_create_name = document.querySelector("#event-create-name")
event_create_description = document.querySelector("#event-create-description")
date_storage = document.querySelector("#day-storage")
date_id_storage = document.querySelector("#date-id-storage")
#Event view modal
event_view_modal = document.querySelector(".event-view-modal")
event_view_title = document.querySelector(".event-view-modal > .title")
event_view_description = document.querySelector("#event-view-description")
event_key_storage = document.querySelector("#event-key-storage")
#offcanvases
offcanvas_tray = document.querySelector(".offcanvas-tray")
offcanvas_tray_toggle = document.querySelector(".offcanvas-tray-toggle")

#variable
current_month = datetime.date.today().month
current_year = datetime.date.today().year

#Set first weekday from Mon to Sun
calendar.setfirstweekday(calendar.SUNDAY)

def htmlReformat(string):
    return str(string.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;").replace("'", "&#39;"))

def setup(month,year):
    global current_month, current_year
    calendar_body.innerHTML = ""
    calendar_selector.value = str(year) + "-" + str(month).zfill(2)
    current_month, current_year = month, year
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
    #Logic: First key is a list of existing event keys. All afterwards are events in dict form, upon creation checks if random id is already in use, if so regenerate
    #gee i sure do hate having to deal with all these edge cases
    try:
        key_list = ast.literal_eval(window.localStorage.getItem("event_keys"))
    except ValueError:
        window.localStorage.setItem("event_keys", "[]")
        setup(current_month, current_year)
        return
    if len(key_list) == 0:
        window.localStorage.setItem("event_keys", "[]")
    else:
        for event_raw in key_list:
            eventS = json.loads(window.localStorage.getItem(str(event_raw)))
            try:
                document.querySelector("#" + eventS["date"]).innerHTML += "<div class='event' id='" + str(event_raw) + "' title='" + str(eventS["description"]) + "'>" + eventS["name"] + "</div>"
            except AttributeError:
                #This really only comes up if the event is on a different month
                pass
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
    date_id_storage.innerText = ""
    #Empty to differentiate between creating and editing
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
    event_key_storage.innerText = event.currentTarget.id

def event_create(name: str, date: str, description: str, color: list, priority: int, change_id: str = ""):
    out = dict(
            name = htmlReformat(event_create_name.value), 
            date = date_storage.innerText,
            description = htmlReformat(event_create_description.value),
        )
    key_list = ast.literal_eval(window.localStorage.getItem("event_keys"))
    if change_id != "":
        window.localStorage.setItem(change_id, json.dumps(out))
    else:
        id=random.randint(100000,999999)
        while id in key_list:
            id=random.randint(100000,999999)
        key_list.append(str(id))
        window.localStorage.setItem("event_keys", str(key_list))
        window.localStorage.setItem(str(id), json.dumps(out))
    setup(current_month, current_year)

@when("click", ".close")
def close_modal(event):
    event.currentTarget.parentNode.style.display = "none"

@when("click", "#event-create-save")
def save_event():
    if event_create_name.value == "":
        window.alert("No name for event!")
    else:
        event_create(event_create_name.value, date_storage.innerText, event_create_description.value, [], 0, date_id_storage.innerText)
        #Clear for all
        event_create_name.value = ""
        event_create_description.value = ""
        return

@when("click", "#event-delete-button")
def delete_event(event):
    event.stopPropagation()
    if window.confirm("Are you sure you want to delete this event?"):
        window.localStorage.removeItem(event_key_storage.innerText)
        key_list = ast.literal_eval(window.localStorage.getItem("event_keys"))
        key_list.remove(event_key_storage.innerText)
        window.localStorage.setItem("event_keys", str(key_list))
        setup(current_month, current_year)

@when("click", "#event-edit-button")
def edit_event(event):
    event.stopPropagation()
    day_modal.style.display = "flex"
    day_modal.style.top = str(event_view_modal.style.top)
    day_modal.style.left = str(event_view_modal.style.left)
    event_view_modal.style.display = "none"
    event_data = json.loads(window.localStorage.getItem(event_key_storage.innerText))
    #Autofills
    event_create_name.value = event_data["name"]
    event_create_description.value = event_data["description"]
    date_storage.innerText = event_data["date"]
    date_list = event_data["date"].split("-")
    day_modal_title.innerText = MONTHS[int(date_list[1])-1] + " " + date_list[0].lstrip("d0") + ", " + date_list[2]
    date_id_storage.innerText = event_key_storage.innerText

#Yeah great shove ALL offcanvas things here

@when("click", ".offcanvas-tray-toggle")
def toggle_offcanvas():
    if offcanvas_tray.style.left == "0px":
        offcanvas_tray.style.left = "-20vw"
        offcanvas_tray_toggle.innerText = ">"
        calendar_main.style.width = "70vw"
    elif offcanvas_tray.style.left == "-20vw":
        offcanvas_tray.style.left = "0px"
        offcanvas_tray_toggle.innerText = "<"
        calendar_main.style.width = "50vw"
    #I don't know how changing width works but margin doesn't. At least they have the same outcome. I'm suspecting it's due to a combination of auto margin and width squeezing

@when("click", ".offcanvas-tray-tab-button")
def switch_offcanvas_tab(event):
    #Hide/switch all off first, then use event to find which to show
    for tab in document.querySelectorAll(".offcanvas-tab-content"):
        tab.style.display = "none"
    for tab_button in document.querySelectorAll(".offcanvas-tray-tab-button"):
        tab_button.style.backgroundColor = "lightgray"
    document.querySelector("#" + event.currentTarget.id.replace("-button", "")).style.display = "block"
    document.querySelector("#" + event.currentTarget.id).style.backgroundColor = "white"

@when("change", "#note-text")
def save_notes(event):
    window.localStorage.setItem("user_notes", event.currentTarget.value)

@when("click", "#clear-localstorage")
def clear_localstorage():
    if window.confirm("Are you sure you want to clear all events? This action cannot be undone."):
        window.localStorage.clear()
        setup(current_month, current_year)


#On runtime functions
document.querySelector("#offc-chatbot-button").style.backgroundColor = "white"
document.querySelector("#offc-chatbot").style.display = "block"
if window.localStorage.getItem("user_notes") is not None:
    document.querySelector("#note-text").value = window.localStorage.getItem("user_notes")

add_event_listener(button_month_left, "click", setup_wrapper)
add_event_listener(button_month_right, "click", setup_wrapper)
add_event_listener(calendar_selector, "change", setup_wrapper)

setup(current_month, current_year)