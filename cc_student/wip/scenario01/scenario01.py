""" The main file to be run to display the scenario. """
from cc.window import Window
from cc_student.wip.scenario01.skeleton.handler import Handler
from cc_student.wip.scenario01.solution import Solution

level = Solution.get_level().name
win_title = "%s Scenario 1: Space Cat Pizza Party!" % level
window = Window(win_title=win_title)
window.toggle_maximized()
window.hide_cursor()

handler = Handler(window)

while window.is_open():
    handler.update()
    window.update()
window.close()
exit(0)
