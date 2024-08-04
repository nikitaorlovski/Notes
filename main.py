from tkinter import *
from tkinter import messagebox, filedialog
from pathlib import Path
import chardet
from chardet.universaldetector import UniversalDetector
import pickle
from PIL import Image, ImageTk
from PIL.Image import Resampling

HasOpen = False
images = []


# Change Theme
def Dark():
    Theme = {'bg': 'gray', 'fg': 'white'}
    text_field.configure(bg=Theme['bg'], fg=Theme['fg'])


def Light():
    Theme = {'bg': 'white', 'fg': 'black'}
    text_field.configure(bg=Theme['bg'], fg=Theme['fg'])


# Function to exit
def exits():
    answer = messagebox.askyesno('Подтверждение выхода', 'Вы уверены что хотите выйти?')
    if answer:
        window.destroy()


# Open file
def open_file():
    global HasOpen, images
    file_path = filedialog.askopenfilename(title='Выбор файла',
                                           filetypes=(('Все файлы', '*.*'),('Текстовые документы (*.txt)', '*.txt'),
                                                      ('Специализированные файлы (*.klc)', '*.klc')))
    HasOpen = True
    filename = (Path(file_path).stem)
    suffix = Path(file_path).suffix
    if file_path:
        if suffix != '.klc':
            detector = UniversalDetector()
            with open(file_path, 'rb') as fh:
                for line in fh:
                    detector.feed(line)
                    if detector.done:
                        break
                detector.close()
            text_field.delete('1.0', END)
            text_field.insert('1.0', open(file_path, 'r', encoding=f"{detector.result['encoding']}").read())
        else:
            with open(file_path, 'rb') as file:
                data = pickle.load(file)
                text_field.delete('1.0', END)
                text_field.insert('1.0', data['text'])
                images = data['images']
                for img_info in images:
                    insert_image(img_info['path'], img_info['index'], from_load=True)

    window.title(f"{filename} - Notes")


def save():
    if HasOpen:
        save_path = filedialog.asksaveasfilename(defaultextension=".klc",
                                                 filetypes=(("KLC files", "*.klc"), ("All files", "*.*")))
        if save_path:
            text = text_field.get("1.0", END)
            data = {'text': text, 'images': images}
            with open(save_path, 'wb') as file:
                pickle.dump(data, file)


def insert_image(path=None, index=None, from_load=False):
    global images

    if not from_load:
        path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"), ("All files", "*.*")])
        index = text_field.index(INSERT)

    if path:
        img = Image.open(path)
        img = img.resize((200, 200), Resampling.LANCZOS)  # Resize image
        img = ImageTk.PhotoImage(img)
        if not from_load:
            images.append({'path': path, 'index': index})
        text_field.image_create(index, image=img)
        text_field.insert(index, '\n')
        text_field.image = img  # Keep a reference to avoid garbage collection


window = Tk()
window.title("Notes")
window.geometry('600x700')

ftext = Frame(window)
ftext.pack(fill=BOTH, expand=1)
text_field = Text(ftext,
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
text_field.pack(expand=1, fill=BOTH, side=LEFT)

scroll = Scrollbar(ftext, command=text_field.yview)
scroll.pack(side=LEFT, fill=Y)
text_field.config(yscrollcommand=scroll.set)

main_menu = Menu(window)
file_menu = Menu(main_menu, tearoff=0)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', command=save)
file_menu.add_command(label='Close', command=exits)
main_menu.add_cascade(label='File', menu=file_menu)
view_menu = Menu(main_menu, tearoff=0)

main_menu.add_cascade(label='View', menu=view_menu)
theme = Menu(view_menu, tearoff=0)
theme.add_command(label='Dark', command=Dark)
theme.add_command(label='Light', command=Light)
view_menu.add_cascade(label='Themes', menu=theme)
window.config(menu=main_menu)

# Add Insert Image button
insert_image_button = Button(window, text="Insert Image", command=insert_image)
insert_image_button.pack()

window.mainloop()
