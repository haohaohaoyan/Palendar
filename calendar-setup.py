from pyscript import document, window, when
from pyodide.ffi.wrappers import add_event_listener
import datetime, calendar, json, random, ast
#oh, a calendar module that literally does what i need it to, yay
from pyscript.js_modules import genai_bot
#finally

#api key: AIzaSyCNUX7mhETUC1lQgoK14J_OQSB10oXvnsI

#Constants in caps
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
#Document objects
#Calendar
calendar_selector = document.querySelector("#calendar-selector")
month_select_modal = document.querySelector("#month-select-modal")
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
notification_button = document.querySelector("#toggle-notifications")

#variable
current_month = datetime.date.today().month
current_year = datetime.date.today().year

def htmlReformat(string):
    return str(string.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;").replace("'", "&#39;")) # hatsune miku??????

def setup(month,year):
    global current_month, current_year
    calendar_body.innerHTML = ""
    calendar_selector.innerText = str(MONTHS[int(month)-1]) + " " + str(year)
    current_month, current_year = month, year
    #Am i just bad at logic *kill me now*
    day_modal.style.display = "none"
    event_view_modal.style.display = "none"
    index = 0
    for i in range(1,(calendar.weekday(year,month,1)+2)):
        #+2 because 1 for the range exclusion and 1 for pushing the index from 0
        calendar_body.innerHTML += "<div class='calendar-day-past'></div>"
        index += 1
    for i in range(1,calendar.monthrange(year,month)[1]+1):
        calendar_body.innerHTML += "<div class='calendar-day' id=d" + str(i).zfill(2) + "-" + str(month).zfill(2) + "-" + str(year) + ">" + str(i) + "</div>"
        index += 1
    while index % 7 != 0:
        calendar_body.innerHTML += "<div class='calendar-day-past'></div>"
        index += 1
    #find current date and highlight hhhggkghkgkhghkghkg
    document.querySelector("#d" + str(datetime.date.today().day).zfill(2) + "-" + str(datetime.date.today().month).zfill(2) + "-" + str(datetime.date.today().year).zfill(2)).className = "calendar-day today"
    #load events
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
        if ".calendar-day--past" not in day.classList:
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

@when("click", "#calendar-selector")
def open_month_select(event):
    month_select_modal.style.display = "flex"
    document.querySelector("#select-month").value = current_month
    document.querySelector("#select-year").value = current_year

@when("click", "#confirm-month-select")
def close_month_select():
    month_select_modal.style.display = "none"
    try:
        setup(int(document.querySelector("#select-month").value), int(document.querySelector("#select-year").value))
    except ValueError:
        pass
        #Doing nothing resets the field

def day_open_modal(event):
    try:
        day_modal.style.display = "flex"
        day_modal.style.top = str(event.clientY) + "px"
        day_modal.style.left = str(event.clientX) + "px"
        date_list = event.currentTarget.id.split("-")
        #For later
        date_storage.innerText = event.currentTarget.id
        date_id_storage.innerText = ""
        #Empty to differentiate between creating and editing
        day_modal_title.innerText = MONTHS[int(date_list[1])-1] + " " + date_list[0].lstrip("d0") + ", " + date_list[2]
    except IndexError:
        pass

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

def event_create(name: str, date: str, description: str = "", color: str = "", priority: int = 0, change_id: str = ""):
    out = dict(
            name = htmlReformat(name), 
            date = date,
            description = htmlReformat(description),
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

#no multi decorators, am i just stupid? event listener down below instead
def drag_modal(event):
    target = event.currentTarget
    target.style.top = str(event.clientY) + "px"
    target.style.left = str(event.clientX) + "px"

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
    day_modal.style.display = "none"
    event_view_modal.style.display = "none"
    if offcanvas_tray.style.left == "0px":
        offcanvas_tray.style.left = "-25vw"
        offcanvas_tray_toggle.innerText = ">"
        calendar_main.style.marginLeft = "calc(50% - 35vw)"
    elif offcanvas_tray.style.left == "-25vw":
        offcanvas_tray.style.left = "0px"
        offcanvas_tray_toggle.innerText = "<"
        calendar_main.style.marginLeft = "27vw"

@when("click", ".offcanvas-tray-tab-button")
def switch_offcanvas_tab(event):
    #Hide/switch all off first, then use event to find which to show
    for tab in document.querySelectorAll(".offcanvas-tab-content"):
        tab.style.display = "none"
    for tab_button in document.querySelectorAll(".offcanvas-tray-tab-button"):
        tab_button.style.backgroundColor = "cornflowerblue"
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

@when("click", "#send-message-button")
async def send_message():
    user_input = document.querySelector("#send-message").value
    if user_input.strip() == "":
        window.alert("Please enter a message.")
        return
    chat_div = document.querySelector("#chat")
    chat_div.innerHTML += "<p class='user-message'>" + htmlReformat(user_input) + "</p>"
    chat_div.scrollTop = chat_div.scrollHeight
    document.querySelector("#spinner-ai").style.display = "flex"
    document.querySelector("#send-message").value = ""
    #Create response
    await genai_bot.generate(str(user_input))
    response = genai_bot.get_response()
    if not response.text:
        chat_div.innerHTML += "<p class='ai-message'>Done!</p>"
    else: 
        chat_div.innerHTML += "<p class='ai-message'>" + response.text + "</p>"
    document.querySelector("#spinner-ai").style.display = "none"
    #Function running
    if response.functionCalls:
        for function in response.functionCalls:
            event_create(function.args.name, function.args.date, function.args.description)
    chat_div.scrollTop = chat_div.scrollHeight

#Running notifications
@when("click", "#toggle-notifications")
def toggle_notifications(event):
    genai_bot.notification.requestPermission()
    window.localStorage.setItem("notification_toggle", notification_button.checked)
    window.alert("Please reload for changes to take effect.")

@when("change", "#notif-set-time")
def set_time():
    current_date = datetime.datetime.now()
    window.localStorage.setItem("notification_time", document.querySelector("#notif-set-time").value)
    set_date = document.querySelector("#notif-set-time").value.split(":")
    window.localStorage.setItem("next_notif", datetime.datetime(current_date.year, current_date.month, current_date.day + 1, int(set_date[0]), int(set_date[1])))

#On runtime functions
#Set first weekday from Mon to Sun
calendar.setfirstweekday(calendar.SUNDAY)

#Set favicon (hehe)
document.querySelector("#favicon").href = "assets/palendar-favico/palendar-favico-" + str(datetime.date.today().day).zfill(2) + ".png"
#remove loader
document.querySelector(".spinner-border").style.display = "none"

#before everything else: welcome
if window.localStorage.length == 0:
    window.alert("Hi! Welcome to Palendar. For now, please provide an API key if you can download this. It should be fixed soon. ")

document.querySelector("#offc-chatbot-button").style.backgroundColor = "white"
document.querySelector("#offc-chatbot").style.display = "block"
if window.localStorage.getItem("user_notes") is not None:
    document.querySelector("#note-text").value = window.localStorage.getItem("user_notes")
if window.localStorage.getItem("notification_toggle") is not None:
    notification_button.checked = True if window.localStorage.getItem("notification_toggle") == "true" else False
    if window.localStorage.getItem("notification_toggle") == "on":
        genai_bot.notification_send()
if window.localStorage.getItem("notification_time") is not None:
    document.querySelector("#notif-set-time").value = window.localStorage.getItem("notification_time")

add_event_listener(button_month_left, "click", setup_wrapper)
add_event_listener(button_month_right, "click", setup_wrapper)
add_event_listener(calendar_selector, "change", setup_wrapper)
add_event_listener(event_view_modal, "dragend", drag_modal)
add_event_listener(day_modal, "dragend", drag_modal)

setup(current_month, current_year)