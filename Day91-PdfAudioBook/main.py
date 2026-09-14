import base64
import os
import subprocess
import tempfile

import requests
from pypdf import PdfReader
from tkinter import Tk, filedialog


# ==========================================================
# SETTINGS
# ==========================================================

GOOGLE_TTS_URL = "https://texttospeech.googleapis.com/v1/text:synthesize"

OUTPUT_FILE = "output.mp3"

# Google Cloud TTS has a 5,000-byte request limit.
# We stay comfortably below that limit.
MAX_CHUNK_BYTES = 4500


# ==========================================================
# SELECT PDF
# ==========================================================

def choose_pdf():
    """
    Opens a file picker so the user can select a PDF.
    """

    window = Tk()
    window.withdraw()

    pdf_path = filedialog.askopenfilename(
        title="Choose a PDF file",
        filetypes=[
            ("PDF files", "*.pdf")
        ]
    )

    window.destroy()

    return pdf_path


# ==========================================================
# EXTRACT TEXT FROM PDF
# ==========================================================

def extract_text(pdf_path):
    """
    Reads every page of the PDF and combines the text.
    """

    reader = PdfReader(pdf_path)

    pages = []

    for page in reader.pages:

        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages)


# ==========================================================
# SPLIT TEXT INTO API-SIZED CHUNKS
# ==========================================================

def split_text(text):
    """
    Splits a large PDF into smaller pieces that can
    safely be sent to the TTS API.
    """

    words = text.split()

    chunks = []

    current_chunk = ""
    current_size = 0

    for word in words:

        word_size = len((word + " ").encode("utf-8"))

        if current_size + word_size > MAX_CHUNK_BYTES:

            if current_chunk:
                chunks.append(current_chunk)

            current_chunk = word + " "
            current_size = word_size

        else:

            current_chunk += word + " "
            current_size += word_size

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


# ==========================================================
# GET GOOGLE CLOUD ACCESS TOKEN
# ==========================================================

def get_access_token():
    """
    Uses the Google Cloud CLI to obtain an access token.

    You need to have authenticated using:
        gcloud auth application-default login
    """

    result = subprocess.run(
        [
            "gcloud",
            "auth",
            "application-default",
            "print-access-token"
        ],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:

        raise RuntimeError(
            "Could not get Google Cloud credentials.\n"
            "Run:\n"
            "gcloud auth application-default login"
        )

    return result.stdout.strip()


# ==========================================================
# CONVERT ONE CHUNK TO SPEECH
# ==========================================================

def text_to_speech(text, access_token):
    """
    Sends one piece of text to Google Cloud TTS
    and returns the resulting audio.
    """

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    data = {

        "input": {
            "text": text
        },

        "voice": {
            "languageCode": "en-US",
            "name": "en-US-Neural2-C"
        },

        "audioConfig": {
            "audioEncoding": "MP3"
        }
    }

    response = requests.post(
        GOOGLE_TTS_URL,
        headers=headers,
        json=data
    )

    response.raise_for_status()

    result = response.json()

    audio_data = result["audioContent"]

    return base64.b64decode(audio_data)


# ==========================================================
# CREATE AUDIOBOOK
# ==========================================================

def create_audiobook(chunks, access_token):
    """
    Converts every text chunk into audio and combines
    them into one MP3 file.
    """

    audio_files = []

    try:

        for number, chunk in enumerate(chunks, start=1):

            print(
                f"Converting chunk {number}/{len(chunks)}..."
            )

            audio_data = text_to_speech(
                chunk,
                access_token
            )

            temporary_file = tempfile.NamedTemporaryFile(
                suffix=".mp3",
                delete=False
            )

            temporary_file.write(audio_data)

            temporary_file.close()

            audio_files.append(temporary_file.name)

        combine_audio_files(
            audio_files,
            OUTPUT_FILE
        )

    finally:

        # Delete temporary audio files
        for file in audio_files:

            if os.path.exists(file):
                os.remove(file)


# ==========================================================
# COMBINE MP3 FILES
# ==========================================================

def combine_audio_files(audio_files, output_file):
    """
    Combines all the temporary MP3 files into one file
    using FFmpeg.
    """

    list_file = tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".txt",
        delete=False
    )

    try:

        for audio_file in audio_files:

            # FFmpeg expects paths in this format
            safe_path = audio_file.replace("'", "'\\''")

            list_file.write(
                f"file '{safe_path}'\n"
            )

        list_file.close()

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                list_file.name,
                "-c",
                "copy",
                output_file
            ],
            check=True
        )

    finally:

        if os.path.exists(list_file.name):
            os.remove(list_file.name)


# ==========================================================
# MAIN PROGRAM
# ==========================================================

def main():

    print("\n==============================")
    print("       PDF → AUDIOBOOK")
    print("==============================\n")

    # Step 1: Select PDF
    pdf_path = choose_pdf()

    if not pdf_path:

        print("No PDF selected.")
        return

    print("PDF selected:")
    print(pdf_path)

    # Step 2: Extract text
    print("\nExtracting text...")

    text = extract_text(pdf_path)

    if not text.strip():

        print("No readable text was found in the PDF.")
        return

    print(
        f"Extracted {len(text)} characters."
    )

    # Step 3: Split text
    print("\nPreparing text for the API...")

    chunks = split_text(text)

    print(
        f"Created {len(chunks)} text chunks."
    )

    # Step 4: Authenticate
    print("\nGetting Google Cloud credentials...")

    access_token = get_access_token()

    print("Authentication successful.")

    # Step 5: Convert everything to speech
    print("\nCreating audiobook...\n")

    create_audiobook(
        chunks,
        access_token
    )

    print("\n==============================")
    print("Audiobook created successfully!")
    print(f"Saved as: {OUTPUT_FILE}")
    print("==============================")


# ==========================================================
# RUN PROGRAM
# ==========================================================

if __name__ == "__main__":
    main()