""" Run this to demonstrate the cc module's functionality.
    Demonstrates possibility of arbitrarily complex scenes through a 'simple' scene of texture-on-color-on-texture,
    and an fps counter.
"""
import math

import cc.colors as colors
from cc.image import Image
from cc.text import Text
from cc.window import Window

# Create window.
win = Window()

# Load any images or fonts just once.
rainbow_img = Image('pyproject/image/rainbow.png')
hazard_img = Image('pyproject/image/hazard.png')
pizza_img = Image('pyproject/image/pizza.png')
nova_flat_26 = Text.load_ttf_font('pyproject/res/NovaFlat.ttf', 26)

last_update_and_fps = [0.0, 0.0]
last_frame_time = win.get_time()
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

    # Layer 3: Semi-transparent gray box.
    gray_box_border = wx_twentieth
    win.drawRect(
        x=gray_box_border,
        y=gray_box_border,
        width=wx - (2 * gray_box_border),
        height=wy - (2 * gray_box_border),
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

    # FPS counter = 1/(time since last frame).
    cur_time = win.get_time()
    update_frequency_seconds = 0.25
    if int(cur_time) > 0 and (cur_time - last_update_and_fps[0] > update_frequency_seconds):
        dt = cur_time - last_frame_time
        last_update_and_fps[1] = 1 / dt
        last_update_and_fps[0] = cur_time
    fps_text = Text(text=f'FPS: {last_update_and_fps[1]:3.0f}', font=nova_flat_26, color=colors.DARK_GRAY)
    win.drawText(
        text=fps_text,
        x=wx - fps_text.width - gray_box_border,
        y=wy - fps_text.height - gray_box_border
    )
    last_frame_time = cur_time

    # Draw!
    win.update()
win.close()
