import sys
import torch
import whisper

def check_gpu_setup():
    print("Python Version:", sys.version)
    
    # CUDA Information
    print("\n--- CUDA Information ---")
    print("CUDA Available:", torch.cuda.is_available())
    print("CUDA Version:", torch.version.cuda)
    print("cuDNN Version:", torch.backends.cudnn.version())
    print("CUDA Device Count:", torch.cuda.device_count())
    
    # GPU Details
    if torch.cuda.is_available():
        print("\n--- GPU Details ---")
        for i in range(torch.cuda.device_count()):
            print(f"GPU {i}:")
            print(f"  Name: {torch.cuda.get_device_name(i)}")
            print(f"  Total Memory: {torch.cuda.get_device_properties(i).total_memory / 1e9:.2f} GB")
    
    # Whisper Model GPU Test
    try:
        print("\n--- Whisper GPU Test ---")
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print("Selected Device:", device)
        
        # Load small model to test GPU
        model = whisper.load_model("tiny").to(device)
        print("Whisper Model Successfully Loaded to GPU")
    
    except Exception as e:
        print("Whisper GPU Test Failed:", str(e))

if __name__ == "__main__":
    check_gpu_setup()