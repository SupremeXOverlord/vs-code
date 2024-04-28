import python_weather
import asyncio
import time
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
CityError = False
SysError = False
#global variables
global FinalTemp

#change settings to window settings
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

stop = threading.Event()
thread = threading.Thread(target=runLoop, args=(loop, stop))
thread.start()

def on_closing():
    stop.set() 
    thread.join()  
    root.destroy()  

root.protocol("WM_DELETE_WINDOW", on_closing)
##




def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        exit()

def getSystem():
    global setSys,ending,chosenSys
    chosenSys = selSystem.get()
    if chosenSys == "Imperial":
      setSys = python_weather.IMPERIAL
      ending = "°F"
      print("imperial")
    elif chosenSys == "Metric":
      setSys = python_weather.METRIC
      ending = "°C"
      print("Metric")
    else:
      print("Please select a valid option!")


#start progress bar to go once
def progress():
    for i in range(100):
      bar.step(1)  # Update progress
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
    


#function ran when button is pressed

  
  
def buttonPress():

    global StrFinal,ending,LocYCount
    
    CityErrorCheck()
    SysErrorCheck()
    if CityError or SysError:
        return
    bar.pack(pady=20)
    getSystem()
    criteria = enterCity.get()
    
    # Schedule the task on the background loop
    asyncio.run_coroutine_threadsafe(getweather(criteria), loop)
    
    #progress()
    time.sleep(3)
    LocYCount = "in " + str(weather.location)+", "+str(weather.country) +" It is Currently"

    FinLabel.config(text=LocYCount)
    background.pack_forget()
    StrFinal=str(FinalTemp)
    print(weather.precipitation)
    temp.config(text=(StrFinal,ending))
    #CityLabel.config(text=testVar)
    secondaryBGR.pack(pady=20)
    

#Check for errors
def CityErrorCheck():
    global CityError, error
    error = False
    if len(enterCity.get()) == 0:
        messagebox.showinfo(title="Error!", message="Please type a city!")
        CityError = True
    else:
        CityError = False

def SysErrorCheck():
    global SysError
    if selSystem.get() not in ["Imperial", "Metric"]:
        messagebox.showinfo(title="Error!", message="Please select a valid Temperature System!")
        SysError = True
    else:
        SysError = False

def precip():
   
   FinLabel.config(text="s")
#----------
# create buttons
submit = tk.Button(background,text="Submit",command=buttonPress,width=15,height=2,background="White")

main = tk.Label(background,text="Computer Science Weather Station",font=("arial","50"))

selSystem = ttk.Combobox(background,values=system,state="readonly")
selSystem.set("Imperial")

criterion = tk.Label(background,text="Please Input Desired City!",font=("arial","25"))

enterCity= tk.Entry(background,width="30")

FinLabel=tk.Label(secondaryBGR,font=("Arial","50"))

CityLabel=tk.Label(secondaryBGR,font=("arial","45"))

temp = tk.Label(secondaryBGR,font=("Arial","50"))

bar = ttk.Progressbar(background,length=500)

precipitation = tk.Button(secondaryBGR,text="Precipitation",relief="groove",width="20",height="2",font="arial",command=precip)
#pack buttons
background.pack()
criterion.pack()
enterCity.pack()
submit.pack()

main.pack()
selSystem.pack()
FinLabel.pack()
temp.pack()
CityLabel.pack()
precipitation.place(x=120,y=180)

#keep window open
root.mainloop()


