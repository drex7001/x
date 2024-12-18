import time
import winsound

def countdown(minutes):
    # Convert minutes to total seconds
    total_seconds = int(minutes * 60)  # Ensure total_seconds is an integer

    while total_seconds > 0:
        # Compute the current minutes and seconds
        mins, secs = divmod(total_seconds, 60)

        # Ensure mins and secs are integers for formatting
        mins = int(mins)
        secs = int(secs)

        # Format the time as MM:SS
        timer = f"{mins:02d}:{secs:02d}"

        # Print the time left
        print("Time Remaining:", timer, end="\r")

        # Wait for a second
        time.sleep(1)

        # Decrement the total number of seconds
        total_seconds -= 1

    # When the countdown finishes, print done and beep
    print("\nTime Remaining: 00:00")
    # Play a beep sound
    winsound.Beep(1000, 1000)  # 1000 Hz frequency for 1 second

if __name__ == "__main__":
    # Ask the user to input the countdown time in minutes
    minutes = float(input("Enter the countdown time in minutes: "))
    countdown(minutes)
