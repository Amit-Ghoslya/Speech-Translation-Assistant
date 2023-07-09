import tkinter as tk
import speech_recognition as spr
from googletrans import Translator
from gtts import gTTS
from playsound import playsound

# Create Recognizer and Microphone instances
recog1 = spr.Recognizer()
mc = spr.Microphone()

# Create Translator instance
translator = Translator()

def recognize_speech():
    # Clear the text box
    text_box.delete('1.0', tk.END)

    with mc as source:
        # Adjust for ambient noise
        recog1.adjust_for_ambient_noise(source, duration=0.2)

        # Capture the speech from the microphone
        audio = recog1.listen(source)

        try:
            # Recognize the speech
            get_sentence = recog1.recognize_google(audio)

            # Display the sentence in the text box
            text_box.insert(tk.END, get_sentence)
        except spr.UnknownValueError:
            text_box.insert(tk.END, "\nUnable to Understand the Input")

def translate_speech():
    # Get the spoken phrase from the text box
    get_sentence = text_box.get("1.0", tk.END).strip()

    if get_sentence:
        try:
            # Detect the input language
            lang_detect = translator.detect(get_sentence)
            input_lang = lang_detect.lang

            # Translate the sentence to Hindi
            text_to_translate = translator.translate(get_sentence, src=input_lang, dest='hi')
            translated_text = text_to_translate.text

            # Display the translated text in the text box
            text_box.insert(tk.END, "\nTranslated Phrase: " + translated_text)

            # Generate speech from the translated text
            tts = gTTS(text=translated_text, lang='hi')

            # Save the speech as a temporary file
            tts.save('temp.mp3')

            # Play the speech using the playsound library
            playsound('temp.mp3')
        except spr.RequestError as e:
            text_box.insert(tk.END, "\nUnable to provide Required Output: {}".format(e))

# Create the GUI window
window = tk.Tk()
window.title("Speech Translation")
window.geometry("400x300")

# Create a label
label = tk.Label(window, text="Speak or type a sentence:")
label.pack()

# Create a text box
text_box = tk.Text(window, height=10, width=40)
text_box.pack()

# Create a recognize button
recognize_button = tk.Button(window, text="Recognize", command=recognize_speech)
recognize_button.pack()

# Create a translate button
translate_button = tk.Button(window, text="Translate", command=translate_speech)
translate_button.pack()

# Start the GUI event loop
window.mainloop()
