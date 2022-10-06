import time

import requests
import wikipedia as wk

dayWords = ["First","Second","Third","Fourth","Fifth","Sixth","Seventh","Eighth","Ninth","Tenth","Eleventh",
            "Twelvfth","Thirteenth","Fourteenth","Fifteenth","Sixteenth","Seventeenth","Eighteenth","Nineteenth",
            "Twentieth","Twenty-first","Twenty-second","Twenty-third","Twenty-fourth","Twenty-fifth","Twenty-sixth",
            "Twenty-seventh","Twenty-eigth","Twenty-ninth","Thirtieth","Thirty-first"]
monthWords = {"Jan":"January","Feb":"Febuary","Mar":"March","Apr":"April","May":"May","Jun":"June","Jul":"July","Aug":"August","Sep":"September","Oct":"October","Nov":"November","Dec":"December"}

dayNames = {"Mon":"Monday", "Tue":"Tuesday", "Wed":"Wednesday", "Thu":"Thursday", "Fri":"Friday", "Sat":"Saturday", "Sun":"Sunday"}

#Opens serial connection to remote for lights
# ser = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
# ser.reset_input_buffer()

# def lights(color):
#     ser.write(bytes(color, "utf-8"))
#     print("Sent color code: " + color)
    
# def lightDance():
#     ser.write(bytes("DANCE", "utf-8"))
    
def find_nth(haystack, needle, n):
   start = haystack.find(needle)
   while start >= 0 and n > 1:
       start = haystack.find(needle, start+len(needle))
       n -= 1
   return start
 
 
def define(term):
 summary = wk.summary(term, 1)
 
 return summary


def what___IsIt(timeType):
    # Gets current date and time info
    info = time.ctime()
    day, month, date, tim, year = info.split()
    hours, minutes, seconds = tim.split(":")

    if timeType == "time":
        # Converts Military to 12-hour time and removes seconds
        if int(hours) > 12:
            hours = int(hours) - 12
            hours = str(hours)
            tim = str(hours) + ":" + str(minutes) + "PM"
        else:
            tim = str(hours) + ":" + str(minutes) + "AM"
        return tim

    elif timeType == "date" or timeType == "day":
        #convert number date to word date
        date = dayWords[int(date) - 1]

        #Convert abbreviated month to full name
        month = monthWords[month]

        #Add on other date info
        fullDate = "It is the " + date + " of " + month + ", " + year
        return fullDate
    
    elif timeType == "day_only":
        dayName = dayNames.get(day)
        return dayName
    
    elif timeType == "raw_date":
        return date, month, year

def getWeather(location = "san diego", t = "all"):
	# set the url to perform the get request
	baseStr = "https://www.google.com/search?q=weather+"
	newStr = ""
	#Replace all spaces with pluses
	for i in location:
		if i == " ":
			i = "+"
		newStr += (i)
	finalUrl = baseStr + newStr

	#Get the HTML for the page
	page = requests.get(finalUrl)

	# load the page content
	text = page.content
	text = text.decode("latin1")
	text = text[:35000]

	if t == "all":
		#gets the temperature
		identifier = '<div class="BNeawe iBp4i AP7Wnd">'
		lower = text.find(identifier) + len(identifier)
		t = text[lower:]
		lower = t.find(identifier) + len(identifier) + lower
		upper = t.find("</div>") + lower - len(identifier) - 7
		temperature = text[lower:upper]


		# gets the sky state (ie: cloudy, rainy, clear)
		identifier = '<div class="BNeawe tAd8D AP7Wnd">'
		lower = text.find(identifier) + len(identifier)
		t = text[lower:]
		lower = t.find(identifier) + len(identifier) + lower
		upper = t.find("</div>") + lower - len(identifier) - 5
		sky = text[lower:upper]
		sky = sky[sky.find("\n")+1:]


		return sky, temperature

	elif t == "temperature":
		# gets the temperature
		identifier = '<div class="BNeawe iBp4i AP7Wnd">'
		lower = text.find(identifier) + len(identifier)
		t = text[lower:]
		lower = t.find(identifier) + len(identifier) + lower
		upper = t.find("</div>") + lower - len(identifier) - 7
		temperature = text[lower:upper]
		return temperature

	elif t == "skyState":
		# gets the sky state (ie: cloudy, rainy, clear)
		identifier = '<div class="BNeawe tAd8D AP7Wnd">'
		lower = text.find(identifier) + len(identifier)
		t = text[lower:]
		lower = t.find(identifier) + len(identifier) + lower
		upper = t.find("</div>") + lower - len(identifier) - 5
		sky = text[lower:upper]
		sky = sky[sky.find("\n") + 1:]
		return sky

	else:
		raise ValueError("Only a parameter of 'temperature' or 'skyState' are allowed")
	

def forecast(day, location = "San Diego"):
    print("Called forecast")
    #Possible args for day: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday
    
    identifier = "°"
    
    # set the url to perform the get request
    baseStr = "https://www.google.com/search?q=weather+"
    newStr = ""
    #Replace all spaces with pluses
    for i in location:
        if i == " ":
            i = "+"
        newStr += (i)
    finalUrl = baseStr + newStr + "+" + day

    #Get the HTML for the page
    page = requests.get(finalUrl)

    # load the page content
    text = page.content
    text = text.decode("latin1")
    
    f = open("output.html", "w")
    
    f.write(text)
    f.close()
    
    location = text.find(identifier)
    
    start = location - 4
    
    end = location
    
    while text[start] != " ":
        start += 1
    
    start += 1
    
    temperature = text[start:end]
    
    spaceCount = 0
    
    while spaceCount <= 3:
        while text[location] != " ":
            location -= 1
        spaceCount += 1
    
    end = location
    
    start = end - 1
    
    while text[start] != " ":
        start -= 1
    
    skyState = text[start:end]
    
    start = skyState.find("\n") + 1
    end = skyState[start:].find("\n") + start
    
    skyState = skyState[start:end]
    
    
    
    return temperature, skyState

print(forecast(what___IsIt("day_only")))