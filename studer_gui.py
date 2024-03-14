import tkinter as tk
from tkinter import ttk
import tkinter as tk

import paho.mqtt.client as mqtt

# MQTT settings
mqtt_broker = "net.ad.kolins.cz"
mqtt_topics = [
    "studer/XT/XT1_active_power_kW",
    "studer/XT/XT2_active_power_kW",
    "studer/XT/XT3_active_power_kW",
    "studer/XT/XT4_active_power_kW"
]

# Create a Tkinter window
window = tk.Tk()
window.title("Kolin Studer GUI")
window.geometry("400x200")

# Create scales and labels
scales = []
value_labels = []



# Create a frame for the headings and place it in the window
heading_frame = ttk.Frame(window)
heading_frame.grid(row=0, column=0, sticky='w')

# Create the heading labels and place them in the heading frame
headng_label1 = ttk.Label(heading_frame, text="Inverter", font=("TkDefaultFont", 10, "bold"))
headng_label1.grid(row=0, column=0, padx=10, sticky='w')

headng_label2 = ttk.Label(heading_frame, text="<< Charging  Discharging >>", font=("TkDefaultFont", 10, "bold"))
headng_label2.grid(row=0, column=1, padx=10, sticky='w')

headng_label3 = ttk.Label(heading_frame, text="Power", font=("TkDefaultFont", 10, "bold"))
headng_label3.grid(row=0, column=2, padx=10, sticky='w')

# Create a new frame for each row, place the labels and scale in the frame, and place the frame in the window
for i in range(len(mqtt_topics)):
    frame = ttk.Frame(window)
    frame.grid(row=i+1, column=0, sticky='w')  # Place the frame in row i+1, column 0 of the window

    studer_label = ttk.Label(frame, text=f"Studer {i+1}")
    studer_label.grid(row=0, column=0, padx=10, sticky='w')  # Place the label in row 0, column 0 of the frame

    scale = ttk.Scale(frame, from_=-10, to=10, length=200)
    scale.grid(row=0, column=1, sticky='w')  # Place the scale in row 0, column 1 of the frame
    scales.append(scale)

    value_label = ttk.Label(frame, text="0")
    value_label.grid(row=0, column=2, padx=10, sticky='w')  # Place the label in row 0, column 2 of the frame
    value_labels.append(value_label)









# MQTT callback function
def on_message(client, userdata, msg):
    # Parse the received message and update the scales and labels
    topic = msg.topic
    value = float(msg.payload.decode())
    index = mqtt_topics.index(topic)
    scales[index].set(value)
    value_labels[index]['text'] = str(value) + " kW"
    if value < 0:
        value_labels[index]['foreground'] = 'green'
    elif value > 0:
        value_labels[index]['foreground'] = 'red'
    else:
        value_labels[index]['foreground'] = 'black'
    print(f"New value received for topic {topic}: {value}")

# Create an MQTT client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

# Set the MQTT callback function
client.on_message = on_message

# Connect to the MQTT broker
client.connect(mqtt_broker)
print("Connected to MQTT broker")

# Subscribe to the MQTT topics
for topic in mqtt_topics:
    client.subscribe(topic)
    print(f"Subscribed to topic: {topic}")

# Start the MQTT loop
client.loop_start()

# Run the Tkinter event loop
window.mainloop()
