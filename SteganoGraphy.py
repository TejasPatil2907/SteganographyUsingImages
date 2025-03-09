from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import re

root = Tk()
root.title("Image Steganography")
root.geometry("700x500+150+180")
root.resizable(False, False)
root.configure(bg="#2E2E2E")

def showimage():
    global filename
    filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                          title='Select Image File',
                                          filetypes=(("PNG file", "*.png"),
                                                     ("JPG File", "*.jpg"),
                                                     ("All Files", "*.*")))
    img = Image.open(filename)
    img = img.resize((250, 250), Image.Resampling.LANCZOS)
    img = ImageTk.PhotoImage(img)
    lbl.configure(image=img, width=250, height=250)
    lbl.image = img

def text_to_binary(message):
    return ''.join(format(ord(char), '08b') for char in message) + '1111111111111110'  # EOF Marker

def binary_to_text(binary_message):
    chars = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    message = ''.join(chr(int(c, 2)) for c in chars if int(c, 2) != 65534)  # Stop at EOF marker
    return message

def hide(image_path, secret_message):
    img = Image.open(image_path)
    binary_message = text_to_binary(secret_message)

    if len(binary_message) > img.width * img.height * 3:
        raise ValueError("Message is too long to be hidden in the image.")

    data_index = 0
    pixels = img.load()
    
    for y in range(img.height):
        for x in range(img.width):
            pixel = list(pixels[x, y])
            for i in range(3):  # R, G, B
                if data_index < len(binary_message):
                    pixel[i] = pixel[i] & 254 | int(binary_message[data_index])
                    data_index += 1
            pixels[x, y] = tuple(pixel)
            if data_index >= len(binary_message):
                break
        if data_index >= len(binary_message):
            break

    output_path = "hidden.png"
    img.save(output_path)
    return output_path

def reveal(image_path):
    img = Image.open(image_path)
    binary_message = ''
    pixels = img.load()

    for y in range(img.height):
        for x in range(img.width):
            pixel = list(pixels[x, y])
            for i in range(3):  # R, G, B
                binary_message += str(pixel[i] & 1)

    if '1111111111111110' in binary_message:
        binary_message = binary_message[:binary_message.index('1111111111111110')]  # Remove EOF marker
    
    return binary_to_text(binary_message)

def Hide():
    global filename
    message = text1.get(1.0, END).strip()
    if not filename:
        text1.insert(END, "\nPlease select an image first!\n")
        return
    output_path = hide(filename, message)
    text1.insert(END, "\nImage hidden successfully! Saved as: " + output_path + "\n")

def Show():
    global filename
    if not filename:
        text1.insert(END, "\nPlease select an image first!\n")
        return
    clear_message = reveal(filename)
    text1.insert(END, "Hidden message: " + clear_message + "\n")

image_icon = PhotoImage(file="logo.jpg")
root.iconphoto(False, image_icon)
logo = PhotoImage(file="logo.png")
Label(root, image=logo, bg="#2E2E2E").place(x=10, y=0)
Label(root, text="Image Steganography", bg="#2E2E2E", fg="white", font="arial 25 bold").place(x=100, y=20)

f = Frame(root, bd=3, bg="black", width=340, height=280, relief=GROOVE)
f.place(x=10, y=80)
lbl = Label(f, bg="black")
lbl.place(x=40, y=10)

frame2 = Frame(root, bd=3, bg="white", width=340, height=280, relief=GROOVE)
frame2.place(x=350, y=80)
text1 = Text(frame2, font="Roboto 15", bg="grey", fg="black", relief=GROOVE, wrap=WORD)
text1.place(x=0, y=0, width=320, height=295)
scrollbar1 = Scrollbar(frame2)
scrollbar1.place(x=320, y=0, height=300)
scrollbar1.configure(command=text1.yview)
text1.configure(yscrollcommand=scrollbar1.set)

frame3 = Frame(root, bd=3, bg="#2E2E2E", width=330, height=100, relief=GROOVE)
frame3.place(x=10, y=370)
Button(frame3, text="Open Image", width=18, height=2, font="arial 14 bold", command=showimage).place(x=50, y=30)
Label(frame3, text="Picture, Image, Photo, File", bg="#2E2E2E", fg="#5F9EA0").place(x=48, y=5)

frame4 = Frame(root, bd=3, bg="#2E2E2E", width=330, height=100, relief=GROOVE)
frame4.place(x=360, y=370)
Button(frame4, text="Hide Data", width=10, height=2, font="arial 14 bold", command=Hide).place(x=20, y=30)
Button(frame4, text="Show Data", width=10, height=2, font="arial 14 bold", command=Show).place(x=180, y=30)
Label(frame4, text="Picture, Image, Photo, File", bg="#2E2E2E", fg="#5F9EA0").place(x=20, y=5)

root.mainloop()
