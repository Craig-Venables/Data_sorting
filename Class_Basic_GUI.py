import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys
import io

class SimpleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple GUI with Terminal and Matplotlib")

        # Create a text widget for the terminal-like interface
        self.terminal = tk.Text(root, height=10)
        self.terminal.pack(fill=tk.BOTH, expand=True)
        sys.stdout = TextRedirector(self.terminal, "stdout")  # Redirect stdout
        sys.stderr = TextRedirector(self.terminal, "stderr")  # Redirect stderr

        # Create an entry widget for user input
        self.input_entry = ttk.Entry(root)
        self.input_entry.pack(fill=tk.BOTH)
        self.input_entry.bind("<Return>", self.handle_input)

        # Create a matplotlib figure and embed it in the GUI
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        # Place a button to update the graph
        self.update_button = ttk.Button(root, text="Update Graph", command=self.update_graph)
        self.update_button.pack()

    def handle_input(self, event):
        input_text = self.input_entry.get()
        self.input_entry.delete(0, tk.END)
        self.terminal.insert(tk.END, f"\n> {input_text}\n")
        self.terminal.see(tk.END)  # Scroll to the end of the terminal

        # Execute the input_text or process it as needed
        # For this example, let's just echo the input back
        self.terminal.insert(tk.END, f"< {input_text}\n")
        self.terminal.see(tk.END)  # Scroll to the end of the terminal

    def update_graph(self):
        x = [1, 2, 3, 4, 5]
        y = [x_val**2 for x_val in x]
        self.ax.clear()
        self.ax.main_plot(x, y)
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_title("Simple Matplotlib Graph")
        self.canvas.draw()

class TextRedirector:
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str, (self.tag,))
        self.widget.configure(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    gui = SimpleGUI(root)
    root.mainloop()
