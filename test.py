import tkinter as tk

def on_button_click():
    print("Button clicked!")

# Create the main window
root = tk.Tk()
root.title("Simple Tkinter Script")

# Create a button and attach the on_button_click function to it
button = tk.Button(root, text="Click Me!", command=on_button_click)
button.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
