import tkinter as tk
from tkinter import *
from datetime import datetime
from tkinter import simpledialog
import requests



def load_events():
    events = []
    with open('sobitia.txt', 'r', encoding='utf-8') as f:
        for line in f:
            name, date_str = line.strip().split(',')
            date = datetime.strptime(date_str, '%Y-%m-%d')
            events.append((name, date))

    events.append((f'Сегодня ({date.today().date()})', datetime.now().strftime('%Y-%m-%d')))
    return events

def update_events(listbox):
    now = datetime.now().date()
    sorted_events = sorted(events, key=lambda e: datetime.strptime(e[1], '%Y-%m-%d') if isinstance(e[1], str) else e[1])
    listbox.delete(0, tk.END)
    for event in sorted_events:
        if isinstance(event[1], str):
            event_date = datetime.strptime(event[1], '%Y-%m-%d').date()
        else:
            event_date = event[1].date()

        days_left = (event_date - now).days

        if days_left < 0:
            listbox.insert(tk.END, f'Прошло {-days_left} дней от {event[0]}')
            listbox.itemconfig(tk.END, {'fg': '#017005'})  
        elif days_left == 0:
            listbox.insert(tk.END, f'Cобытие сегодня: {event[0]}')
            listbox.itemconfig(tk.END, {'fg': '#00bd06'})  
        else:
            listbox.insert(tk.END, f'Осталось {days_left} дней до {event[0]}')
            listbox.itemconfig(tk.END, {'fg': '#9cff9f'})  



def ask_for_city():
    global city_label
    global city
    city = 'Санкт-Петербург'
    city = simpledialog.askstring("Input", "Введите город: ")
    city_label.config(text=f"Выбранный город: {city}")

def open_weather():
    new_window = tk.Toplevel()
    new_window.title("Погода")
    new_window.geometry("400x170")
    tk.Label(new_window,font=("Courier", "15", "bold"),  bg='#0afc8f',foreground=('#001a0e'), text=f"Погода в городе: {city}").pack(fill=X)
    url = 'https://api.openweathermap.org/data/2.5/weather?q='+city+'&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'
    weather_data = requests.get(url).json()
    temperature = round(weather_data['main']['temp'])
    temperature_feels = round(weather_data['main']['feels_like'])
    tk.Label(new_window,font=("Courier", "15"), foreground=('#001a0e'), text=f"Сейчас в городе {str(temperature)} °C").pack(pady=15)
    tk.Label(new_window,font=("Courier", "15"), foreground=('#001a0e'), text=f"Ощущается как {str(temperature_feels)} °C").pack(pady=15)
    

if __name__ == '__main__':
    
    root = tk.Tk()
    root.title("Список дел")
    root.geometry("800x500")
    icon = PhotoImage(file="img/cat.png")
    root.iconphoto(False, icon)

    event_label = tk.Label(root, text="Список событий:", bg='#0afc8f', font=("Courier", "27", "bold"), foreground=('#001a0e'), relief="ridge")
    event_label.pack(side=tk.TOP, fill=tk.BOTH)

    events_listbox = tk.Listbox(root, font=("Courier", "15", "bold"), bg="#1c1c1c")
    events_listbox.pack(fill=tk.BOTH)

    events = load_events()
    update_events(events_listbox)
    root.after(86400000, update_events, events_listbox)  
  
    weather_label = tk.Label(root, text="Погода:", bg='#0afc8f', font=("Courier", "27", "bold"), foreground=('#001a0e'), relief="ridge")
    weather_label.pack(side=tk.TOP, fill=tk.BOTH)
    city = 'Санкт-Петербург'
    city_label = tk.Label(root,font=("Courier", "17", "bold"),   text="Выбранный город: ")
    city_label.config(font=("Courier", "17", "bold"),  text=f"Выбранный город: Санкт-Петербург" )
    city_label.pack(pady=10)

    button_new_window = tk.Button(root,font=("Courier", "15", "bold"), bg='#00c26b', text="Узнать погоду!", command=open_weather)
    button_new_window.pack()

    button_ask_city = tk.Button(root,font=("Courier", "15", "bold"), bg='#00c26b', text="Изменить город", command=ask_for_city)
    button_ask_city.pack(pady=10)


    root.mainloop()
