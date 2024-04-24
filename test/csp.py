import turtle as trtl
import python_weather
import asyncio
import time
import tkinter as tk
city = input("what city (City, State) " )
root = tk.Tk()

background = tk.Frame(root)
background.pack()

main = tk.Label(text="test",fo)
main.pack()











def spinning_cursor():
  for i in range(5):
    for cursor in '\\|/-':
      time.sleep(0.1)
      print(f"\r{cursor}", end="", flush=True)

def progress_bar():
  for i in range(11):
    time.sleep(0.1)
    print(f"\r{i:02d}: {'#'*(i//2)}", end="", flush=True)

async def getweather(city):
  async with python_weather.Client(unit=python_weather.IMPERIAL) as client:

    weather = await client.get(city)
    print("Getting temp for", weather," at current time")
    #spinning_cursor()
    print(weather.country)
    print(weather.temperature)




root.mainloop()
asyncio.run(getweather(city))