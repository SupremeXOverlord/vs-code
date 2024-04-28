import python_weather
import asyncio
import tkinter as tk
from tkinter import ttk,messagebox
import os
import threading
#imports

root = tk.Tk()
root.geometry("1000x500")
background = tk.Frame(root)
secondaryBGR = tk.Frame(root)
system = ["Metric","Imperial"]
Possibilities = ["Feels like","Ultraviolet","wind speed","Humidity"]
CityError = False
SysError = False
AlUsed = False

#global variables
global FinalTemp

# Ensure correct loop policy
if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


#optimize ui
#base idea off web, not a vital function
loop = asyncio.new_event_loop()

def runLoop(loop, stop):
    asyncio.set_event_loop(loop)
    while not stop.is_set():
        loop.run_until_complete(asyncio.sleep(0.1))
    loop.stop()
    loop.close()

# Start a background thread for handling asyncio tasks
stop = threading.Event()
thread = threading.Thread(target=runLoop, args=(loop, stop))
thread.start()

#so program will stop when window is closed
def on_closing():
    stop.set() 
    thread.join()  
    root.destroy()  

root.protocol("WM_DELETE_WINDOW", on_closing)
##


def getSystem():
    global setSys,ending,chosenSys,PrecipLength,speed
    chosenSys = selSystem.get()
    if chosenSys == "Imperial":
      setSys = python_weather.IMPERIAL
      ending = "°F"
      PrecipLength="Inches"
      speed = "MPH"
      print("imperial")
    elif chosenSys == "Metric":
      setSys = python_weather.METRIC
      ending = "°C"
      PrecipLength = "MM"
      speed = "KMH"
      print("Metric")
    else:
      print("Please select a valid option!")

#start progress bar to go once
def progress(steps,stepLen):
    bar.pack(pady=20)
    for i in range(steps):
      bar.step(stepLen)  # Update progress
      root.update_idletasks() 
      root.after(20)


#-------------------------------------------------------------


#main function to get weather from city

async def getweather(city):
  global setSys,ending,FinalTemp,weather
  async with python_weather.Client(unit=setSys) as client:

    weather = await client.get(city)
    
    print("Getting temp for", weather," at current time")
    print(weather.country)
    print(weather.temperature,ending)
    FinalTemp = weather.temperature
    





# Main function for fetching weather data and updating the UI
def buttonPress(SelectedCity,loopAmt):
    
    global StrFinal,ending,LocYCount,AlUsed
    
    CityErrorCheck()
    SysErrorCheck()
    if CityError or SysError:
        return
    
     # Get the temperature system and fetch weather data asynchronously
    getSystem()
    criteria = enterCity.get()
    asyncio.run_coroutine_threadsafe(getweather(SelectedCity), loop)
    
    for i in range(loopAmt):
        progress(50,2)
    if AlUsed == True:
       precipitation.config(text="Precipitation",command=precip)
       AlUsed=False
    bar.pack_forget()
    LocYCount = "in " + str(weather.location)+", "+str(weather.country) +" It is Currently"
    FinLabel.config(text=LocYCount)
    background.pack_forget()
    StrFinal=str(FinalTemp)
    temp.config(text=(StrFinal+ending+" and "+str(weather.kind)))
    #CityLabel.config(text=testVar)
    secondaryBGR.pack(pady=20)
    
    
    
    

#Check for errors
def CityErrorCheck():
    global CityError, error
    error = False
    # Check if the city input is empty, displaying an error message if true
    if len(enterCity.get()) == 0:
        messagebox.showinfo(title="Error!", message="Please type a city!")
        CityError = True
    else:
        CityError = False

# Check for a valid temperature system
def SysErrorCheck():
    global SysError
    if selSystem.get() not in ["Imperial", "Metric"]:
        messagebox.showinfo(title="Error!", message="Please select a valid Temperature System!")
        SysError = True
    else:
        SysError = False

def precip():
   global AlUsed
   progress(50,2)
   weather.precipitation
   FinLabel.config(text="Precipitation in " + str(weather.location)+", "+str(weather.country)+" is currently")
   temp.config(text=(str(weather.precipitation)+" "+str(PrecipLength)))
   precipitation.config(text="return?",command=lambda: buttonPress(enterCity.get(),1))
   AlUsed = True

def otherPos():
    global AlUsed
    print(weather.kind)
    progress(50,2)
    bar.pack_forget()
    AlUsed=True
    precipitation.config(text="return?",command=lambda: buttonPress(enterCity.get(),1))
    
    #"Feels like","Ultraviolet","wind speed","Humidity"]
    selected = others.get()
    if selected == "Feels like":
        FinLabel.config(text="In " + str(weather.location)+" it currently feels like")
        temp.config(text=str(weather.feels_like)+str(ending))
    elif selected=="Ultraviolet": #ss
        FinLabel.config(text="In " + str(weather.location)+" the UV Index is")
        temp.config(text=str(weather.ultraviolet))
        print(weather.ultraviolet)
    elif selected == "wind speed": #ss
       FinLabel.config(text="In " + str(weather.location)+" the wind speed and direction is")
       temp.config(text=(str(weather.wind_speed) +" "+speed+" heading "+ str(weather.wind_direction)))
    elif selected =="Humidity":
       
       FinLabel.config(text="Humidity Percentage in " + str(weather.location)+" is currently")
       temp.config(text=str(str(weather.humidity)+"%"))
       

#----------
# create buttons


main = tk.Label(background,text="Computer Science Weather Station",font=("arial","50"))

selSystem = ttk.Combobox(background,values=system,state="readonly")
selSystem.set("Imperial")

criterion = tk.Label(background,text="Please Input Desired City!",font=("arial","25"))

enterCity= tk.Entry(background,width="30")
submit = tk.Button(background,text="Submit",command=lambda: buttonPress(enterCity.get(),2),width=15,height=2,background="White",relief="raised")
FinLabel=tk.Label(secondaryBGR,font=("Arial 50"))

CityLabel=tk.Label(secondaryBGR,font=("arial","45"))

temp = tk.Label(secondaryBGR,font=("Arial","50"))

bar = ttk.Progressbar(length=500)

precipitation = tk.Button(secondaryBGR,text="Precipitation",relief="groove",width="20",height="2",font="arial",command=precip)

OtrLabel = tk.Label(secondaryBGR,text="Others:")
others = ttk.Combobox(secondaryBGR,values=Possibilities,state="readonly")
otrConf= ttk.Button(secondaryBGR,text="Confirm",command=otherPos)

#pack buttons
background.pack()
criterion.pack()
enterCity.pack()
submit.pack(pady=6)
main.pack()
selSystem.pack()
FinLabel.pack()
temp.pack()
CityLabel.pack()
precipitation.pack(pady=5)
OtrLabel.pack()
others.pack(pady=15)
otrConf.pack()

#keep window open
root.mainloop()

