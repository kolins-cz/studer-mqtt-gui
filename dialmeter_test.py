import tkinter
from tkdial import Meter


def main():
    root = tkinter.Tk()
    dial = Meter(root,start=-4, end=4,radius=300, major_divisions=1, minor_divisions=0.1,scale_color="black", needle_color="red")
    dial.set(-2.5)
    dial.pack(padx=10, pady=10)
    root.mainloop()

if __name__ == "__main__":
    main()