from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os


# -----------------------------
# WINDOW SETUP
# -----------------------------

window = Tk()
window.title("Watermark Studio")
window.geometry("800x700")
window.config(padx=30, pady=25)


# -----------------------------
# GLOBAL VARIABLES
# -----------------------------

original_image = None
edited_image = None
display_image = None


# -----------------------------
# LOAD FONT
# -----------------------------

def get_font(size):
    """
    Returns a font that comes bundled with Pillow.
    This avoids depending on a font installed on the computer.
    """

    font_folder = os.path.join(
        os.path.dirname(ImageFont.__file__),
        "fonts"
    )

    font_path = os.path.join(font_folder, "DejaVuSans.ttf")

    return ImageFont.truetype(font_path, size)


# -----------------------------
# DISPLAY IMAGE
# -----------------------------

def show_image(image):
    """
    Resizes an image for the Tkinter preview
    while keeping its original proportions.
    """

    global display_image

    preview = image.copy()

    preview.thumbnail((700, 480))

    display_image = ImageTk.PhotoImage(preview)

    image_display.config(image=display_image)
    image_display.image = display_image


# -----------------------------
# CHOOSE IMAGE
# -----------------------------

def choose_image():

    global original_image
    global edited_image

    file_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[
            ("Image Files", "*.jpg *.jpeg *.png *.webp"),
            ("All Files", "*.*")
        ]
    )

    if not file_path:
        return

    try:
        original_image = Image.open(file_path).convert("RGBA")

        edited_image = original_image.copy()

        show_image(edited_image)

        status_label.config(
            text=f"Loaded: {os.path.basename(file_path)}"
        )

    except Exception:
        messagebox.showerror(
            "Error",
            "The selected file could not be opened as an image."
        )


# -----------------------------
# ADD WATERMARK
# -----------------------------

def add_watermark():

    global edited_image

    if original_image is None:
        messagebox.showwarning(
            "No Image",
            "Please choose an image first."
        )
        return

    watermark_text = watermark_entry.get().strip()

    if not watermark_text:
        messagebox.showwarning(
            "No Watermark",
            "Please enter some watermark text."
        )
        return

    try:
        font_size = int(size_entry.get())

        if font_size <= 0:
            raise ValueError

    except ValueError:
        messagebox.showwarning(
            "Invalid Font Size",
            "Please enter a positive number for the font size."
        )
        return

    # Start from the original image
    edited_image = original_image.copy()

    draw = ImageDraw.Draw(edited_image)

    font = get_font(font_size)

    # Find the size of the watermark text
    text_box = draw.textbbox(
        (0, 0),
        watermark_text,
        font=font
    )

    text_width = text_box[2] - text_box[0]
    text_height = text_box[3] - text_box[1]

    # Padding from the edges of the image
    padding = 40

    # Bottom-right position
    x = edited_image.width - text_width - padding
    y = edited_image.height - text_height - padding

    # Draw a subtle background behind the watermark
    background_padding = 15

    draw.rounded_rectangle(
        (
            x - background_padding,
            y - background_padding,
            x + text_width + background_padding,
            y + text_height + background_padding
        ),
        radius=12,
        fill=(0, 0, 0, 100)
    )

    # Draw the watermark
    draw.text(
        (x, y),
        watermark_text,
        font=font,
        fill=(255, 255, 255, 180)
    )

    show_image(edited_image)

    status_label.config(
        text="Watermark added successfully!"
    )


# -----------------------------
# RESET IMAGE
# -----------------------------

def reset_image():

    global edited_image

    if original_image is None:
        return

    edited_image = original_image.copy()

    show_image(edited_image)

    status_label.config(
        text="Image reset."
    )


# -----------------------------
# SAVE IMAGE
# -----------------------------

def save_image():

    if edited_image is None:
        messagebox.showwarning(
            "Nothing to Save",
            "Please choose an image first."
        )
        return

    save_path = filedialog.asksaveasfilename(
        title="Save Watermarked Image",
        defaultextension=".png",
        filetypes=[
            ("PNG Image", "*.png"),
            ("JPEG Image", "*.jpg"),
            ("All Files", "*.*")
        ]
    )

    if not save_path:
        return

    try:

        # JPEG does not support transparency,
        # so convert the image before saving.
        if save_path.lower().endswith((".jpg", ".jpeg")):
            edited_image.convert("RGB").save(save_path)
        else:
            edited_image.save(save_path)

        status_label.config(
            text=f"Saved: {os.path.basename(save_path)}"
        )

        messagebox.showinfo(
            "Saved",
            "Your watermarked image has been saved!"
        )

    except Exception:
        messagebox.showerror(
            "Save Error",
            "The image could not be saved."
        )


# ============================================================
# GUI
# ============================================================


# -----------------------------
# TITLE
# -----------------------------

title_label = Label(
    window,
    text="WATERMARK STUDIO",
    font=("Arial", 24, "bold")
)

title_label.pack(pady=(0, 5))


subtitle_label = Label(
    window,
    text="Protect your images with a custom watermark",
    font=("Arial", 11)
)

subtitle_label.pack(pady=(0, 20))


# -----------------------------
# IMAGE PREVIEW
# -----------------------------

image_display = Label(
    window,
    text="No image selected\n\nChoose an image to get started",
    width=70,
    height=20,
    relief="groove"
)

image_display.pack(pady=10)


# -----------------------------
# CHOOSE IMAGE BUTTON
# -----------------------------

choose_button = Button(
    window,
    text="Choose Image",
    command=choose_image,
    width=20
)

choose_button.pack(pady=10)


# -----------------------------
# WATERMARK TEXT
# -----------------------------

watermark_label = Label(
    window,
    text="Watermark Text"
)

watermark_label.pack(pady=(10, 3))


watermark_entry = Entry(
    window,
    width=40
)

watermark_entry.insert(0, "@mywebsite")

watermark_entry.pack()


# -----------------------------
# FONT SIZE
# -----------------------------

size_label = Label(
    window,
    text="Font Size"
)

size_label.pack(pady=(10, 3))


size_entry = Entry(
    window,
    width=10
)

size_entry.insert(0, "40")

size_entry.pack()


# -----------------------------
# ACTION BUTTONS
# -----------------------------

button_frame = Frame(window)

button_frame.pack(pady=20)


watermark_button = Button(
    button_frame,
    text="Add Watermark",
    command=add_watermark,
    width=18
)

watermark_button.grid(row=0, column=0, padx=5)


reset_button = Button(
    button_frame,
    text="Reset",
    command=reset_image,
    width=12
)

reset_button.grid(row=0, column=1, padx=5)


save_button = Button(
    button_frame,
    text="Save Image",
    command=save_image,
    width=15
)

save_button.grid(row=0, column=2, padx=5)


# -----------------------------
# STATUS
# -----------------------------

status_label = Label(
    window,
    text="Ready",
    font=("Arial", 10)
)

status_label.pack(pady=5)


# -----------------------------
# START APPLICATION
# -----------------------------

window.mainloop()