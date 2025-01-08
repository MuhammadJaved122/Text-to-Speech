import tkinter as tk
from tkinter import messagebox
from nltk.sentiment import SentimentIntensityAnalyzer
from gtts import gTTS
import os
import nltk

nltk.download('vader_lexicon')

# Function Definitions
def analyze_sentiment_vader(text):
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(text)
    if sentiment_score['compound'] > 0.05:
        sentiment = "POSITIVE"
    elif sentiment_score['compound'] < -0.05:
        sentiment = "NEGATIVE"
    else:
        sentiment = "NEUTRAL"
    return sentiment, sentiment_score

def text_to_speech(text, filename="output.mp3"):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    os.system(f"start {filename}")

def get_user_input():
    user_text = text_input.get("1.0", tk.END).strip()
    if not user_text:
        messagebox.showwarning("Input Error", "Please enter some text.")
        return None
    return user_text

def convert_to_tts():
    user_text = get_user_input()
    if user_text:
        text_to_speech(user_text, "input_phrase.mp3")
        messagebox.showinfo("TTS", "Text has been converted to speech.")

def perform_analysis():
    user_text = get_user_input()
    if user_text:
        sentiment, scores = analyze_sentiment_vader(user_text)

        result_label.config(text=f"Sentiment: {sentiment}")
        scores_label.config(
            text=(f"Scores:\nPositive: {scores['pos']:.2f}, Neutral: {scores['neu']:.2f}, "
                  f"Negative: {scores['neg']:.2f}, Compound: {scores['compound']:.2f}")
        )

        output_box.config(state="normal")
        output_box.delete("1.0", tk.END)
        output_box.insert(
            tk.END, f"Sentiment: {sentiment}\n"
            f"Positive: {scores['pos']:.2f}\nNeutral: {scores['neu']:.2f}\n"
            f"Negative: {scores['neg']:.2f}\nCompound: {scores['compound']:.2f}"
        )
        output_box.config(state="disabled")

        analysis_text = (
            f"The sentiment analysis results are as follows: "
            f"Sentiment: {sentiment}. Positive score: {scores['pos']:.2f}. "
            f"Neutral score: {scores['neu']:.2f}. Negative score: {scores['neg']:.2f}. "
            f"Compound score: {scores['compound']:.2f}."
        )
        text_to_speech(analysis_text, "analysis_output.mp3")

def perform_both():
    user_text = get_user_input()
    if user_text:
        convert_to_tts()
        perform_analysis()

def exit_application():
    root.destroy()

# GUI Setup
root = tk.Tk()
root.title("Sentiment Analysis and Text-to-Speech")
root.geometry("900x700")
root.resizable(True, True)
root.config(bg="#ffffff")

# Heading Label
heading_label = tk.Label(
    root, text="Sentiment Analysis with TTS", font=("Helvetica", 20, "bold"), bg="#ffffff", fg="#333333"
)
heading_label.pack(pady=20)

# Text Input Field (smaller size)
text_input_label = tk.Label(root, text="Enter your text below:", font=("Helvetica", 14), bg="#ffffff", fg="#333333")
text_input_label.pack(anchor="w", padx=30)

# Create a frame to hold the Text widget and Scrollbar
text_input_frame = tk.Frame(root)
text_input_frame.pack(pady=10, padx=30)

# Create a Text widget for input
text_input = tk.Text(text_input_frame, height=6, width=60, font=("Helvetica", 12), bd=2, relief="groove", bg="#f7f7f7")
text_input.pack(side="left", fill="both", expand=True)

# Create a Scrollbar and link it to the Text widget
scrollbar = tk.Scrollbar(text_input_frame, orient="vertical", command=text_input.yview)
scrollbar.pack(side="right", fill="y")

# Configure the Text widget to work with the scrollbar
text_input.config(yscrollcommand=scrollbar.set)

# Menu Buttons with sky blue color and red for exit
menu_frame = tk.Frame(root, bg="#ffffff")
menu_frame.pack(pady=20)

menu_2_button = tk.Button(
    menu_frame, text="Convert to TTS", font=("Helvetica", 12), command=convert_to_tts, bg="#4CAF50", fg="white", relief="raised", width=20
)
menu_2_button.grid(row=0, column=0, padx=20, pady=10)

menu_3_button = tk.Button(
    menu_frame, text="Analyze Sentiment", font=("Helvetica", 12), command=perform_analysis, bg="#4CAF50", fg="white", relief="raised", width=20
)
menu_3_button.grid(row=1, column=0, padx=20, pady=10)

menu_4_button = tk.Button(
    menu_frame, text="Perform Both", font=("Helvetica", 12), command=perform_both, bg="#4CAF50", fg="white", relief="raised", width=20
)
menu_4_button.grid(row=0, column=1, padx=20, pady=10)

menu_5_button = tk.Button(
    menu_frame, text="Exit", font=("Helvetica", 12), command=exit_application, bg="#f44336", fg="white", relief="raised", width=20
)
menu_5_button.grid(row=1, column=1, padx=20, pady=10)

# Output Box for Sentiment Analysis (same size as input box)
output_label = tk.Label(root, text="Sentiment Analysis Output:", font=("Helvetica", 14), bg="#ffffff", fg="#333333")
output_label.pack(anchor="w", padx=30, pady=(10, 0))

output_box = tk.Text(root, height=6, width=60, font=("Helvetica", 12), bd=2, relief="groove", state="disabled", bg="#f7f7f7")
output_box.pack(pady=10, padx=30)

# Results Labels
result_label = tk.Label(root, text="", font=("Helvetica", 14, "bold"), fg="#333333", bg="#ffffff")
result_label.pack(pady=5)

scores_label = tk.Label(root, text="", font=("Helvetica", 12), bg="#ffffff", fg="#333333")
scores_label.pack(pady=5)

# Run the Application
root.mainloop()
