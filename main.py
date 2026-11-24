import tkinter as tk
from interfaz.login import VentanaLogin


def main():
    root = tk.Tk()
    VentanaLogin(root)
    root.mainloop()


if __name__ == "__main__":
    main()