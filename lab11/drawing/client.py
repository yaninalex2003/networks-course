import socket
import tkinter as tk

DEST_ADDR= ('::1', 50001)

class DrawingClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        self.sock.connect(DEST_ADDR)

        self.root = tk.Tk()
        self.root.title("Я на клиенте")
        self.canvas = tk.Canvas(self.root, width=500, height=500)
        self.canvas.pack()

        self.last_x = None
        self.last_y = None

        self.canvas.bind("<ButtonPress-1>", self.save_posn)
        self.canvas.bind("<B1-Motion>", self.add_line)
        self.root.protocol("WM_DELETE_WINDOW", self.delete_window)
        self.root.mainloop()

    def save_posn(self, event):
        self.last_x = event.x
        self.last_y = event.y

    def add_line(self, event):
        x, y = event.x, event.y
        self.canvas.create_line(self.last_x, self.last_y, x, y)
        data = f"{self.last_x},{self.last_y},{x},{y}\n"
        print(f"Client: I sent {data}")
        self.sock.sendall(data.encode())
        self.last_x = x
        self.last_y = y

    def delete_window(self):
        self.sock.close()
        self.root.destroy()

if __name__ == "__main__":
    DrawingClient()
