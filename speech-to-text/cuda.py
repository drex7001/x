import os
import torch
import whisper
import tkinter as tk
from tkinter import filedialog, scrolledtext
import threading
import logging

class WhisperTranscriber:
    def __init__(self):
        # Configure logging
        logging.basicConfig(
            level=logging.INFO, 
            format='%(asctime)s - %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)

        # Check and log GPU availability
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.logger.info(f"Transcription will use: {self.device}")

    def transcribe_video(self, video_path, model, output_dir):
        """
        Transcribe a single video file using Whisper
        """
        try:
            filename = os.path.basename(video_path)
            self.logger.info(f"Transcribing: {filename}")
            
            # Transcribe with GPU optimization
            result = model.transcribe(
                video_path, 
                fp16=torch.cuda.is_available(),  # Use half precision on GPU
                language='en',  # Adjust language as needed
                verbose=False
            )
            
            # Generate output path
            transcription_filename = os.path.splitext(filename)[0] + '_transcription.txt'
            transcription_path = os.path.join(output_dir, transcription_filename)
            
            # Write transcription
            with open(transcription_path, 'w', encoding='utf-8') as f:
                f.write(result['text'])
            
            self.logger.info(f"Transcription saved: {transcription_path}")
            return True
        
        except Exception as e:
            self.logger.error(f"Transcription failed for {filename}: {e}")
            return False

    def transcribe_batch(self, video_files, model_size='base'):
        """
        Batch transcribe videos using CUDA
        """
        try:
            # Create output directory
            if not video_files:
                self.logger.warning("No video files selected")
                return 0, 0

            output_dir = os.path.join(os.path.dirname(video_files[0]), 'transcriptions')
            os.makedirs(output_dir, exist_ok=True)

            # Load Whisper model to GPU
            self.logger.info(f"Loading {model_size} Whisper model to {self.device}")
            model = whisper.load_model(model_size).to(self.device)
            self.logger.info(f"Whisper model loaded on {model.device}")

            # Transcribe videos
            successful = 0
            failed = 0
            for video in video_files:
                if self.transcribe_video(video, model, output_dir):
                    successful += 1
                else:
                    failed += 1

            return successful, failed

        except Exception as e:
            self.logger.error(f"Batch transcription error: {e}")
            return 0, len(video_files)

class WhisperTranscriptionApp:
    def __init__(self, master):
        self.master = master
        self.transcriber = WhisperTranscriber()
        
        master.title("Whisper GPU Transcription")
        master.geometry("600x500")

        # Device Information
        self.device_label = tk.Label(
            master, 
            text=f"Transcription Device: {self.transcriber.device}", 
            fg="blue"
        )
        self.device_label.pack(pady=10)

        # File Selection
        tk.Button(
            master, 
            text="Select Video Files", 
            command=self.select_files
        ).pack(pady=10)

        # Selected Files Display
        self.files_text = scrolledtext.ScrolledText(
            master, height=6, width=70, wrap=tk.WORD
        )
        self.files_text.pack(pady=10)
        self.files_text.config(state=tk.DISABLED)

        # Model Selection
        tk.Label(master, text="Whisper Model:").pack()
        self.model_var = tk.StringVar(value="base")
        tk.OptionMenu(
            master, 
            self.model_var, 
            "tiny", "base", "small", "medium", "large"
        ).pack()

        # Transcribe Button
        self.transcribe_btn = tk.Button(
            master, 
            text="Start Transcription", 
            command=self.start_transcription,
            state=tk.DISABLED
        )
        self.transcribe_btn.pack(pady=10)

        # Progress Display
        self.progress_text = scrolledtext.ScrolledText(
            master, height=10, width=70, wrap=tk.WORD
        )
        self.progress_text.pack(pady=10)
        
        self.video_files = []

    def select_files(self):
        filetypes = [
            ('Video Files', '*.mp4 *.avi *.mov *.mkv *.flv'),
            ('All Files', '*.*')
        ]
        selected_files = filedialog.askopenfilenames(
            title="Select Video Files", 
            filetypes=filetypes
        )
        
        if selected_files:
            self.video_files = list(selected_files)
            
            # Update file display
            self.files_text.config(state=tk.NORMAL)
            self.files_text.delete(1.0, tk.END)
            for file in self.video_files:
                self.files_text.insert(tk.END, file + "\n")
            self.files_text.config(state=tk.DISABLED)
            
            self.transcribe_btn.config(state=tk.NORMAL)

    def start_transcription(self):
        # Disable buttons during transcription
        self.transcribe_btn.config(state=tk.DISABLED)
        
        # Clear previous progress
        self.progress_text.config(state=tk.NORMAL)
        self.progress_text.delete(1.0, tk.END)
        self.progress_text.config(state=tk.DISABLED)
        
        # Start in a separate thread
        threading.Thread(target=self.run_transcription, daemon=True).start()

    def run_transcription(self):
        try:
            model_size = self.model_var.get()
            
            # Update UI with transcription start
            self.update_progress(f"Starting transcription with {model_size} model")
            
            # Perform transcription
            successful, failed = self.transcriber.transcribe_batch(
                self.video_files, 
                model_size=model_size
            )
            
            # Update UI with results
            self.update_progress(f"Transcription Complete")
            self.update_progress(f"Successful: {successful}, Failed: {failed}")
        
        except Exception as e:
            self.update_progress(f"Transcription Error: {e}")
        
        finally:
            # Re-enable transcribe button
            self.master.after(0, lambda: self.transcribe_btn.config(state=tk.NORMAL))

    def update_progress(self, message):
        # Thread-safe progress update
        self.master.after(0, self._update_progress_thread, message)

    def _update_progress_thread(self, message):
        # Actual progress update method
        self.progress_text.config(state=tk.NORMAL)
        self.progress_text.insert(tk.END, message + "\n")
        self.progress_text.see(tk.END)
        self.progress_text.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = WhisperTranscriptionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()