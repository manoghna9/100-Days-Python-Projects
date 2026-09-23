from flask import Flask, render_template, request
import requests


# ==========================================================
# FLASK SETUP
# ==========================================================

app = Flask(__name__)


# ==========================================================
# HOME PAGE
# ==========================================================

@app.route("/", methods=["GET", "POST"])
def home():

    word_data = None
    error = None

    # ------------------------------------------------------
    # Check if the user searched for a word
    # ------------------------------------------------------

    if request.method == "POST":

        word = request.form.get("word")

        # Remove unnecessary spaces
        word = word.strip()

        if word:

            # --------------------------------------------------
            # Ask the Dictionary API for information
            # --------------------------------------------------

            api_url = (
                f"https://api.dictionaryapi.dev/api/v2/"
                f"entries/en/{word}"
            )

            try:
                response = requests.get(api_url, timeout=10)

                if response.status_code == 200:
                    word_data = response.json()[0]
                else:
                    error = "The dictionary service is currently unavailable."

            except requests.exceptions.RequestException:
                error = "Could not connect to the dictionary service."

            # --------------------------------------------------
            # Check if the API found the word
            # --------------------------------------------------

            if response.status_code == 200:

                word_data = response.json()[0]

            else:

                error = (
                    "Sorry, we couldn't find that word. "
                    "Try another one."
                )

        else:

            error = "Please enter a word."


    # ------------------------------------------------------
    # Send the information to our HTML page
    # ------------------------------------------------------

    return render_template(
        "index.html",
        word_data=word_data,
        error=error
    )


# ==========================================================
# RUN THE APP
# ==========================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        port=5009
    )