import tkinter as tk


# ==========================================================
# SETTINGS
# ==========================================================

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600

COUNTDOWN_TIME = 5


# ==========================================================
# MAIN WINDOW
# ==========================================================

window = tk.Tk()

window.title("The Last Chance Writer")
window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")

window.configure(bg="#11121a")


# ==========================================================
# VARIABLES
# ==========================================================

# Stores the number of seconds remaining
time_left = COUNTDOWN_TIME

# Keeps track of whether the user has started writing
writing_started = False

# Stores the timer created by Tkinter
timer_id = None


# ==========================================================
# TIMER
# ==========================================================

def start_timer():
    """
    Starts or restarts the countdown.
    """

    global timer_id

    # Cancel the previous timer if one exists
    if timer_id is not None:
        window.after_cancel(timer_id)

    # Start counting down
    countdown()


def countdown():
    """
    Counts down one second at a time.
    """

    global time_left
    global timer_id

    # Update the timer shown on screen
    timer_label.config(text=f"{time_left:.1f}")

    # If the timer has reached zero...
    if time_left <= 0:

        # Delete everything the user wrote
        text_area.delete("1.0", tk.END)

        # Reset the timer
        time_left = COUNTDOWN_TIME

        # Reset the interface
        timer_label.config(text=f"{COUNTDOWN_TIME:.1f}")

        status_label.config(
            text="Everything was erased. Start again."
        )

        # Stop the countdown
        timer_id = None

        return

    # Reduce the timer
    time_left -= 0.1

    # Run this function again after 100 milliseconds
    timer_id = window.after(100, countdown)


# ==========================================================
# WHEN USER TYPES
# ==========================================================

def user_is_typing(event=None):
    """
    Runs whenever the user types something.
    """

    global time_left
    global writing_started

    # The user has now started writing
    writing_started = True

    # Reset the timer
    time_left = COUNTDOWN_TIME

    # Update the status
    status_label.config(
        text="Keep writing..."
    )

    # Start/restart the countdown
    start_timer()

    # Update word and character count
    update_stats()


# ==========================================================
# WORD / CHARACTER COUNTER
# ==========================================================

def update_stats():
    """
    Updates the number of words and characters.
    """

    # Get everything currently written
    content = text_area.get("1.0", tk.END).strip()

    # Count characters
    character_count = len(content)

    # Count words
    if content:
        word_count = len(content.split())
    else:
        word_count = 0

    # Update labels
    stats_label.config(
        text=f"{word_count} words  •  {character_count} characters"
    )


# ==========================================================
# NEW SESSION
# ==========================================================

def new_session():
    """
    Clears the text and starts a fresh writing session.
    """

    global time_left
    global writing_started
    global timer_id

    # Cancel existing timer
    if timer_id is not None:
        window.after_cancel(timer_id)

    # Clear the writing area
    text_area.delete("1.0", tk.END)

    # Reset variables
    time_left = COUNTDOWN_TIME
    writing_started = False
    timer_id = None

    # Reset labels
    timer_label.config(
        text=f"{COUNTDOWN_TIME:.1f}"
    )

    status_label.config(
        text="Start writing..."
    )

    stats_label.config(
        text="0 words  •  0 characters"
    )

    # Put cursor back into text box
    text_area.focus_set()


# ==========================================================
# HEADER
# ==========================================================

title_label = tk.Label(
    window,
    text="THE LAST CHANCE WRITER",
    font=("Helvetica", 14, "bold"),
    bg="#11121a",
    fg="#a78bfa"
)

title_label.pack(pady=(35, 5))


subtitle_label = tk.Label(
    window,
    text="Don't stop. Don't think. Just write.",
    font=("Helvetica", 11),
    bg="#11121a",
    fg="#777887"
)

subtitle_label.pack()


# ==========================================================
# TIMER DISPLAY
# ==========================================================

timer_label = tk.Label(
    window,
    text="5.0",
    font=("Helvetica", 42, "bold"),
    bg="#11121a",
    fg="#f4f1ea"
)

timer_label.pack(pady=(25, 5))


status_label = tk.Label(
    window,
    text="Start writing...",
    font=("Helvetica", 10),
    bg="#11121a",
    fg="#777887"
)

status_label.pack()


# ==========================================================
# WRITING AREA
# ==========================================================

text_area = tk.Text(
    window,
    wrap="word",
    font=("Helvetica", 15),
    bg="#191a24",
    fg="#f4f1ea",
    insertbackground="#a78bfa",
    relief="flat",
    padx=20,
    pady=20
)

text_area.pack(
    fill="both",
    expand=True,
    padx=60,
    pady=25
)


# ==========================================================
# STATISTICS
# ==========================================================

stats_label = tk.Label(
    window,
    text="0 words  •  0 characters",
    font=("Helvetica", 9),
    bg="#11121a",
    fg="#666775"
)

stats_label.pack()


# ==========================================================
# NEW SESSION BUTTON
# ==========================================================

new_button = tk.Button(
    window,
    text="NEW SESSION",
    command=new_session,
    font=("Helvetica", 10, "bold"),
    bg="#a78bfa",
    fg="#11121a",
    activebackground="#c4b5fd",
    relief="flat",
    padx=20,
    pady=10,
    cursor="hand2"
)

new_button.pack(pady=20)


# ==========================================================
# KEYBOARD EVENT
# ==========================================================

# Whenever the user presses a key inside the text box,
# user_is_typing() will run.
text_area.bind("<Key>", user_is_typing)


# Put the cursor inside the writing area when the app opens
text_area.focus_set()


# ==========================================================
# START THE APPLICATION
# ==========================================================

window.mainloop()