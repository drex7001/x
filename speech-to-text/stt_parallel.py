import os
import torch
import whisper
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed
import multiprocessing
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

class EfficientWhisperTranscriber:
    def __init__(self):
        # Detect GPU availability
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.num_cpus = multiprocessing.cpu_count()
        print(f"Device: {self.device}")
        print(f"Available CPUs: {self.num_cpus}")

    def transcribe_video(self, video_path, model, output_dir):
        """
        Transcribe a single video file
        
        Args:
            video_path (str): Path to the video file
            model (whisper.Whisper): Loaded Whisper model
            output_dir (str): Directory to save transcription
        
        Returns:
            dict: Transcription result with file details
        """
        try:
            filename = os.path.basename(video_path)
            print(f"Transcribing: {filename}")
            
            # Transcribe with GPU acceleration if available
            result = model.transcribe(
                video_path, 
                fp16=torch.cuda.is_available(),  # Use half precision on GPU
                language='en',  # Optional: specify language if known
                verbose=False
            )
            
            # Generate output filename
            transcription_filename = os.path.splitext(filename)[0] + '_transcription.txt'
            transcription_path = os.path.join(output_dir, transcription_filename)
            
            # Write transcription to file
            with open(transcription_path, 'w', encoding='utf-8') as f:
                f.write(result['text'])
            
            return {
                'input_file': video_path,
                'output_file': transcription_path,
                'success': True,
                'error': None
            }
        
        except Exception as e:
            return {
                'input_file': video_path,
                'output_file': None,
                'success': False,
                'error': str(e)
            }

    def batch_transcribe(self, video_files, model_size='base', max_workers=None):
        """
        Batch transcribe multiple video files in parallel
        
        Args:
            video_files (list): List of video file paths
            model_size (str): Whisper model size
            max_workers (int, optional): Number of parallel processes
        
        Returns:
            list: Transcription results
        """
        # Determine number of workers
        if max_workers is None:
            max_workers = min(self.num_cpus, len(video_files))
        
        # Load model on specified device
        print(f"Loading {model_size} model on {self.device}")
        model = whisper.load_model(model_size).to(self.device)
        
        # Create output directory
        output_dir = os.path.join(os.path.dirname(video_files[0]), 'transcriptions')
        os.makedirs(output_dir, exist_ok=True)
        
        # Parallel processing
        results = []
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            # Submit transcription jobs
            futures = {
                executor.submit(self.transcribe_video, video, model, output_dir): video 
                for video in video_files
            }
            
            # Collect results
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                
                # Print individual results
                if result['success']:
                    print(f"Successfully transcribed: {result['input_file']}")
                else:
                    print(f"Failed to transcribe: {result['input_file']} - {result['error']}")
        
        return results

class WhisperTranscriptionApp:
    def __init__(self, master):
        self.master = master
        self.transcriber = EfficientWhisperTranscriber()
        
        master.title("Efficient Whisper Transcription")
        master.geometry("700x600")

        # Video Files Selection
        self.files_frame = tk.Frame(master)
        self.files_frame.pack(padx=10, pady=10, fill=tk.X)

        self.selected_files_label = tk.Label(self.files_frame, text="Selected Files:")
        self.selected_files_label.pack(side=tk.TOP, anchor='w')

        self.selected_files_text = scrolledtext.ScrolledText(self.files_frame, height=6, width=70, wrap=tk.WORD)
        self.selected_files_text.pack(side=tk.TOP, fill=tk.X)
        self.selected_files_text.config(state=tk.DISABLED)

        # Device Information
        self.device_label = tk.Label(master, 
            text=f"Device: {self.transcriber.device}, CPUs: {self.transcriber.num_cpus}", 
            fg="blue"
        )
        self.device_label.pack(padx=10)

        # Model and Parallel Processing Frame
        self.config_frame = tk.Frame(master)
        self.config_frame.pack(padx=10, pady=10)

        # Model Selection
        tk.Label(self.config_frame, text="Whisper Model:").pack(side=tk.LEFT)
        self.model_var = tk.StringVar(value="base")
        self.model_dropdown = tk.OptionMenu(
            self.config_frame, 
            self.model_var, 
            "tiny", "base", "small", "medium", "large"
        )
        self.model_dropdown.pack(side=tk.LEFT, padx=5)

        # Workers Selection
        tk.Label(self.config_frame, text="Parallel Workers:").pack(side=tk.LEFT)
        self.workers_var = tk.StringVar(value=str(self.transcriber.num_cpus))
        self.workers_entry = tk.Entry(self.config_frame, textvariable=self.workers_var, width=5)
        self.workers_entry.pack(side=tk.LEFT, padx=5)

        # Buttons Frame
        self.buttons_frame = tk.Frame(master)
        self.buttons_frame.pack(padx=10, pady=10)

        self.select_button = tk.Button(
            self.buttons_frame, 
            text="Select Video Files", 
            command=self.select_files
        )
        self.select_button.pack(side=tk.LEFT, padx=5)

        self.transcribe_button = tk.Button(
            self.buttons_frame, 
            text="Transcribe", 
            command=self.start_transcription,
            state=tk.DISABLED
        )
        self.transcribe_button.pack(side=tk.LEFT, padx=5)

        # Status Frame
        self.status_frame = tk.Frame(master)
        self.status_frame.pack(padx=10, pady=10, fill=tk.X)

        self.status_label = tk.Label(self.status_frame, text="Ready", fg="green")
        self.status_label.pack(side=tk.TOP, anchor='w')

        self.progress_text = scrolledtext.ScrolledText(
            self.status_frame, 
            height=10, 
            width=70, 
            wrap=tk.WORD
        )
        self.progress_text.pack(side=tk.TOP, fill=tk.X)
        self.progress_text.config(state=tk.DISABLED)

        self.video_files = []

    def select_files(self):
        # Video file selection logic (similar to previous implementation)
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
            
            # Update selected files display
            self.selected_files_text.config(state=tk.NORMAL)
            self.selected_files_text.delete(1.0, tk.END)
            for file in self.video_files:
                self.selected_files_text.insert(tk.END, file + "\n")
            self.selected_files_text.config(state=tk.DISABLED)
            
            self.transcribe_button.config(state=tk.NORMAL)

    def start_transcription(self):
        # Disable buttons
        self.select_button.config(state=tk.DISABLED)
        self.transcribe_button.config(state=tk.DISABLED)
        
        # Clear previous progress
        self.progress_text.config(state=tk.NORMAL)
        self.progress_text.delete(1.0, tk.END)
        self.progress_text.config(state=tk.DISABLED)
        
        # Start transcription in a separate thread
        import threading
        threading.Thread(target=self.run_transcription, daemon=True).start()

    def run_transcription(self):
        try:
            # Get model and workers from UI
            model_size = self.model_var.get()
            workers = int(self.workers_var.get())

            # Update status
            self.update_status(f"Starting transcription with {model_size} model")
            self.update_status(f"Using {workers} parallel workers")
            
            # Perform transcription
            results = self.transcriber.batch_transcribe(
                self.video_files, 
                model_size=model_size, 
                max_workers=workers
            )
            
            # Summarize results
            successful = sum(1 for r in results if r['success'])
            failed = sum(1 for r in results if not r['success'])
            
            self.update_status(f"Transcription Complete")
            self.update_status(f"Successful: {successful}, Failed: {failed}")
        
        except Exception as e:
            self.update_status(f"Error: {str(e)}")
        
        finally:
            # Re-enable buttons
            self.master.after(0, self.reset_buttons)

    def update_status(self, message):
        # Thread-safe status update
        self.master.after(0, self._update_status_thread, message)

    def _update_status_thread(self, message):
        # Actual status update method
        self.progress_text.config(state=tk.NORMAL)
        self.progress_text.insert(tk.END, message + "\n")
        self.progress_text.see(tk.END)
        self.progress_text.config(state=tk.DISABLED)

    def reset_buttons(self):
        # Reset UI
        self.select_button.config(state=tk.NORMAL)
        self.transcribe_button.config(state=tk.NORMAL)
        self.status_label.config(text="Ready", fg="green")

def main():
    root = tk.Tk()
    app = WhisperTranscriptionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()