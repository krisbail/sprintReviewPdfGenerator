import curses
import os


def clear_terminal():
    """
    Call the platform specific function to clear the terminal: cls on windows, reset otherwise
    """
    os.system('reset')

class testCurses:

    def __init__(self):
        self.title ="test"
        self.subtitle = "coucouc"

    def clear_screen(self):
        """
        Clear the screen belonging to this menu
        """
        self.screen.clear()

    def main_loop(self, stdscr=None):
        print "main loop"
        self.stdscr = stdscr if not None else curses.initscr()
        self.screen = curses.newpad(10 + 6, self.stdscr.getmaxyx()[1])

        self._set_up_colors()
        curses.curs_set(0)
        self.stdscr.refresh()
        self.draw()

    def _set_up_colors(self):
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        self.highlight = curses.color_pair(1)
        self.normal = curses.A_NORMAL

    def draw(self):
        self.screen.border(0)
        if self.title is not None:
            self.screen.addstr(2, 2, self.title, curses.A_STANDOUT)
        if self.subtitle is not None:
            self.screen.addstr(4, 2, self.subtitle, curses.A_BOLD)

        screen_rows, screen_cols = self.stdscr.getmaxyx()
        top_row = 0
        self.screen.refresh(top_row, 0, 0, 0, screen_rows - 1, screen_cols - 1)

    def show(self):
        #self.main_loop()
        curses.wrapper(self.main_loop)

        self.clear_screen()
        clear_terminal()

def t():

    pad = curses.newpad(10, 10)
    #  These loops fill the pad with letters; this is
    # explained in the next section
    for y in range(0, 100):
        for x in range(0, 100):
            try:
                pad.addch(y, x, ord('a') + (x * x + y * y) % 26)
            except curses.error:
                pass

    # Displays a section of the pad in the middle of the screen
    pad.refresh(0, 0, 5, 5, 20, 75)

'''
test = testCurses()
test.show()
test.stdscr.getch()
'''
st=curses.initscr()
t()
st.getch()

