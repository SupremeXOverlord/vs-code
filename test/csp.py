import python_weather
import asyncio
import time
import tkinter as tk
from tkinter import ttk
#city = input("what city (City, State) " )
root = tk.Tk()
root.geometry("1000x500")
background = tk.Frame(root)
secondaryBGR = tk.Frame(root)
background.pack()
unit2 = [python_weather.METRIC,python_weather.IMPERIAL]
work = False
set = 0




criterion = tk.Label(background,text="Please Input Desired City's Weather, and Country!",font=("arial","25"))
criterion.pack()

enterCity= tk.Entry(background,width="30")
enterCity.pack()


test = ttk.Progressbar(background)


def spinning_cursor():
  for i in range(100):
    for cursor in '\\|/-':
      time.sleep(0.1)
      print(f"\r{cursor}", end="", flush=True)
  
def progress_bar():
  for i in range(11):
    time.sleep(0.1)
    print(f"\r{i:02d}: {'#'*(i//2)}", end="", flush=True)


#main function to get city and get weather
async def getweather(city):
  async with python_weather.Client(unit=python_weather.IMPERIAL) as client:

    weather = await client.get(city)
    print("Getting temp for", weather," at current time")
    #spinning_cursor()
    print(weather.country)
    print(weather.temperature)

def buttonPress():
  criteria = enterCity.get()
  background.pack_forget()
  asyncio.run(getweather(criteria))
  background.pack()
  test.pack()
  for i in range(10):
    test.start()
  

  secondaryBGR.pack()
  

submit = tk.Button(background,text="Submit",command=buttonPress)
submit.pack()

main = tk.Label(background,text="Computer Science Weather Station",font=("arial","50"))
main.pack()






root.mainloop()


