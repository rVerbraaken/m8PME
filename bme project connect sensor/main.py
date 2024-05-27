from CreaTeBME import SensorEmulator, SensorManager
import numpy as np
import matplotlib.animation as animation
import matplotlib.pyplot as plt

# Create a sensor manager for the given sensor names using the given callback
manager = SensorManager(['874E'])

sample_rate = 100
max_samples = 1000  # Maximum number of samples to store
accelerometer = np.zeros((max_samples, 3))  # Initialize numpy array for accelerometer data
gyroscope = np.zeros((max_samples, 3))  # Initialize numpy array for gyroscope data
fig, (ax1, ax2) = plt.subplots(2, 1)  # Create subplots for accelerometer and gyroscope data

# Start the sensor manager
manager.start()
manager.set_sample_rate(sample_rate)

# Current index in the circular buffer
current_index = 0



def animate(frame):
    global accelerometer, gyroscope, current_index

    measurements = manager.get_measurements()

    for sensor, data in measurements.items():
        if len(data) > 0:
            for datapoint in data:
                accelerometer[current_index] = datapoint[:3]
                gyroscope[current_index] = datapoint[3:6]
                current_index = (current_index + 1) % max_samples
                angle1 = datapoint[1] * 100
                print(angle1)

    # Clear axis
    ax1.clear()
    ax2.clear()

    # Plot accelerometer data
    ax1.plot(accelerometer[:, 0], label='X-axis')
    ax1.plot(accelerometer[:, 1], label='Y-axis')
    ax1.plot(accelerometer[:, 2], label='Z-axis')
    ax1.set_title('Accelerometer Data')
    ax1.legend()


    # Plot gyroscope data
    ax2.plot(gyroscope[:, 0], label='X-axis')
    ax2.plot(gyroscope[:, 1], label='Y-axis')
    ax2.plot(gyroscope[:, 2], label='Z-axis')
    ax2.set_title('Gyroscope Data')
    ax2.legend()


# Animate the plot
ani = animation.FuncAnimation(fig, animate, interval=50)
plt.tight_layout()
plt.show()

# Stop the sensor manager
manager.stop()
