import python_weather
import asyncio
import time
import tkinter as tk
from tkinter import ttk
import os
#city = input("what city (City, State) " )
root = tk.Tk()
root.geometry("1000x500")
background = tk.Frame(root)
secondaryBGR = tk.Frame(root)
background.pack()

system = ["Metric","Imperial"]
selSystem = ttk.Combobox(background,values=system)
selSystem.set("What Temperature system would you Like?")
selSystem.place(y=200)
criterion = tk.Label(background,text="Please Input Desired City's Weather, and Country!",font=("arial","25"))
criterion.pack()

enterCity= tk.Entry(background,width="30")
enterCity.pack()


test = ttk.Progressbar(background)

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


#make progress bar go to 100
def progress():
    for i in range(100):
      test.step(1)  # Update progress
      root.update_idletasks()  # Ensure UI updates
      time.sleep(0.02)  # Simulate some work
##############


#main function to get weather from city
async def getweather(city):
  global setSys,ending
  async with python_weather.Client(unit=setSys) as client:

    weather = await client.get(city)
    print("Getting temp for", weather," at current time")
    #spinning_cursor()
    print(weather.country)
    print(weather.temperature,ending)
  if __name__ == '__main__':
    if os.name == 'nt':
      asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


#function ran when button is pressed
def buttonPress():
  
  test.pack()
  getSystem()
  criteria = enterCity.get()
  asyncio.run(getweather(criteria))
  
  progress()
  time.sleep(.4)
  background.pack_forget()
  secondaryBGR.pack()

submit = tk.Button(background,text="Submit",command=buttonPress)
submit.pack()

main = tk.Label(background,text="Computer Science Weather Station",font=("arial","50"))
main.pack()






root.mainloop()


