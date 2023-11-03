import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox, Text
from requests import get  
import os, subprocess
import threading
versions =  {
    "1.20.2": "https://api.papermc.io/v2/projects/paper/versions/1.20.2/builds/241/downloads/paper-1.20.2-241.jar",
    "1.20.1": "https://api.papermc.io/v2/projects/paper/versions/1.20.1/builds/196/downloads/paper-1.20.1-196.jar",
    "1.20": "https://api.papermc.io/v2/projects/paper/versions/1.20/builds/17/downloads/paper-1.20-17.jar",
    "1.19.4": "https://api.papermc.io/v2/projects/paper/versions/1.19.4/builds/550/downloads/paper-1.19.4-550.jar",
    "1.19.3": "https://api.papermc.io/v2/projects/paper/versions/1.19.3/builds/448/downloads/paper-1.19.3-448.jar",
    "1.19.2": "https://api.papermc.io/v2/projects/paper/versions/1.19.2/builds/307/downloads/paper-1.19.2-307.jar",
    "1.19.1": "https://api.papermc.io/v2/projects/paper/versions/1.19.1/builds/111/downloads/paper-1.19.1-111.jar",
    "1.19": "https://api.papermc.io/v2/projects/paper/versions/1.19/builds/81/downloads/paper-1.19-81.jar",
    "1.18.2": "https://api.papermc.io/v2/projects/paper/versions/1.18.2/builds/388/downloads/paper-1.18.2-388.jar",
    "1.18.1": "https://api.papermc.io/v2/projects/paper/versions/1.18.1/builds/216/downloads/paper-1.18.1-216.jar",
    "1.18": "https://api.papermc.io/v2/projects/paper/versions/1.18/builds/66/downloads/paper-1.18-66.jar",
    "1.17.1": "https://api.papermc.io/v2/projects/paper/versions/1.17.1/builds/411/downloads/paper-1.17.1-411.jar",
    "1.17": "https://api.papermc.io/v2/projects/paper/versions/1.17/builds/79/downloads/paper-1.17-79.jar",
    "1.16.5": "https://api.papermc.io/v2/projects/paper/versions/1.16.5/builds/794/downloads/paper-1.16.5-794.jar",
    "1.16.4": "https://api.papermc.io/v2/projects/paper/versions/1.16.4/builds/416/downloads/paper-1.16.4-416.jar",
    "1.16.3": "https://api.papermc.io/v2/projects/paper/versions/1.16.3/builds/253/downloads/paper-1.16.3-253.jar",
    "1.16.2": "https://api.papermc.io/v2/projects/paper/versions/1.16.2/builds/189/downloads/paper-1.16.2-189.jar",
    "1.16.1": "https://api.papermc.io/v2/projects/paper/versions/1.16.1/builds/138/downloads/paper-1.16.1-138.jar",
    "1.15.2": "https://api.papermc.io/v2/projects/paper/versions/1.15.2/builds/393/downloads/paper-1.15.2-393.jar",
    "1.14.4": "https://api.papermc.io/v2/projects/paper/versions/1.14.4/builds/245/downloads/paper-1.14.4-245.jar",
    "1.13.2": "https://api.papermc.io/v2/projects/paper/versions/1.13.2/builds/657/downloads/paper-1.13.2-657.jar",
    "1.12.2": "https://api.papermc.io/v2/projects/paper/versions/1.12.2/builds/1620/downloads/paper-1.12.2-1620.jar",
    "1.11.2": "https://api.papermc.io/v2/projects/paper/versions/1.11.2/builds/1106/downloads/paper-1.11.2-1106.jar",
    "1.10.2": "https://api.papermc.io/v2/projects/paper/versions/1.10.2/builds/918/downloads/paper-1.10.2-918.jar",
    "1.9.4": "https://api.papermc.io/v2/projects/paper/versions/1.9.4/builds/775/downloads/paper-1.9.4-775.jar",
    "1.8.8": "https://api.papermc.io/v2/projects/paper/versions/1.8.8/builds/445/downloads/paper-1.8.8-445.jar"
  }

def download(url, file_name,folder):    
    os.mkdir(folder)
    with open(f'{folder}/{file_name}', "wb") as file:
        response = get(url)              
        file.write(response.content)   

def start_server():
    inp_version = version_entry.get()
    folder_name = folder_entry.get()
    ram_set = ram_entry.get()

    if inp_version not in versions:
        messagebox.showerror("Error", "잘못된 버전입니다")
        return
    if ram_set.isdigit() is False:
        messagebox.showerror("Error","램 할당은 숫자만 입력해주세요")
        return
    log_text.configure(state="normal") 
    log_text.insert(tk.END, f"다운로드 폴더: {folder_name}\n버전: Paper {inp_version}\nRAM 할당: {ram_set}GB\n")
    log_text.configure(state="disabled")

    def run_task():
        url = versions[inp_version]
        download(url, "server.jar", folder_name)

        with open(f'{folder_name}/prestart.bat','w') as f:
            f.write(f'@echo off \njava -Xms{ram_set}G -Xmx{ram_set}G -Dcom.mojang.eula.agree=true -jar server.jar -nogui  \npause')
        with open(f'{folder_name}/start.bat','w') as f:
            f.write(f'@echo off \njava -Xms{ram_set}G -Xmx{ram_set}G -jar server.jar -nogui  \npause')
        log_text.configure(state="normal")
        log_text.insert(tk.END, f"서버 구성중\n")
        log_text.configure(state="disabled")
        cmd = 'prestart.bat'
        cwd = f'{folder_name}\\'
        process = subprocess.run(cmd, cwd=cwd, shell=True, input='stop', text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        eula_content = ''
        with open(f'{folder_name}/eula.txt','r',encoding="UTF-8") as f:
            eula_content = f.read()
        eula_content = eula_content.replace('false','true')
        with open(f'{folder_name}/eula.txt','w',encoding="UTF-8") as f:
            f.write(eula_content)
        os.remove(f'{folder_name}\\prestart.bat')
        
        log_text.configure(state="normal")
        log_text.insert(tk.END, "설치가 완료되었습니다\n")
        log_text.configure(state="disabled")
        messagebox.showinfo('AutoSpigot','설치가 완료되었습니다.')

    task_thread = threading.Thread(target=run_task)
    task_thread.start()

root = tk.Tk()
root.title("AutoPaper")
version_label = tk.Label(root, text="Minecraft 버전 (1.8.8 - 1.20.2):")
version_entry = tk.Entry(root)

folder_label = tk.Label(root, text="다운로드 폴더 이름:")
folder_entry = tk.Entry(root)

ram_label = tk.Label(root, text="RAM 할당 (GB):")
ram_entry = tk.Entry(root)

install_button = tk.Button(root, text="서버 설치", command=start_server)

log_text = Text(root, height=10, width=50)

log_text.configure(state="disabled")

version_label.pack()
version_entry.pack()

folder_label.pack()
folder_entry.pack()

ram_label.pack()
ram_entry.pack()

install_button.pack()
log_text.pack()
root.mainloop()
