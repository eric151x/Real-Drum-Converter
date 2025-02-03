from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import tempfile
import os
import zipfile
import shutil
from pydub import AudioSegment

ffmpeg_path = os.path.join(os.path.dirname(__file__), "ffmpeg", "ffmpeg.exe")

os.environ["FFMPEG_BINARY"] = ffmpeg_path

temp_local = tempfile.gettempdir()
mp3s = ""
wavs = ""

def arquivo():
    global mp3s, wavs
    file = filedialog.askopenfilename(filetypes=[("Real Drum File", "*.realdrum")])
    if file:
        escolher.config(text="desselecionar", command=desselecionar)
        fazer.config(state=(NORMAL))

        with zipfile.ZipFile(file, 'r') as file:
            file.extractall(path=temp_local)

        coisas = os.listdir(f"{temp_local}/realdrumkit")
        arquivos = [os.path.splitext(files)[0] for files in coisas if files.endswith(".mp3")]
        wavs = arquivos
        mp3s = [
        os.path.join(f"{temp_local}/realdrumkit", files)
        for files in coisas if files.endswith(".mp3")
        ]

        for coisas in arquivos:
            lista.insert(0, coisas)

def desselecionar():
    escolher.config(text="Escolher o arquivo", command=arquivo)
    lista.delete(0, lista.size() - 1)
    shutil.rmtree(f"{temp_local}/realdrumkit")
    fazer.config(state=DISABLED)

def lugar():
    local = filedialog.askdirectory()
    if local:
        caminho.delete(0,END)
        caminho.insert(0, local)

def converter():
    if caminho.get():
        for seila in mp3s:
            audio = AudioSegment.from_file(seila, "mp3")
        for seila2 in wavs:
            audio.export(f"{caminho.get()}/{seila2}.wav", format="wav")

        escolher.config(text="Escolhe o arquivo", command=arquivo)
        lista.delete(0, lista.size() - 1)
        shutil.rmtree(f"{temp_local}/realdrumkit")
        fazer.config(state=DISABLED)

        messagebox.showinfo("Sucesso!", "conversão feita com sucesso!")

    else:
        messagebox.showwarning("Atenção!", "Nenhum local de salvamento.")

janela = Tk()
janela.title("Real Drum Converter")
janela.geometry("325x265")
janela.iconbitmap("ico.ico")

escolher = ttk.Button(janela, text="Escolher o arquivo", command=arquivo)
escolher.grid(column=0, row=0)

texto = Label(janela, text="Local de salvamento:")
texto.grid(column=0, row=1)

caminho = ttk.Entry(janela)
caminho.grid(column=1, row=1)

botao_caminho = ttk.Button(janela, text="...", command=lugar)
botao_caminho.grid(column=2, row=1)

lista = Listbox(janela, width=50)
lista.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

janela.grid_columnconfigure(0, weight=1)
janela.grid_columnconfigure(1, weight=1)
janela.grid_columnconfigure(2, weight=1)

fazer = ttk.Button(janela, text="Converter", command=converter, state=DISABLED)
fazer.grid(column=2, row=3)

def fechar():
    if os.path.exists(f"{temp_local}/realdrumkit") and os.path.isdir(f"{temp_local}/realdrumkit"):
        shutil.rmtree(f"{temp_local}/realdrumkit")
    janela.destroy()

janela.protocol("WM_DELETE_WINDOW", fechar)

janela.mainloop()