from tkinter import *
from tkinter import messagebox, filedialog
from pathlib import Path
import chardet
from chardet.universaldetector import UniversalDetector
import pickle
from PIL import Image, ImageTk
from PIL.Image import Resampling
import base64

HasOpen = False
images = []
image_refs = []  # To keep references to images to prevent garbage collection


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
    global HasOpen, images, image_refs, current_file_path
    file_path = filedialog.askopenfilename(title='Выбор файла',
                                           filetypes=(('Все файлы', '*.*'), ('Текстовые документы (*.txt)', '*.txt'),
                                                      ('Специализированные файлы (*.klc)', '*.klc')))
    HasOpen = True
    current_file_path = file_path
    filename = Path(file_path).stem
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
            encoding = detector.result['encoding']
            if encoding is None:
                encoding = 'utf-8'  # Default to utf-8 if encoding is not detected
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    text = file.read()
            except (UnicodeDecodeError, LookupError):
                messagebox.showerror("Error", "Unable to decode file with detected encoding.")
                return

            text_field.delete('1.0', END)
            text_field.insert('1.0', text)
        else:
            try:
                with open(file_path, 'rb') as file:
                    data = pickle.load(file)
                text_field.delete('1.0', END)
                text_field.insert('1.0', data['text'])
                images = data['images']
                for img_info in images:
                    insert_image(img_info['path'], img_info['index'], from_load=True)
            except (pickle.UnpicklingError, EOFError, KeyError):
                messagebox.showerror("Error", "Unable to open .klc file.")
                return

    window.title(f"{filename} - Notes")


def save():
    global current_file_path
    if HasOpen and current_file_path:
        text = text_field.get("1.0", END)
        data = {'text': text, 'images': images}
        with open(current_file_path, 'wb') as file:
            pickle.dump(data, file)
        window.title(f"{Path(current_file_path).stem} - Notes")
    else:
        save_as()


def save_as():
    global current_file_path
    save_path = filedialog.asksaveasfilename(defaultextension=".klc",
                                             filetypes=(("KLC files", "*.klc"), ("All files", "*.*")))
    if save_path:
        text = text_field.get("1.0", END)
        data = {'text': text, 'images': images}
        with open(save_path, 'wb') as file:
            pickle.dump(data, file)
        current_file_path = save_path
        window.title(f"{Path(save_path).stem} - Notes")


def insert_image(path=None, index=None, from_load=False):
    global images, image_refs

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
        image_refs.append(img)  # Keep a reference to avoid garbage collection


def save_shortcut(event=None):
    save()


# Base64 encoded icon
icon_base64 = """
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
"""

# Decode Base64 to binary data
icon_data = base64.b64decode(icon_base64)

# Create a temporary icon file
icon_path = "icon.ico"
with open(icon_path, "wb") as icon_file:
    icon_file.write(icon_data)

window = Tk()
window.title("Notes")
window.geometry('600x700')
window.iconbitmap(icon_path)

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
file_menu.add_command(label='Insert Image', command=insert_image)
file_menu.add_command(label='Save', command=save)
file_menu.add_command(label='Save As...', command=save_as)
file_menu.add_command(label='Close', command=exits)
main_menu.add_cascade(label='File', menu=file_menu)
view_menu = Menu(main_menu, tearoff=0)

main_menu.add_cascade(label='View', menu=view_menu)
theme = Menu(view_menu, tearoff=0)
theme.add_command(label='Dark', command=Dark)
theme.add_command(label='Light', command=Light)
view_menu.add_cascade(label='Themes', menu=theme)
window.config(menu=main_menu)

window.bind('<Control-s>', save_shortcut)

window.mainloop()

# Clean up temporary icon file
import os
os.remove(icon_path)
