
#
# The program calculates:
#   1. Words Per Minute (WPM)
#   2. Accuracy
#   3. Number of characters typed
#   4. Number of correct characters

# 1. IMPORTS

# tkinter is Python's built-in library for creating GUI
# (Graphical User Interface) applications.
import tkinter as tk

# ttk contains improved versions of many Tkinter widgets,
# such as buttons and labels.
from tkinter import ttk

# random allows us to randomly select one of our sample texts.
import random


# # 2. CONSTANTS

# The total amount of time the user gets for one test.
TEST_DURATION = 60


# These are the texts that the user can be asked to type.
#
# Having multiple texts makes the program more interesting
# because the same text is not shown every time.

TEXT_SAMPLES = [
    (
        "Technology changes quickly, but learning never goes "
        "out of style. Every new skill begins with curiosity "
        "and improves through consistent practice."
    ),

    (
        "The best way to learn programming is to build things. "
        "Small projects teach you how different concepts work "
        "together and help you become a better problem solver."
    ),

    (
        "Speed is useful, but accuracy is even more important. "
        "A good typist learns to balance both while staying "
        "focused on the words appearing on the screen."
    ),

    (
        "Programming gives us a way to turn ideas into reality. "
        "With patience and practice, even a complicated problem "
        "can be broken into smaller and simpler pieces."
    ),

    (
        "Creativity and technology can work together to create "
        "interesting solutions. The most exciting projects often "
        "begin with a simple question and a willingness to explore."
    )
]

# 3. MAIN APPLICATION CLASS

class TypingSpeedTest:
    """
    This class contains the entire typing test application.

    Keeping the program inside a class helps us organize
    related variables and functions together.
    """

    def __init__(self, root):
        """
        This method runs automatically when we create an
        object of the TypingSpeedTest class.

        'root' is the main Tkinter window.
        """

        # Store the main window in self.root so that we can
        # access it from other methods in the class.
        self.root = root

        # Set the title shown at the top of the window.
        self.root.title("FocusType - Typing Speed Test")

        # Set the size of the application window.
        self.root.geometry("850x650")

        # Prevent the window from becoming extremely small.
        self.root.minsize(700, 550)

        # VARIABLES USED BY THE PROGRAM

        # This stores the sample text currently being tested.
        self.target_text = ""

        # This keeps track of whether the test is currently
        # running.
        self.test_running = False

        # This stores the number of seconds that have passed.
        self.elapsed_seconds = 0

        # This stores the ID returned by root.after().
        #
        # We need this ID later if we want to cancel the timer.
        self.timer_id = None

        # Number of characters the user has typed.
        self.characters_typed = 0

        # Number of characters typed correctly.
        self.correct_characters = 0

        # Number of correctly typed words.
        self.correct_words = 0

        # CREATE THE USER INTERFACE

        self.create_styles()
        self.create_header()
        self.create_text_area()
        self.create_typing_area()
        self.create_statistics()
        self.create_buttons()

        # Start the application in its initial state.
        self.reset_test()

    # 4. STYLING

    def create_styles(self):
        """
        Create the visual styles used by our ttk widgets.
        """

        # Create a style object.
        style = ttk.Style()

        # 'clam' gives us a consistent appearance across
        # different operating systems.
        try:
            style.theme_use("clam")
        except tk.TclError:
            # If the theme is not available, Tkinter will
            # simply continue using its default theme.
            pass

        # Style used for the main title.
        style.configure(
            "Title.TLabel",
            font=("Helvetica", 28, "bold")
        )

        # Style used for the smaller subtitle.
        style.configure(
            "Subtitle.TLabel",
            font=("Helvetica", 12)
        )

        # Style used for the statistics.
        style.configure(
            "Stats.TLabel",
            font=("Helvetica", 14, "bold")
        )

        # Style used for buttons.
        style.configure(
            "Main.TButton",
            font=("Helvetica", 12, "bold"),
            padding=10
        )

    # 5. HEADER

    def create_header(self):
        """
        Create the title and instructions at the top of
        the application.
        """

        # Frame is simply a container that helps us organize
        # widgets.
        header = ttk.Frame(self.root, padding=(30, 25))

        # Place the frame in the window.
        header.pack(fill="x")

        # Main title.
        title = ttk.Label(
            header,
            text="FocusType",
            style="Title.TLabel"
        )

        title.pack()

        # Short description below the title.
        subtitle = ttk.Label(
            header,
            text="Test your typing speed, accuracy and focus.",
            style="Subtitle.TLabel"
        )

        subtitle.pack(pady=(5, 0))

    # 6. SAMPLE TEXT AREA

    def create_text_area(self):
        """
        Create the area that displays the text the user
        needs to type.
        """

        # Create a frame around the sample text.
        text_frame = ttk.Frame(
            self.root,
            padding=(30, 5)
        )

        text_frame.pack(fill="x")

        # Label explaining what the user needs to do.
        instruction = ttk.Label(
            text_frame,
            text="Type the text below:",
            font=("Helvetica", 12, "bold")
        )

        instruction.pack(anchor="w", pady=(0, 8))

        # Text widget is useful when we want to display
        # multiple lines of text.
        self.sample_text_box = tk.Text(
            text_frame,
            height=6,
            wrap="word",
            font=("Helvetica", 15),
            padx=15,
            pady=15,
            relief="solid",
            borderwidth=1
        )

        self.sample_text_box.pack(fill="x")

        # The user should not be able to edit the sample text.
        self.sample_text_box.config(state="disabled")

        # TAGS
        # Tags allow us to change the appearance of particular
        # pieces of text inside a Tkinter Text widget.

        # Incorrect characters will be shown differently.
        self.sample_text_box.tag_configure(
            "error",
            underline=True
        )

    # 7. USER TYPING AREA

    def create_typing_area(self):
        """
        Create the Text widget where the user types.
        """

        typing_frame = ttk.Frame(
            self.root,
            padding=(30, 15, 30, 5)
        )

        typing_frame.pack(fill="both", expand=True)

        # Instruction above the typing box.
        instruction = ttk.Label(
            typing_frame,
            text="Your typing:",
            font=("Helvetica", 12, "bold")
        )

        instruction.pack(anchor="w", pady=(0, 8))

        # This is where the user actually types.
        self.typing_box = tk.Text(
            typing_frame,
            height=8,
            wrap="word",
            font=("Helvetica", 15),
            padx=15,
            pady=15,
            undo=True,
            relief="solid",
            borderwidth=1
        )

        self.typing_box.pack(fill="both", expand=True)

        # Whenever the user types or deletes something,
        # Tkinter generates the <<Modified>> event.
        #
        # We connect that event to our handle_typing method.
        # Run handle_typing() every time the user releases a key.
# This lets us update the WPM and accuracy while they type.
        self.typing_box.bind(
        "<KeyRelease>",
        self.handle_typing)

        # The user starts with the cursor inside the typing box.
        self.typing_box.focus_set()

    # 8. STATISTICS

    def create_statistics(self):
        """
        Create the section showing live statistics.
        """

        stats_frame = ttk.Frame(
            self.root,
            padding=(30, 15)
        )

        stats_frame.pack(fill="x")

        # We use StringVar objects because their displayed
        # values can be changed while the program is running.

        self.time_text = tk.StringVar(value="Time: 0s")

        self.wpm_text = tk.StringVar(value="WPM: 0")

        self.accuracy_text = tk.StringVar(
            value="Accuracy: 100%"
        )

        self.characters_text = tk.StringVar(
            value="Characters: 0"
        )


        # Create labels for each statistic.

        ttk.Label(
            stats_frame,
            textvariable=self.time_text,
            style="Stats.TLabel"
        ).pack(side="left", expand=True)

        ttk.Label(
            stats_frame,
            textvariable=self.wpm_text,
            style="Stats.TLabel"
        ).pack(side="left", expand=True)

        ttk.Label(
            stats_frame,
            textvariable=self.accuracy_text,
            style="Stats.TLabel"
        ).pack(side="left", expand=True)

        ttk.Label(
            stats_frame,
            textvariable=self.characters_text,
            style="Stats.TLabel"
        ).pack(side="left", expand=True)

    # 9. BUTTONS
    def create_buttons(self):
        """
        Create the result message and the Restart/Finish buttons.
        """

        # --------------------------------------------------------
        # RESULT MESSAGE
        # --------------------------------------------------------

        # This label will display the final result after the test.
        self.result_label = ttk.Label(
            self.root,
            text="Start typing to begin the test!",
            font=("Helvetica", 13, "bold"),
            anchor="center",
            justify="center"
        )

        self.result_label.pack(
            fill="x",
            padx=30,
            pady=(0, 10)
        )


        # --------------------------------------------------------
        # BUTTON FRAME
        # --------------------------------------------------------

        button_frame = ttk.Frame(
            self.root,
            padding=(30, 5, 30, 25)
        )

        button_frame.pack(fill="x")


        # --------------------------------------------------------
        # RESTART BUTTON
        # --------------------------------------------------------

        restart_button = ttk.Button(
            button_frame,
            text="Restart",
            style="Main.TButton",
            command=self.reset_test
        )

        restart_button.pack(
            side="left",
        expand=True,
        padx=(0, 10)
    )


        # --------------------------------------------------------
        # FINISH BUTTON
        # --------------------------------------------------------

        finish_button = ttk.Button(
            button_frame,
            text="Finish Test",
            style="Main.TButton",
            command=self.finish_test
        )

        finish_button.pack(
        side="right",
        expand=True,
        padx=(10, 0))

    # 10. RESET THE TEST
    def reset_test(self):
        """
        Reset everything and prepare a new typing test.
        """

        # If an old timer is still running, cancel it.
        if self.timer_id is not None:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

        # Choose a random sample from our list.
        self.target_text = random.choice(TEXT_SAMPLES)

        # Reset all values.
        self.test_running = False
        self.elapsed_seconds = 0
        self.characters_typed = 0
        self.correct_characters = 0
        self.correct_words = 0

        # Update the sample text shown to the user.
        self.sample_text_box.config(state="normal")

        # Delete everything currently inside the widget.
        self.sample_text_box.delete("1.0", "end")

        # Insert our new sample text.
        self.sample_text_box.insert(
            "1.0",
            self.target_text
        )

        # Make the sample text read-only again.
        self.sample_text_box.config(state="disabled")

        # Clear the user's previous typing.
        self.typing_box.delete("1.0", "end")

        # Reset the modified flag.
        #
        # Without this, Tkinter could immediately trigger
        # our typing event after we clear the box.
        self.typing_box.edit_modified(False)

        # Update the statistics displayed on screen.
        self.update_statistics()

        # Put the cursor back in the typing box.
        self.typing_box.focus_set()

 # 11. DETECT USER TYPING

    def handle_typing(self, event=None):
        """
        This method is called whenever the user changes
        something in the typing box.
        """

        # Get rid of the modified flag first.
        #
        # Tkinter keeps track of whether the Text widget has
        # changed. We reset it so the next change can trigger
        # the event again

        # If the test is already finished, don't process
        # any more typing.
        if not self.test_running and self.elapsed_seconds >= TEST_DURATION:
            return

        # Get everything the user has typed.
        typed_text = self.typing_box.get(
            "1.0",
            "end-1c"
        )

        # Start the timer when the user types their first
        # character.
        if len(typed_text) > 0 and not self.test_running:

            self.test_running = True

            # Start our timer.
            self.run_timer()

        # Calculate the current score.
        self.calculate_score(typed_text)

        # Update the visual statistics.
        self.update_statistics()

        # Highlight incorrect characters.
        self.highlight_errors(typed_text)

        # If the user has typed the entire sample correctly,
        # we can automatically finish the test.
        if typed_text == self.target_text:
            self.finish_test()

   # 12. TIMER
    
    def run_timer(self):
        """
        Increase the elapsed time once every second.

        Tkinter's after() method lets us schedule a function
        to run later without freezing the GUI.
        """

        # If the test isn't running, don't continue.
        if not self.test_running:
            return

        # Increase the elapsed time by one second.
        self.elapsed_seconds += 1

        # Update the timer shown to the user.
        self.time_text.set(
            f"Time: {self.elapsed_seconds}s"
        )

        # Check whether the user has reached the time limit.
        if self.elapsed_seconds >= TEST_DURATION:

            # The test is finished.
            self.finish_test()

            return

        # Schedule this same method to run again after
        # 1000 milliseconds (1 second).
        #
        # We save the returned ID so that we can cancel it
        # later if necessary.
        self.timer_id = self.root.after(
            1000,
            self.run_timer
        )

    # 13. CALCULATE SCORE

    def calculate_score(self, typed_text):
        """
        Compare what the user typed with the target text.

        We calculate:
            - characters typed
            - correct characters
            - accuracy
            - WPM
        """

        # Number of characters typed by the user.
        self.characters_typed = len(typed_text)

        # We compare the user's text character by character.

        correct = 0

        for index, character in enumerate(typed_text):

            # If the user hasn't typed beyond the sample text
            # and the character matches, it is correct.
            if (
                index < len(self.target_text)
                and character == self.target_text[index]
            ):
                correct += 1

        # Store the number of correct characters.
        self.correct_characters = correct

        # Calculate the number of correctly typed words.
        #
        # The standard typing-test assumption is that
        # 5 characters = 1 word.
        self.correct_words = correct / 5

  # 14. CALCULATE WPM

    def calculate_wpm(self):
        """
        Calculate Words Per Minute.

        WPM is commonly calculated using:
        
            characters typed / 5
            -------------------
              time in minutes
        """

        # If no time has passed, we can't calculate WPM.
        if self.elapsed_seconds == 0:
            return 0

        # Convert seconds into minutes.
        minutes = self.elapsed_seconds / 60

        # Calculate words using the standard 5-character
        # definition.
        words = self.correct_characters / 5

        # Calculate words per minute.
        wpm = words / minutes

        # Round to the nearest whole number.
        return round(wpm)


    
    # 15. CALCULATE ACCURACY
    
    def calculate_accuracy(self):
        """
        Calculate typing accuracy as a percentage.
        """

        # If the user hasn't typed anything yet, accuracy
        # is considered 100%.
        if self.characters_typed == 0:
            return 100

        # Accuracy formula:
        #
        # correct characters
        # ------------------ × 100
        # total characters
        #
        accuracy = (
            self.correct_characters
            / self.characters_typed
        ) * 100

        return round(accuracy)


    
    # 16. UPDATE STATISTICS
    
    def update_statistics(self):
        """
        Update all the numbers displayed in the GUI.
        """

        # Calculate the latest WPM.
        wpm = self.calculate_wpm()

        # Calculate the latest accuracy.
        accuracy = self.calculate_accuracy()

        # Update the labels.
        self.wpm_text.set(
            f"WPM: {wpm}"
        )

        self.accuracy_text.set(
            f"Accuracy: {accuracy}%"
        )

        self.characters_text.set(
            f"Characters: {self.characters_typed}"
        )

        self.time_text.set(
            f"Time: {self.elapsed_seconds}s"
        )

    # 17. HIGHLIGHT ERRORS

    def highlight_errors(self, typed_text):
        """
        Highlight characters in the sample text where the
        user's typing does not match.

        This gives the user immediate visual feedback.
        """

        # First remove all existing error highlights.
        self.sample_text_box.tag_remove(
            "error",
            "1.0",
            "end"
        )

        # Check each character typed by the user.
        for index, character in enumerate(typed_text):

            # If the user has typed beyond the target text,
            # there is nothing more to compare.
            if index >= len(self.target_text):
                break

            # Compare the typed character with the target.
            if character != self.target_text[index]:

                # Tkinter text indexes look like:
                #
                # "line.character"
                #
                # Since our sample is treated as one line,
                # we can use:
                #
                # 1.index

                start = f"1.{index}"

                # Add 1 to the character index to find the
                # end of the highlighted character.
                end = f"1.{index + 1}"

                self.sample_text_box.tag_add(
                    "error",
                    start,
                    end
                )

    # 18. FINISH TEST

    def finish_test(self):
        """
        Stop the test and show the final result.
        """

        # If the test has already finished, do nothing.
        if (
            not self.test_running
            and self.elapsed_seconds == 0
        ):
            return

        # Stop the timer.
        self.test_running = False

        # Cancel any scheduled timer callback.
        if self.timer_id is not None:

            try:
                self.root.after_cancel(
                    self.timer_id
                )
            except tk.TclError:
                pass

            self.timer_id = None

        # Get the user's final text.
        typed_text = self.typing_box.get(
            "1.0",
            "end-1c"
        )

        # Recalculate the final score.
        self.calculate_score(typed_text)

        # Update the statistics one last time.
        self.update_statistics()

        # Disable the typing box so the user can't change
        # the result after finishing.
        self.typing_box.config(
            state="disabled"
        )

        # Show the final result.
        self.show_result()

    # 19. SHOW FINAL RESULT

    def show_result(self):
        """
        Display a final message inside the application.
        """

        # Calculate final statistics.
        wpm = self.calculate_wpm()
        accuracy = self.calculate_accuracy()

        # Create a result message based on performance.
        if wpm >= 80:
            message = "Excellent! Your typing speed is impressive."

        elif wpm >= 60:
            message = "Great job! You have a strong typing speed."

        elif wpm >= 40:
            message = "Good work! Keep practising to get faster."

        else:
            message = "Nice start! Accuracy and practice will improve your speed."

        # Add the result information to the bottom of the
        # window.
        self.result_label.config(
            text=(
                f"Test Complete!\n"
                f"{wpm} WPM  •  {accuracy}% Accuracy\n"
                f"{message}"
            )
        )


    
    # 20. RUN APPLICATION

# CREATE THE MAIN TKINTER WINDOw
# Tk() creates the main application window.
root = tk.Tk()

# CREATE OUR APPLICATION

# Create an instance of our TypingSpeedTest class.
app = TypingSpeedTest(root)

# START THE TKINTER EVENT LOOP

# Tkinter applications work using an event loop.
#
# mainloop() continuously waits for events such as:
#   - mouse clicks
#   - keyboard presses
#   - timer events
#   - window resizing
#
# Without mainloop(), the window would appear and immediately
# close.
root.mainloop()