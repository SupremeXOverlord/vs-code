import python_weather
import asyncio
import time
import tkinter as tk
from tkinter import ttk,messagebox
import os
#imports
global criteria,FinalTemp
#basic variables
root = tk.Tk()
root.geometry("1000x500")
background = tk.Frame(root)
secondaryBGR = tk.Frame(root)

system = ["Metric","Imperial"]
##########




bar = ttk.Progressbar(background)

def getSystem():
    global setSys,ending
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
      exit()


#start progress bar to go once
def progress():
    for i in range(100):
      bar.step(1)  # Update progress
      root.update_idletasks()  # Ensure UI updates
      time.sleep(0.02)  # Simulate some work
#-------------------------------------------------------------


#main function to get weather from city
async def getweather(city):
  global setSys,ending,FinalTemp
  async with python_weather.Client(unit=setSys) as client:

    weather = await client.get(city)
    print("Getting temp for", weather," at current time")
    #spinning_cursor()
    print(weather.country)
    print(weather.temperature,ending)
    FinalTemp = weather.temperature
  if __name__ == '__main__':
    if os.name == 'nt':
      asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


#function ran when button is pressed

  
  
def buttonPress():
  global criteria
  CityErrorCheck()
  bar.pack()
  getSystem()
  criteria = enterCity.get()
  asyncio.run(getweather(criteria))
  
  progress()
  time.sleep(.08)
  background.pack_forget()
  secondaryBGR.pack()
def CityErrorCheck():
  global criteria
  if len (enterCity.get())==0:
    messagebox.showinfo(title="Error!",message="Please type a city!")
def SysErrorCheck():
  if len (enterCity.get())==0:
    messagebox.showinfo(title="Error!",message="Please select a valid Temperature System!")   

  submit = tk.Button(background,text="Submit",command=buttonPress,width=15,height=2,background="White",)

main = tk.Label(background,text="Computer Science Weather Station",font=("arial","50"))

selSystem = ttk.Combobox(background,values=system)
selSystem.set("Imperial")

criterion = tk.Label(background,text="Please Input Desired City's Weather, and Country!",font=("arial","25"))

enterCity= tk.Entry(background,width="30")

temp = tk.Label(secondaryBGR,text="test")

background.pack()
criterion.pack()
enterCity.pack()
submit.pack()
main.pack()
selSystem.pack()
temp.pack()
root.mainloop()


