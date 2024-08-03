from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from pathlib import Path
HasOpen = False
#Change Thema
def Dark():
    Theme = {'bg':'black', 'fg': 'white', }
    text_fild.configure(bg = Theme['bg'], fg = Theme['fg'])

def Light():
    Theme = {'bg': 'white', 'fg': 'black', }
    text_fild.configure(bg=Theme['bg'], fg=Theme['fg'])
#Функция для выхода
def exits():
    answer = messagebox.askyesno('Подтверждение выхода', 'Вы уверены что хотите выйти?')
    if answer:
        window.destroy()
#Открытие файла
def open_file():
    file_path = filedialog.askopenfilename(title='Выбор файла',
                                           filetypes=(('Текстовые документы (*.txt)', '*.txt'), ('Все файлы', '*.*'), ('Специализированные файлы (*.klc)', ('*.klc'))))
    global HasOpen
    HasOpen = True
    filename = (Path(file_path).stem)
    suffix = Path(file_path).suffix
    if file_path:
        if suffix != '.klc':
            text_fild.delete('1.0', END)
            text_fild.insert('1.0', open(file_path,'r', encoding='UTF-8').read())
        else:
            text_fild.delete('1.0', END)
            text_fild.insert('1.0', open(file_path, 'r', encoding='UTF-8').read())

    window.title(f"{filename} - Notes")

def save():
    if HasOpen:
        save = filedialog.asksaveasfilename()
        if save != "":
            text = text_fild.get("1.0", END)
        f = open(f"{save}.klc", 'w', encoding= 'UTF-8')
        f.write(text)



window = Tk()
window.title("Notes")
window.geometry('600x700')

ftext = Frame(window)
ftext.pack(fill=BOTH, expand=1)
text_fild = Text(ftext,
            bg='white',
            fg='black',
            padx=10,
            pady=10,
            wrap=WORD,
            insertbackground='brown',
            selectbackground='#8D917A',
            spacing3=10,
            width=30,
            font='Arial 14'
            )
text_fild.pack(expand=1, fill=BOTH, side=LEFT)

scroll = Scrollbar(ftext, command=text_fild.yview)
scroll.pack(side=LEFT, fill=Y)
text_fild.config(yscrollcommand=scroll.set)

main_menu = Menu(window)
file_menu = Menu(main_menu, tearoff = 0)
file_menu.add_command(label = 'Open', command=open_file)
file_menu.add_command(label = 'Save', command = save)
file_menu.add_command(label = 'Close', command = exits)
main_menu.add_cascade(label='File', menu=file_menu)
view_menu =  Menu(main_menu, tearoff = 0)

main_menu.add_cascade(label='View', menu=view_menu)
theme = Menu(view_menu, tearoff = 0)
theme.add_command(label = 'Dark', command = Dark)
theme.add_command(label = 'Light', command = Light)
view_menu.add_cascade(label = 'Themes', menu = theme)
window.config(menu=main_menu)

window.mainloop()sss

