import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import whisper
import threading

class WhisperTranscriptionApp:
    def __init__(self, master):
        self.master = master
        master.title("Whisper Video Transcription")
        master.geometry("600x500")

        # Video Files Selection
        self.files_frame = tk.Frame(master)
        self.files_frame.pack(padx=10, pady=10, fill=tk.X)

        self.selected_files_label = tk.Label(self.files_frame, text="Selected Files:")
        self.selected_files_label.pack(side=tk.TOP, anchor='w')

        self.selected_files_text = scrolledtext.ScrolledText(self.files_frame, height=6, width=70, wrap=tk.WORD)
        self.selected_files_text.pack(side=tk.TOP, fill=tk.X)
        self.selected_files_text.config(state=tk.DISABLED)

        # Buttons Frame
        self.buttons_frame = tk.Frame(master)
        self.buttons_frame.pack(padx=10, pady=10)

        self.select_button = tk.Button(self.buttons_frame, text="Select Video Files", command=self.select_files)
        self.select_button.pack(side=tk.LEFT, padx=5)

        self.transcribe_button = tk.Button(self.buttons_frame, text="Transcribe", command=self.start_transcription, state=tk.DISABLED)
        self.transcribe_button.pack(side=tk.LEFT, padx=5)

        # Model Selection
        self.model_frame = tk.Frame(master)
        self.model_frame.pack(padx=10, pady=10)

        self.model_label = tk.Label(self.model_frame, text="Select Whisper Model:")
        self.model_label.pack(side=tk.LEFT)

        self.model_var = tk.StringVar(value="base")
        self.model_options = ["tiny", "base", "small", "medium", "large"]
        self.model_dropdown = tk.OptionMenu(self.model_frame, self.model_var, *self.model_options)
        self.model_dropdown.pack(side=tk.LEFT, padx=5)

        # Status Frame
        self.status_frame = tk.Frame(master)
        self.status_frame.pack(padx=10, pady=10, fill=tk.X)

        self.status_label = tk.Label(self.status_frame, text="Status: Ready", fg="green")
        self.status_label.pack(side=tk.TOP, anchor='w')

        self.progress_text = scrolledtext.ScrolledText(self.status_frame, height=6, width=70, wrap=tk.WORD)
        self.progress_text.pack(side=tk.TOP, fill=tk.X)
        self.progress_text.config(state=tk.DISABLED)

        # Video files list
        self.video_files = []

    def select_files(self):
        # Reset previous selection
        self.video_files = []
        self.selected_files_text.config(state=tk.NORMAL)
        self.selected_files_text.delete(1.0, tk.END)

        # Open file dialog to select video files
        filetypes = [
            ('Video Files', '*.mp4 *.avi *.mov *.mkv *.flv'),
            ('All Files', '*.*')
        ]
        selected_files = filedialog.askopenfilenames(title="Select Video Files", filetypes=filetypes)
        
        # Update selected files
        if selected_files:
            self.video_files = list(selected_files)
            for file in self.video_files:
                self.selected_files_text.insert(tk.END, file + "\n")
            
            self.selected_files_text.config(state=tk.DISABLED)
            self.transcribe_button.config(state=tk.NORMAL)

    def start_transcription(self):
        # Disable buttons during transcription
        self.select_button.config(state=tk.DISABLED)
        self.transcribe_button.config(state=tk.DISABLED)
        
        # Clear previous progress
        self.progress_text.config(state=tk.NORMAL)
        self.progress_text.delete(1.0, tk.END)
        
        # Start transcription in a separate thread
        threading.Thread(target=self.transcribe_videos, daemon=True).start()

    def transcribe_videos(self):
        try:
            # Load the Whisper model
            model_size = self.model_var.get()
            self.update_status(f"Loading {model_size} Whisper model...")
            model = whisper.load_model(model_size)

            # Create transcriptions directory
            transcription_dir = os.path.join(os.path.dirname(self.video_files[0]), 'transcriptions')
            os.makedirs(transcription_dir, exist_ok=True)

            # Transcribe each video
            for video_path in self.video_files:
                try:
                    filename = os.path.basename(video_path)
                    self.update_status(f"Transcribing: {filename}")
                    
                    # Transcribe the video
                    result = model.transcribe(video_path, fp16=False)
                    
                    # Generate transcription filename
                    transcription_filename = os.path.splitext(filename)[0] + '_transcription.txt'
                    transcription_path = os.path.join(transcription_dir, transcription_filename)
                    
                    # Write transcription to file
                    with open(transcription_path, 'w', encoding='utf-8') as f:
                        f.write(result['text'])
                    
                    self.update_status(f"Transcription saved to {transcription_path}")
                
                except Exception as e:
                    self.update_status(f"Error transcribing {filename}: {str(e)}")

            self.update_status("Transcription complete!")
        
        except Exception as e:
            self.update_status(f"Error: {str(e)}")
        
        finally:
            # Re-enable buttons
            self.master.after(0, self.reset_buttons)

    def update_status(self, message):
        # Update status in the GUI from a different thread
        self.master.after(0, self._update_status_thread, message)

    def _update_status_thread(self, message):
        # Actual status update method
        self.progress_text.config(state=tk.NORMAL)
        self.progress_text.insert(tk.END, message + "\n")
        self.progress_text.see(tk.END)
        self.progress_text.config(state=tk.DISABLED)

    def reset_buttons(self):
        # Reset buttons and status
        self.select_button.config(state=tk.NORMAL)
        self.transcribe_button.config(state=tk.NORMAL)
        self.status_label.config(text="Status: Ready", fg="green")

def main():
    root = tk.Tk()
    app = WhisperTranscriptionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
# import os
# import whisper
# from pathlib import Path

# def transcribe_videos(video_directory):
#     """
#     Transcribe all video files in the specified directory using OpenAI Whisper.
    
#     Args:
#         video_directory (str): Path to the directory containing video files
#     """
#     # Load the Whisper model (you can choose different sizes: 'tiny', 'base', 'small', 'medium', 'large')
#     model = whisper.load_model('base')
    
#     # Supported video file extensions
#     VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv', '.flv']
    
#     # Create a directory for transcriptions if it doesn't exist
#     transcription_dir = os.path.join(video_directory, 'transcriptions')
#     os.makedirs(transcription_dir, exist_ok=True)
    
#     # Iterate through video files in the directory
#     for filename in os.listdir(video_directory):
#         # Check if the file is a video
#         if Path(filename).suffix.lower() in VIDEO_EXTENSIONS:
#             video_path = os.path.join(video_directory, filename)
            
#             try:
#                 print(f"Transcribing: {filename}")
                
#                 # Transcribe the video
#                 result = model.transcribe(video_path, fp16=False)
                
#                 # Generate transcription filename
#                 transcription_filename = os.path.splitext(filename)[0] + '_transcription.txt'
#                 transcription_path = os.path.join(transcription_dir, transcription_filename)
                
#                 # Write transcription to file
#                 with open(transcription_path, 'w', encoding='utf-8') as f:
#                     f.write(result['text'])
                
#                 print(f"Transcription saved to {transcription_path}")
            
#             except Exception as e:
#                 print(f"Error transcribing {filename}: {e}")

# # Example usage
# if __name__ == "__main__":
#     # Replace with the path to your video files directory
#     video_directory = '/path/to/your/videos'
#     transcribe_videos(video_directory)