import pcdr
from pcdr.unstable.flow import OsmoSingleFreqTransmitter as OSFT
import time

def transmit_across_range(transmitter, start=145e6, stop=146e6, step=0.005e6, repeat=True):
    while True:
        current_frequency = start
        while current_frequency < stop:
            print(f"Setting frequency to {current_frequency} Hz")
            try:
                # Use the correct method to set the frequency
                transmitter.set_center_freq(current_frequency)  # Replace with correct method if needed
            except AttributeError as e:
                print(f"Error setting frequency: {e}")
                break
            print(f"Transmitting at {current_frequency} Hz\n")
            
            time.sleep(.005)  # Adjust sleep duration as needed
            
            current_frequency += step
        
        # Optionally add a delay before restarting the frequency sweep
        if repeat:
            print("Restarting frequency sweep...")
            time.sleep(.5)  # Adjust delay between sweeps if needed
        else:
            break

# Initialize with a starting frequency
start_frequency = 145e6
transmitter = OSFT("hackrf=0", start_frequency)  # Provide the initial frequency if required

# Start the transmitter
print("Starting transmitter...")
transmitter.start()

# Set the IF gain
transmitter.set_if_gain(45)

# Transmit across the frequency range
print("Starting transmission across frequency range...")
transmit_across_range(transmitter)

# Stop the transmitter
print("Stopping transmitter...")
# Ensure the correct method is used to stop if `stop` is incorrect
try:
    transmitter.close()  # Use the correct cleanup method
except AttributeError as e:
    print(f"Error stopping transmitter: {e}")
