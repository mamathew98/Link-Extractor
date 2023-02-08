from tkinter import *
from tkinter import messagebox
import tkinter as tk
import requests
import re
from bs4 import BeautifulSoup
from tkinter import filedialog


def get_links(url, file_types):
    try:
        # Request the website
        res = requests.get(url)
    except:
        messagebox.showerror('Error 404', 'URL Not Found!')
        return []
    # Parse the HTML content
    soup = BeautifulSoup(res.text, 'html.parser')
    # Find all links in the HTML
    links = soup.find_all('a')
    # Filter links that match the specified file types
    filtered_links = [link['href'] for link in links if 'href' in link.attrs and any(ft in link['href'] for ft in file_types)]
    return filtered_links

def save():
    links = listbox_links.get(0, END)
    if not links:
        messagebox.showerror('Error 404', 'No Links Available!')
        return
    file_name = filedialog.asksaveasfilename(defaultextension='.txt')
    with open(file_name, 'w') as f:
        for link in links:
            f.write(link + '\n')
            
def submit_handler():
    url = entry_url.get()
    file_types = entry_file_types.get().split(', ')
    links = get_links(url, file_types)
    listbox_links.delete(0, 'end')
    for link in links:
        listbox_links.insert('end', link)

root = tk.Tk()
root.iconphoto(False, tk.PhotoImage(file='D:\CODE\Link Extractor\icon.png'))
root.title("Download Links Extractor")

frame_url = tk.Frame(root, bg='#BDBDBD')
frame_url.pack(pady=10)

label_url = tk.Label(frame_url, text='Enter URL:', bg='#BDBDBD', height=2)
label_url.pack()

entry_url = tk.Entry(frame_url, width=60, bg='#F5F5F5')
entry_url.pack(side='left')

frame_file_types = tk.Frame(root, bg='#BDBDBD')
frame_file_types.pack(pady=10)

label_file_types = tk.Label(frame_file_types, text="Enter file types separated by a comma (e.g. '.zip, .pdf'):", bg='#BDBDBD', height=2)
label_file_types.pack()

entry_file_types = tk.Entry(frame_file_types, width=60, bg='#F5F5F5')
entry_file_types.pack(side='left')

frame_buttons = tk.Frame(root, bg='#2f2f2f')
frame_buttons.pack(pady=10)

button_submit = tk.Button(frame_buttons, text='Extract Links', command=submit_handler, width=30)
button_submit.pack()

button_save = tk.Button(frame_buttons, text='Save Links', command=save, width=30)
button_save.pack(pady=5)


frame_listbox = tk.Frame(root)
frame_listbox.pack(fill=BOTH, expand=True)
listbox_links = Listbox(frame_listbox, selectmode='multiple', bg='#F5F5F5')
listbox_links.pack(fill=BOTH, expand=True)

scrollbarX = tk.Scrollbar(listbox_links, orient='vertical')
scrollbarX.pack(side='right', fill='y')

scrollbarX.config(command=listbox_links.yview)
listbox_links.config(yscrollcommand=scrollbarX.set)

root.configure(background='#2f2f2f')
root.geometry("700x500")

root.mainloop()
