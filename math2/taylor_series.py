# https://gist.github.com/mick001/7c4741961a72d69f880d0c602c833fcf
import sympy as sy
import numpy as np
from sympy.functions import sin, cos, ln
import matplotlib.pyplot as plt

from tkinter import *

from PIL import ImageTk, Image

plt.style.use("ggplot")

def close_this_sht():
    plt.gcf()
    plt.clf()
    #plt.close()

# Factorial function
def factorial(n):
    if n <= 0:
        return 1
    else:
        return n * factorial(n - 1)


# Taylor approximation at x0 of the function 'function'
def taylor(function, x0, n, x=sy.Symbol('x')):
    i = 0
    p = 0
    while i <= n:
        p = p + (function.diff(x, i).subs(x, x0)) / (factorial(i)) * (x - x0) ** i
        i += 1
    return p


def plot(f, x0=0, n=9, by=2, x_lims=[-5, 5], y_lims=[-5, 5], npoints=800, x=sy.Symbol('x')):
    x1 = np.linspace(x_lims[0], x_lims[1], npoints)
    # Approximate up until n starting from 1 and using steps of by
    for j in range(1, n + 1, by):
        func = taylor(f, x0, j)
        taylor_lambda = sy.lambdify(x, func, "numpy")
        print('Taylor expansion at n=' + str(j), func)
        plt.plot(x1, taylor_lambda(x1), label='Order ' + str(j))
    # Plot the function to approximate (sine, in this case)
    func_lambda = sy.lambdify(x, f, "numpy")
    plt.plot(x1, func_lambda(x1), label='Function of x')

    plt.xlim(x_lims)
    plt.ylim(y_lims)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)
    plt.title('Taylor series approximation')
    plt.savefig("taylor.png")


def run():
    x = sy.Symbol('x')
    f = ln(10 + x)
    plot(f)

    imgx = 600
    imgy = 600
    root = Tk()
    root.title("Taylor series approximation")
    root.geometry('{}x{}'.format(imgx, imgy))

    exitb = Button(root, text="Exit", bd=12, relief="raised", command=lambda: [close_this_sht(), root.destroy()],
                   width=15)
    exitb.configure(bg="gray", fg="white", font="Calibri 9 bold")
    exitb.pack(padx=10, pady=30)

    imgName = "taylor.png"
    canvas = Canvas(root, width=imgx, height=imgy)
    canvas.pack()
    img = ImageTk.PhotoImage(Image.open(imgName), master=root)
    canvas.create_image(0, 0, anchor=NW, image=img)

    for event in root.event.get():
        if event.type == root.QUIT:
            root.destroy()

    root.mainloop()


run()
