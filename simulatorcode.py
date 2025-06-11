import cv2
import numpy as np
import matplotlib.pyplot as plt
from collections import deque
import time
import pygame  # Import pygame for sound

# Initialize pygame mixer for sound playback
pygame.mixer.init()

# Load different sounds based on frequency
low_freq_sound = pygame.mixer.Sound("low_beep.wav")  
mid_freq_sound = pygame.mixer.Sound("mid_beep.wav")  
high_freq_sound = pygame.mixer.Sound("high_beep.wav")  

current_freq = None  # Track the last frequency to detect changes

def play_sound_for_frequency(freq):
    """Plays a new sound if frequency changes, stopping the previous one."""
    global current_freq
    
    if current_freq == freq:  # If frequency is the same, do nothing
        return  
    
    pygame.mixer.stop()  # Stop any currently playing sound

    if freq < 7:
        low_freq_sound.play()
    elif 7 <= freq < 15:
        mid_freq_sound.play()
    else:
        high_freq_sound.play()

    current_freq = freq  # Update the current frequency

def create_plot_image(signal, title="Simulated EEG Signal"):
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(signal, color='blue')
    ax.set_title(title)
    ax.set_xlabel("Time")
    ax.set_ylabel("Amplitude")
    plt.tight_layout()
    
    fig.canvas.draw()
    
    try:
        image = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    except AttributeError:
        image_argb = np.frombuffer(fig.canvas.tostring_argb(), dtype=np.uint8)
        width, height = fig.canvas.get_width_height()
        image_argb = image_argb.reshape((height, width, 4))
        image = image_argb[:, :, 1:]
    
    width, height = fig.canvas.get_width_height()
    image = image.reshape((height, width, 3))
    plt.close(fig)
    return image

def generate_eeg_signal(t, freq=10, noise_level=0.5):
    """Simulate an EEG signal with sine waves and noise."""
    return np.sin(2 * np.pi * freq * t) + noise_level * np.random.randn(len(t))

def nothing(x):
    pass

def main():
    window_size = 100  
    sampling_rate = 50  
    t = np.linspace(0, window_size / sampling_rate, window_size)
    eeg_buffer = deque([0] * window_size, maxlen=window_size)

    cv2.namedWindow("EEG Signal", cv2.WINDOW_NORMAL)

    # Create trackbars for frequency and noise level
    cv2.createTrackbar("Frequency x0.1", "EEG Signal", 100, 500, nothing)
    cv2.createTrackbar("Noise x0.01", "EEG Signal", 50, 100, nothing)
    
    start_time = time.time()
    
    while True:
        freq = cv2.getTrackbarPos("Frequency x0.1", "EEG Signal") * 0.1
        noise_level = cv2.getTrackbarPos("Noise x0.01", "EEG Signal") * 0.01
        
        current_time = time.time() - start_time
        t_new = np.linspace(current_time, current_time + (1 / sampling_rate), 1)
        new_point = generate_eeg_signal(t_new, freq=freq, noise_level=noise_level)[0]
        eeg_buffer.append(new_point)
        
        command_text = "Command Detected: Action Triggered!" if new_point > 0.8 else ""
        
        if new_point > 0.8:  # If a spike is detected
            play_sound_for_frequency(freq)  # Play sound & stop previous if freq changes
        
        signal_array = np.array(eeg_buffer)
        plot_img = create_plot_image(signal_array)
        plot_img = cv2.cvtColor(plot_img, cv2.COLOR_RGB2BGR)
        
        if command_text:
            cv2.putText(plot_img, command_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                        0.8, (0, 0, 255), 2, cv2.LINE_AA)
        
        cv2.putText(plot_img, f"Freq: {freq:.1f} Hz", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.7, (255, 255, 255), 2)
        cv2.putText(plot_img, f"Noise: {noise_level:.2f}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.7, (255, 255, 255), 2)
        
        cv2.imshow("EEG Signal", plot_img)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            cv2.imwrite("eeg_snapshot.png", plot_img)
            print("Image saved as eeg_snapshot.png")
        if key == 27:  # ESC key
            break
        
        if cv2.getWindowProperty("EEG Signal", cv2.WND_PROP_VISIBLE) < 1:
            break

    cv2.destroyAllWindows()
    cv2.waitKey(1)

if __name__ == '__main__':
    main()
