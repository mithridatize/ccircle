""" Run this for an adhoc test to demonstrate cc module functionality.
    Demonstrates possibility of arbitrarily complex scenes through a 'simple' scene of texture-on-color-on-texture.
"""
import math

import cc.colors as colors
from cc.font import Font
from cc.image import Image
from cc.window import Window

# Create window.
win = Window()

# Load any images or fonts just once.
rainbow_img = Image('pyproject/image/rainbow.png')
hazard_img = Image('pyproject/image/hazard.png')
pizza_img = Image('pyproject/image/pizza.png')
nova_hello = Font('../res/NovaFlat.ttf', 'hello')

while win.is_open():
    win.clear(colors.DARK_GRAY)

    # Misc window info.
    wx, wy = win.get_size()
    cx, cy = wx / 2, wy / 2
    wx_fifth = int(wx / 5)
    wy_fifth = int(wy / 5)
    wx_twentieth = int(wx / 20)
    wy_twentieth = int(wy / 20)

    # Layer 1: Rainbow backdrop.
    win.drawImage(
        image=rainbow_img,
        x=0,
        y=0,
        width=wx,
        height=wy,
    )

    # Layer 2: Top-left: Static pizza.
    win.drawImage(
        image=pizza_img,
        x=wx_fifth,
        y=wx_fifth,
        width=wx_fifth,
        height=wy_fifth,
    )

    # Layer 3: Semi-transparent grey box.
    border = wx_twentieth
    win.drawRect(
        x=border,
        y=border,
        width=wx - (2 * border),
        height=wy - (2 * border),
        r=colors.GRAY.r, g=colors.GRAY.g, b=colors.GRAY.b, a=0.8
    )

    # Layer 4: Bottom-right: A circle that changes size over time.
    max_radius = wx_fifth
    radius = int(abs(max_radius * math.sin(win.get_time())))
    win.drawCircle(
        x=cx + wx_fifth,
        y=cy + wx_fifth,
        radius=radius,
        center_color=colors.BLUE20,
        outer_color=colors.RED,
    )

    # Top layer: Hazard triangle that moves with the mouse (cursor).
    mouse_pos = win.get_mouse_pos()
    mx, my = mouse_pos.x, mouse_pos.y
    win.drawImage(
        image=hazard_img,
        x=mx - (wx_twentieth / 2),
        y=my,
        width=wx_twentieth,
        height=wy_twentieth,
    )

    # Draw some text.
    win.drawImage(
        image=nova_hello,
        x=0,
        y=0,
        width=nova_hello.width,
        height=nova_hello.height,
    )

    # Draw!
    win.update()
win.close()
