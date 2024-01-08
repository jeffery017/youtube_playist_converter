import customtkinter as ctk
from converter import *


# ========== basic setting ==============
app = ctk.CTk()
app.geometry('400x650')
# app.iconphoto('iconphoto', 'icon.png')
app.minsize(350, 300)
app.title("YouTube Playlist Converter")
app.rowconfigure(2, weight=1)
app.columnconfigure(0, weight=1)


# ========== functions =================
def click(event): # clear url entry content while click
  url_entry.configure(state='normal')
  url_entry.delete(0, ctk.END)
  url_entry.unbind('<Button-1>', clicked)

def updateMessage(msg): # to change the text content of message label
  message.configure(text=msg)
  message.update()

def updateContentBox(newContent):
  content_box.delete(1.0, ctk.END)
  content_box.insert(ctk.END, newContent)
  
def copyContentToClipboard():
  copyToClipboard(content_box.get("1.0", ctk.END))
  updateMessage("Copy to Clipboard")
  
def convert(): # fetch url and parse html content to video info list
  updateMessage('Fetching data from YouTube...')
  global videos
  videos = getVideoRawDataFromPlaylist(URL.get())

  if len(videos) == 0:
    updateMessage('No Video Found.')
    updateContentBox("")
    return
  updateContentBox(videosToMd(videos))
  updateMessage('Complete')




  # if addTime.get():
  #   txt = videosToTxtWithLength(videos)
  #   md = videosToMdWithLength(videos)
  # else:
  #   txt = videosToTxt(videos)
  #   md = videosToMd(videos)

  # updateMessage('Complete')





# ============= Variable ================

URL = ctk.StringVar()
format = ctk.IntVar()
containsTime = ctk.BooleanVar()
message = ctk.StringVar()
addTime = ctk.BooleanVar()
videos = []

# =============== Create =================
# Blocks
head = ctk.CTkFrame(master=app)
head.columnconfigure(1, weight=1)
body = ctk.CTkFrame(master=app)
body.columnconfigure(0, weight=1)
body.rowconfigure(0, weight=1)
dashboard = ctk.CTkFrame(master=app)
dashboard.columnconfigure(0, weight=1)
footer = ctk.CTkFrame(master=app, corner_radius=0)
footer.columnconfigure(0, weight=1)

# Components
title = ctk.CTkLabel(master=app, text=str.upper("YouTube Playlist Converter"), font=("Helvetica Bold", 20))
# URL
url_lab = ctk.CTkLabel(master=head, text='URL', anchor="w")
url_entry = ctk.CTkEntry(master=head, textvariable=URL)
url_entry.insert(0, 'https://www.youtube.com/playlist?list=PLuxlg1BYq9r2bYL4GBrCvCH7iTLRHSDxI')
clicked = url_entry.bind('<Button-1>', click)
convert_btn = ctk.CTkButton(master=head, text="▶", command=convert, width=20)


content_box = ctk.CTkTextbox(master=body )
format_lab = ctk.CTkLabel(master=dashboard, text='Format', anchor='w')
md_radio = ctk.CTkRadioButton(master=dashboard, text='Markdown URL',value=0, variable=format, command=lambda:updateContentBox(videosToMd(videos)))
txt_radio = ctk.CTkRadioButton(master=dashboard, text='Title Only', value=1, variable=format, command=lambda:updateContentBox(videosToTxt(videos)))
# txt_btn = ctk.CTkButton(master=dashboard, text="Title only", command=lambda:updateContentBox(videosToTxt(videos)), width=20)
# md_btn = ctk.CTkButton(master=dashboard, text="Markdown", command=lambda:updateContentBox(videosToMd(videos)), width=20)
copy_btn = ctk.CTkButton(master=dashboard, text="Copy to Clipboard", command=copyContentToClipboard, width=20)
message = ctk.CTkLabel(master=footer, text="Yichi Lin")

# ============== Block Layout =================
title.grid( pady = (10,0), sticky='nsew')
head.grid(padx=10, pady = 10, sticky='nsew')
body.grid(padx=10, pady = (0,10), sticky="nsew")
dashboard.grid(sticky="nsew", padx=10, pady=(0, 10))
footer.grid(sticky="nsew")

# Elements
url_lab.grid(row=0, column=0,sticky="nsew", padx=(10,5), pady=10)
url_entry.grid(row=0, column=1,sticky="nsew", pady=10)
convert_btn.grid(row=0, column=2 ,sticky="nsew", padx=(5, 10), pady=10)


content_box.grid(columnspan=2, padx=10, pady = 10,  sticky="nsew")
format_lab.grid(row=0, column=0, padx=(20,5),pady=10,  sticky="nsew")
md_radio.grid(row=0, column=1, pady=10)
txt_radio.grid(row=0, column=2, padx=(5,20), pady=10)
copy_btn.grid(row=1, columnspan=3, padx=10, pady=(0, 10), ipady=5,  sticky="ew")

message.grid(padx=20, pady = (0, 10),  sticky="nsew")


# =======================================
head.mainloop()