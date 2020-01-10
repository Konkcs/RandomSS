import requests
import random
import string
from bs4 import BeautifulSoup
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from datetime import datetime
import os

cur_img = ''

def getimg():
    global cur_img

    url = 'https://prnt.sc/'

    randstr = random.choice(string.ascii_lowercase) + random.choice(string.ascii_lowercase)
    rand = random.randint(1111, 9999)

    url2 = url+randstr+str(rand)

    r = requests.get(url2, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
     'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36'})

    if'//st.prntscr.com/2019/11/26/0154/img/0_173a7b_211be8ff.png' in r.text:
        getimg()
    else:
        cur_img = url2
        source = r.text
        soup = BeautifulSoup(source, 'lxml')
        image = soup.find('img')['src']

        print(f'Generated a new url: {url2} #{total_this_session+1}')

        response = requests.get(image)
        with open("stuff/temp_img.png", 'wb') as f:
            f.write(response.content)
    return
total_this_session = 0

def new(event):
    global my_label
    global button_new
    global total_this_session
    getimg()
    total_this_session += 1
    my_label.grid_forget()
    rand_img = ImageTk.PhotoImage(Image.open('stuff/temp_img.png'))
    my_label = Label(root, image=rand_img)
    my_label.photo = rand_img
    my_label.grid(row=1, column=0, columnspan=3)
    root.title(f'Prnt.sc random screenshot. Total this session: {total_this_session}')

def copy():
    root.clipboard_clear()
    root.clipboard_append(cur_img)

def save():
    try:
        if 'saved' not in os.listdir():
            os.mkdir('saved')
        now = datetime.now()
        date_string = now.strftime('%d-%m-%Y')
        if date_string not in os.listdir('saved'):
            os.mkdir(f'saved/'+date_string)
        time_string = now.strftime('%H-%M-%S')
        os.rename('stuff/temp_img.png', f'saved/{date_string}/{time_string}.png')
        messagebox.showinfo('Success', 'Image was saved.\n(You can close me with space also!)')
        print('Sent success infobox')
    except:
        messagebox.showerror('Error', 'There was an error saving your image. '
                                      'Please manually save by going to /stuff/temp_img.png')
        print('Sent error infobox')


root = Tk()
root.title(f'Prnt.sc random screenshot. Total this session: 0')

rand_img = ImageTk.PhotoImage(Image.open('stuff/konk.png'))
my_label = Label(image=rand_img)
my_label.grid(row=1, column=0, columnspan=3 )

button_new = Button(root, text='Copy', command=lambda: copy())
button_save = Button(root, text='Save', command=lambda : save())

button_new.grid(row=0, column=0)
button_save.grid(row=0, column=2)


root.configure(background='black')
root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file='stuff/konk.png'))
root.bind('<space>', new)
print('Sent welcome infobox')
messagebox.showinfo('Welcome', 'press spacebar to get load a fresh image and destroy the current one\n'
                               '(You can close me with space also!)')
root.mainloop()
