import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.filedialog
from tkinter.colorchooser import askcolor
from PIL import Image, ImageTk, ImageDraw
from tkfontchooser import askfont
from tkinter.filedialog import asksaveasfile, asksaveasfilename


def image_uploader():
    file_types = [("Image Files", "*.png;*.jpg;*.jpeg")]
    path = tk.filedialog.askopenfilename(filetypes=file_types)

    if len(path):
        img = Image.open(path)
        img = img.resize((850, 478))
        pic = ImageTk.PhotoImage(img)

        image_to_watermark.config(width=f"{pic.width()}", height=f"{pic.height()}")
        image_to_watermark.image = pic
        image_to_watermark.create_image(425, 239, image=image_to_watermark.image)
        text_entry.focus()
    else:
        print("No file is Chosen || Please choose a file.")


def watermark_text():
    text = text_entry.get()
    image_to_watermark.itemconfig(watermark, text=text)
    image_to_watermark.tag_raise(watermark)
    text_entry.delete(0, END)


def change_color():
    text_color = askcolor(title="Choose color")
    image_to_watermark.itemconfig(watermark, fill=text_color[1])


def select_font():
    font = askfont(window)
    # font is "" if the user has cancelled
    if font:
        # spaces in the family name need to be escaped
        font['family'] = font['family'].replace(' ', '\ ')
        font_str = "%(family)s %(size)i %(weight)s %(slant)s" % font
        if font['underline']:
            font_str += ' underline'
        if font['overstrike']:
            font_str += ' overstrike'
        # label.configure(font=font_str, text='Chosen font: ' + font_str.replace('\ ', ' '))
        image_to_watermark.itemconfig(watermark, font=font_str)


def angle():
    def select():
        value = int(ang.get())
        image_to_watermark.itemconfig(watermark, angle=value)
        ang.delete(0, END)
        top.destroy()
    top = Toplevel(window)
    top.title("Enter an Angle")
    ang = Entry(top, width=10, font=("Arial", 12))
    ang.grid(row=0, pady=5, padx=5)
    Button(top, text='select', command=select).grid(row=1, pady=5, padx=5)


def opacity():
    # window.attributes('-alpha', 0.7)
    alpha = 0.5
    image_to_watermark.itemconfig(watermark, tags=("transparent_text",), alpha=alpha)


def dwnload():
    img = asksaveasfile(initialfile='watermarked_image.jpg', defaultextension=".jpg", filetypes=[("All Files", "*.*"), ("Image Files", "*.png;*.jpg;*.jpeg"), ("Text Documents", "*.txt")])


def save_as(canvas):
    file_path = asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])

    if file_path:
        # Create a PostScript file
        canvas.postscript(file=file_path + ".ps", colormode="color")

        # Use Pillow (PIL) to convert the PostScript file to an image (PNG)
        img = Image.open(file_path + ".ps")
        img.save(file_path, format="png", quality=99)
        img.close()


def download():
    save_as(image_to_watermark)


window = tk.Tk()
window.title("Image WaterMarker")

backGround = Canvas(window, height=300, width=600, bg="#BFD8AF")
backGround.grid()


window.option_add("*Button*Background", "#D4E7C5")
window.option_add("*Entry*Background", "#E1F0DA")

image_to_watermark = Canvas(backGround, width=600, height=300)
image_to_watermark.grid(row=0, pady=10, padx=10, columnspan=7)
watermark = image_to_watermark.create_text(425, 239, text="", fill="black", font=('Helvetica 15 bold'), anchor=CENTER, angle=45)


uploadButton = Button(backGround, text="Upload Image", command=image_uploader, width=11)
uploadButton.grid(column=0, row=1, padx=1)

textButton = Button(backGround, text="Text", command=watermark_text, width=8)
textButton.grid(column=1, row=1, padx=2)

colorButton = Button(backGround, text="Color", command=change_color, width=8)
colorButton.grid(column=2, row=1, padx=2)

fontButton = Button(backGround, text="Select Font", command=select_font, width=8)
fontButton.grid(column=3, row=1,padx=2)

angleButton = Button(backGround, text="Angle", command=angle, width=8)
angleButton.grid(column=4, row=1, padx=2)

opacityButton = Button(backGround, text="Opacity", command=opacity, width=8)
opacityButton.grid(column=5, row=1, padx=2)

downloadButton = Button(backGround, text="Download", command=download, width=8)
downloadButton.grid(column=6, row=1, padx=2)

text_entry = Entry(window, width=50, font=("Arial", 15))
text_entry.grid(row=2, pady=10, padx=20, columnspan=5)


window.mainloop()
