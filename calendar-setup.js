const TODAY = new Date();
const MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
var currentMonth = TODAY.getMonth();
var currentYear = TODAY.getFullYear();

function htmlReformatStr(string) {
    return string.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#39;"); // hatsune miku??!?!;
}

function setup(month, year) {
    // Clean up, set date, hide modals
    currentYear = year;
    currentMonth = month;
    document.querySelector("#calendar-body").innerHTML = "";
    document.querySelector("#calendar-selector").innerText = `${MONTHS[month]} ${year}`;
    document.querySelector(".day-modal").style.display = 'none';
    document.querySelector(".event-view-modal").style.display = 'none';

    // Create calendar
    calendarBody = document.querySelector("#calendar-body");
    for (let i = 0; i < new Date(currentYear, currentMonth).getDay(); i++) {
        calendarBody.innerHTML += '<div class="calendar-day-past"></div>';
    };
    for (let i = 0; i < new Date(currentYear, currentMonth+1, 0).getDate(); i++) {
        calendarBody.innerHTML += `<div class="calendar-day" id="d${String(i + 1).padStart(2,"0")}-${String(currentMonth + 1).padStart(2,"0")}-${currentYear}">${i + 1}</div>`;
    };
    while (calendarBody.childElementCount % 7 != 0) {
        calendarBody.innerHTML += '<div class="calendar-day-past"></div>';
    };
    //highlight today
    try {
        document.querySelector(`#d${String(TODAY.getDate()).padStart(2, "0")}-${String(TODAY.getMonth()+1).padStart(2,"0")}-${TODAY.getFullYear()}`).className = "calendar-day today";
    } catch (TypeError) {}; // do nothing if it's another month

    // Event things
    if (localStorage.getItem('event_keys') === null) {
        // create empty event keys and restarts if it doesn't exist yet
        localStorage.setItem('event_keys', '[]')
        setup(currentMonth, currentYear)
        return
    } else {
        let keyList = JSON.parse(localStorage.getItem('event_keys'));
        for (const event of keyList) {
            // Use event ids in key list to get events
            let eventParsed = JSON.parse(localStorage.getItem(event));
            try {
                document.querySelector(`#${eventParsed.date}`).innerHTML += `<div class='event' id='${event}' title='${eventParsed.description}'>${eventParsed.name}</div>`;
            } catch (TypeError) {} // do nothing, this is because day of event is on date not shown
        };
    } 
    
    // prepare event listeners
    for (const day of document.querySelectorAll('.calendar-day')) {
        day.addEventListener('click', openDayModal);
    };
    for (const event of document.querySelectorAll('.event')) {
        event.addEventListener('click', openEventModal);
    };
}

function createEvent(name, date, description = '', color = '', priority = 0, changeId = '') {
    // aww, can't type annotate?????
    // construct dictionary from inputs
    let output = JSON.stringify({
        'name': htmlReformatStr(name),
        'date': date,
        'description': htmlReformatStr(description) 
    });
    // Priority and color are planned, not in yet bc "we got bigger fish to fry" 
    if (changeId != '') {
        localStorage.setItem(changeId, output);
        setup(currentMonth, currentYear)
        return
    } else {
        // fetch key list, create random 6 digit id, write 
        let keyList = JSON.parse(localStorage.getItem('event_keys'));
        let newId = String(Math.floor((Math.random()*10000)+1)).padStart(4, "0");
        // prevent dupes
        while (keyList.includes(newId)) {
            newId = String(Math.floor((Math.random()*10000)+1)).padStart(4, "0");
        };
        keyList.push(newId)
        localStorage.setItem('event_keys', JSON.stringify(keyList))
        localStorage.setItem(newId, output)
        setup(currentMonth, currentYear)
        return
    }
}

// Modal funcs
function openDayModal(event) {
    let dayModal = document.querySelector('.day-modal');
    dayModal.style.display = 'flex';
    dayModal.style.top = `${event.clientY}px`;
    dayModal.style.left = `${event.clientX}px`;
    // For later when saving events
    document.querySelector('#date-storage').innerText = event.currentTarget.id;
    // Differentiate between editing and changing, blanks the target
    document.querySelector('#date-id-storage').innerText = '';
    // parse date id to natural english
    let dateList = String(event.currentTarget.id).split('-');
    dayModal.querySelector('.title').innerText = `${MONTHS[dateList[1]-1]} ${Number(dateList[0].replace('d', ''))}, ${dateList[2]}`;
    dayModal.querySelector('.modal-header > p').innerText = `Creating event`;
}

document.querySelector('#event-create-save').addEventListener('click', function() {
    if (document.querySelector('#event-create-name').value == "") {
        window.alert("No name for event!");
        return
    } else {
        createEvent(document.querySelector('#event-create-name').value, document.querySelector('#date-storage').innerText, document.querySelector('#event-create-description').value, [], 0, document.querySelector('#date-id-storage').innerText);
        // blank args for the unimplemented ones
        document.querySelector('#event-create-name').value = "";
        document.querySelector('#event-create-description').value = "";
        document.querySelector('#date-id-storage').innerText = "";
        return
    }
});

function openEventModal(event) {
    // make sure it doesn't trigger day modal too
    event.stopPropagation();

    let eventModal = document.querySelector('.event-view-modal');
    eventModal.style.display = 'flex';
    eventModal.style.top = `${event.clientY}px`;
    eventModal.style.left = `${event.clientX}px`;

    // fill out
    eventModal.querySelector('.title').innerText = event.currentTarget.innerText;
    eventModal.querySelector('#event-view-description').innerText = event.currentTarget.title;

    // for changing
    eventModal.querySelector('#event-key-storage').innerText = event.currentTarget.id;
}

document.querySelector('#event-delete-button').addEventListener('click', function(event) {
    event.stopPropagation();
    if (confirm("Are you sure you want to delete this event?")) {
        let eventKeyStorage = document.querySelector('#event-key-storage');
        // remove
        localStorage.removeItem(eventKeyStorage.innerText);
        keyList = JSON.parse(window.localStorage.getItem("event_keys"));
        keyList.splice(keyList.indexOf(eventKeyStorage.innerText), 1);
        localStorage.setItem("event_keys", JSON.stringify(keyList));
        // reset
        setup(currentMonth, currentYear);
        eventKeyStorage.innerText = '';
    }
})

document.querySelector('#event-edit-button').addEventListener('click', function(event) {
    // edit event
    event.stopPropagation()

    let dayModal = document.querySelector('.day-modal');
    let eventViewModal = document.querySelector('.event-view-modal');
    dayModal.style.display = "flex";
    dayModal.style.top = eventViewModal.style.top;
    dayModal.style.left = eventViewModal.style.left;
    eventViewModal.style.display = "none";

    // fill out
    let eventData = JSON.parse(localStorage.getItem(eventViewModal.querySelector('#event-key-storage').innerText));
    dayModal.querySelector('#event-create-name').value = eventData.name
    dayModal.querySelector('.modal-header > p').innerText = `Editing event "${eventData.name}"`
    dayModal.querySelector('#event-create-description').value = eventData.description
    dayModal.querySelector('#date-storage').innerText = eventData.date
    // format for title
    let dateList = String(eventData.date).split('-');
    dayModal.querySelector('.title').innerText = `${MONTHS[dateList[1]-1]} ${Number(dateList[0].replace('d', ''))}, ${dateList[2]}`;
    // used to provide a target for changing
    dayModal.querySelector('#date-id-storage').innerText = eventViewModal.querySelector('#event-key-storage').innerText
});

// Offcanvas functions

document.querySelector('.offcanvas-tray-toggle').addEventListener('click', function() {
    // quick and dirty solution. TODO: make this better by eliminating the ifthen or something?????
    document.querySelector('.day-modal').style.display = 'none';
    document.querySelector('.event-view-modal').style.display = 'none';

    let offcanvasTray = document.querySelector('.offcanvas-tray'), offcanvasTrayToggle = document.querySelector('.offcanvas-tray-toggle'), calendarMain = document.querySelector(".calendar-main");
    if (offcanvasTray.style.left == "0px") {
        offcanvasTray.style.left = "-25vw";
        offcanvasTrayToggle.innerText = ">";
        calendarMain.style.marginLeft = "calc(50% - 35vw)";
    } else if (offcanvasTray.style.left == "-25vw") {
        offcanvasTray.style.left = "0px";
        offcanvasTrayToggle.innerText = "<";
        calendarMain.style.marginLeft = "27vw";
    };
});

for (const button of document.querySelectorAll('.offcanvas-tray-tab-button')) {
    button.addEventListener('click', function(event) {
        for (const tab of document.querySelectorAll(".offcanvas-tab-content")) {
            tab.style.display = "none";
        };
        for (const tabButton of document.querySelectorAll(".offcanvas-tray-tab-button")) {
            tabButton.style.backgroundColor = "cornflowerblue";
        }
        document.querySelector(`#${String(event.currentTarget.id).replace('-button', '')}`).style.display = "block";
        document.querySelector(`#${event.currentTarget.id}`).style.backgroundColor = "white";
    })
};


// Miscs
// Other button-based functions
for (const eventItem of document.querySelectorAll('.close')) {
    eventItem.addEventListener('click', function(event) {
        event.currentTarget.parentNode.parentNode.style.display = 'none';
    });
};

document.querySelector('#button-month-left').addEventListener('click', function() {
    let newDate = new Date(currentYear, currentMonth-1);
    setup(newDate.getMonth(), newDate.getFullYear());
});

document.querySelector('#button-month-right').addEventListener('click', function() {
    let newDate = new Date(currentYear, currentMonth+1);
    setup(newDate.getMonth(), newDate.getFullYear());
});

document.querySelector('#calendar-selector').addEventListener('click', function() {
    document.querySelector('#month-select-modal').style.display = 'flex';
    document.querySelector('#select-month').value = currentMonth + 1;
    document.querySelector('#select-year').value = currentYear;
});

document.querySelector('#confirm-month-select').addEventListener('click', function() {
    // catch empty year field (month cannot be invalid)
    if (isNaN(document.querySelector('#select-year').value)) {
        document.querySelector('#select-year').value = currentYear;
    }
    setup(document.querySelector('#select-month').value - 1, document.querySelector('#select-year').value);
    document.querySelector('#month-select-modal').style.display = 'none'; 
});

document.querySelector('#note-text').addEventListener('change', function() {
    localStorage.setItem("user_notes", document.querySelector('#note-text').value);
});

document.querySelector('#clear-localstorage').addEventListener('click', function() {
    if (confirm('Are you sure you want to delete all events and clear storage? \n This is only really needed whenever a new update is put in.')) {
        localStorage.clear();
        setup(currentMonth, currentYear);
    };
});

// Drag function *used w3 example.... i'm so bad at js...maybe update to be smoother with fast movements by either stealing google's bezier tweening anims + rewrite to not depend on offsets??

function draggable(element) {
    var changeX = 0, changeY = 0, locX = 0, locY = 0;
    element.querySelector('.modal-header').onmousedown = start

    function start(event) {
        event.preventDefault();
        document.onmouseup = clear;
        element.onmousemove = drag;
        locX = event.clientX, locY = event.clientY;
    };

    function drag(event) {
        changeX = locX - event.clientX, changeY = locY - event.clientY, locX = event.clientX, locY = event.clientY;
        element.style.left = `${element.offsetLeft - changeX}px`;
        element.style.top = `${element.offsetTop - changeY}px`;
    }

    function clear() {
        element.onmousemove = null, element.onmouseup = null;
    }
}

draggable(document.querySelector('.day-modal')), draggable(document.querySelector('.event-view-modal'))

document.querySelector('#offc-chatbot').style.display = "block";
document.querySelector('#offc-chatbot-button').style.backgroundColor = "white";

document.querySelector("#spinner-loader-main").style.display = "none"; 
document.querySelector('#favicon').href = `assets/palendar-favico/palendar-favico-${TODAY.getDate()}.png`
// Begin!!!
setup(currentMonth, currentYear);