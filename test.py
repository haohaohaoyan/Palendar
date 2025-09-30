import datetime, json

#Constant time name lists
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def writedate():
    #Write dates to events file. Will be replaced with query boxes in final html form
    with open("events.txt", "a+") as eventsource:
        #Set of questions
        nameI = str(input("Name of event: "))
        monthI = int(input("Month of date: "))
        dayI = int(input("Day of date: "))
        yearI = int(input("Year of date: "))
        priorityI = int(input("Priority of event: "))

        #Dump formatted event into file via json, so that it is readable
        out = dict(name = nameI, date = str(datetime.date(yearI, monthI, dayI)), priority = priorityI)
        #took me 2 hours of research to realize i wrote "/n" instead of "\n"
        eventsource.write('\n')
        json.dump(out, eventsource)

def main():
    #Main process. Ran upon file open, refresh, and after writing dates.
    
    #Fetch current date and print
    currentdate = datetime.date.today()
    print("Today is " + MONTHS[int(currentdate.month) - 1] + " " + str(currentdate.day) + ". It is a " + DAYS[currentdate.weekday()] + ".")

    #Display events, sorted by time and priority. Catches FileNotFound if events.txt doesn't exist *unfinished
    try:
        with open("events.txt", "r") as eventsource:
            print("Events: ")
            for line in eventsource:
                eventS = json.loads(line)
                print(eventS["date"] + ": " + eventS["name"])

    #Create file in case events.txt doesn't exist
    except FileNotFoundError:
        writeescape = input("No events file found. Create one by writing event? y/n")
        if writeescape == "y":
            writedate()
            main()

    #Prompt user to write events
    writestatus = input("write events? y/n ")
    if writestatus == "y":
        writedate()
        main()

main()  
