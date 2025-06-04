import tkinter as tk
from openai import OpenAI
import math
import pygame
from pygame import mixer
import pyttsx3
from PIL import Image, ImageTk, ImageSequence


class Lyra:
    def __init__(self, master):
        # Initializing the GUI
        self.master = master
        master.title("Lyra Your Personal Assistant")
        
        # Background color to dark
        master.configure(bg='#2E2E2E')
        
        # Loading GIF image with Pillow
        self.gif_image = Image.open("Lyra'sLightbody.gif")  # File path
        self.gif_frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(self.gif_image)]

        # A Label widget to display the GIF
        self.gif_label = tk.Label(master, image=self.gif_frames[0], bg='#2E2E2E')
        self.gif_label.pack() 
        self.gif_label.configure(height=350)  # desired height value

        # Starting the GIF animation
        self.animate_gif(0)

        # Initializing the messages list with a system message
        self.messages = []
        self.system_msg = "Please describe Lyra's personality."
        self.messages.append({"role": "system", "content": self.system_msg})

        # Creating and packing GUI elements (label, entry field, send button, text widget)
        self.label = tk.Label(master, text="Please describe Lyra's personality, then ask your questions.", bg='#2E2E2E', fg='white')
        self.label.pack()
        
        self.entry = tk.Entry(master, width=55, bg='#404040', fg='white')
        self.entry.pack()

        # Increase the size of the buttons
        button_width = 10
        button_height = 1
        
        # Button colors
        button_bg_color = '#606060'
        button_fg_color = 'white'

        self.send_button = tk.Button(master, text="Send", command=self.send_message, width=button_width, height=button_height, bg=button_bg_color, fg=button_fg_color)
        self.send_button.pack() 
        
        # The speak button
        self.speak_button = tk.Button(master, text="Speak", command=self.speak_message, width=button_width, height=button_height, bg=button_bg_color, fg=button_fg_color)
        self.speak_button.pack()

        # Text Widget
        self.output_text = tk.Text(master, height=15, width=70)
        self.output_text.pack() 
        
        
        
        # Initialize the pygame mixer
        pygame.mixer.init()
        # Load and play background music 
        mixer.music.load('ethnic-background-music-1.mp3')
        mixer.music.play(-1)  # -1 means play continuously
        
        # Set the volume for the mixer (adjust the value based on preference)
        mixer.music.set_volume(1.0)  # 0.5 Set the volume to 50%
        
        # Initialize the text-to-speech engine
        self.engine = pyttsx3.init()
        
        # Set the volume (0.0 to 1.0, where 1.0 is the maximum volume)
        self.engine.setProperty('volume', 1.0)
        
        
    def send_message(self):
        # User's message from the entry field
        user_message = self.entry.get()
        self.messages.append({"role": "user", "content": user_message})

        # Geting the chatbot's response from OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        
        assistant_reply = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": assistant_reply})

        
        # Display the conversation in the text widget
        self.output_text.insert(tk.END, f"\nUser: {user_message}\nAssistant: {assistant_reply}\n")
        
        """# Speak the assistant's reply
        self.speak(assistant_reply) """
        
        
        # Clear the entry for the next message
        self.entry.delete(0, tk.END)
    
    def speak_message(self):
        # Speaking the last assistant's reply
        last_reply_index = next((i for i, msg in enumerate(reversed(self.messages)) if msg['role'] == 'assistant'), None)
        if last_reply_index is not None:
            last_reply = self.messages[-last_reply_index - 1]['content']
            self.speak(last_reply)
        
    def speak(self, text):
        # Use text-to-speech to speak the provided text
        self.engine.say(text) 
        self.engine.runAndWait()
     
        
    def animate_gif(self, frame_index):
        # Update the displayed frame
        self.gif_label.configure(image=self.gif_frames[frame_index])

        # Schedule the next animation frame
        self.master.after(100, lambda: self.animate_gif((frame_index + 1) % len(self.gif_frames)))

if __name__ == "__main__":
    # Initializing the OpenAI client with your API key
    client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="...",
)
    
    

    # Tkinter root window and ChatbotGUI instance
    root = tk.Tk()
    Lyra_GUI = Lyra(root)
    
    # Width and height of the window
    root.geometry("600x700")

    # Start the Tkinter main loop
    root.mainloop()
