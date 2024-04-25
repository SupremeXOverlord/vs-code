import turtle as trtl
import python_weather
import asyncio
import time
import tkinter as tk
#city = input("what city (City, State) " )
root = tk.Tk()
root.geometry("1000x500")
background = tk.Frame(root)
secondaryBGR = tk.Frame(root)
background.pack()
unit = [python_weather.METRIC,python_weather.IMPERIAL]

set = 0
main = tk.Label(root,text="Computer Science Weather Station",font=("arial","50"))
main.pack()



criterion = tk.Label(root,text="Please input desired city's weather",font=("arial","25"))
criterion.pack()

enterCity= tk.Entry(width="30")
enterCity.pack()



def spinning_cursor():
  for i in range(5):
    for cursor in '\\|/-':
      time.sleep(0.1)
      print(f"\r{cursor}", end="", flush=True)
  
def progress_bar():
  for i in range(11):
    time.sleep(0.1)
    print(f"\r{i:02d}: {'#'*(i//2)}", end="", flush=True)

async def getweather(city,):
  async with python_weather.Client(unit=python_weather.IMPERIAL) as client:

    weather = await client.get(city)
    print("Getting temp for", weather," at current time")
    #spinning_cursor()
    print(weather.country)
    print(weather.temperature)

def buttonPress():
  secondaryBGR.pack()
  asyncio.run(getweather(criterion))

submit = tk.Button(text="Submit",command=buttonPress)
submit.pack()

root.mainloop()


