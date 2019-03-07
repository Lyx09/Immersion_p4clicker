# Amélie BERTIN

"""
    An example of a game: a window and some Buttons and Label
"""

from tkinter import *


class Game:
    """
    The Class of the game.
    It contains all the methods used by the game.
    """

    def __init__(self):
        """
        The initiation function, it is called at the beginning
        """

        # Create the window of the game
        self.__window = Tk()
        # Give it a name
        self.__window.title("Game example")
        self.__dimY = 6

        # Display Text: Which player has to play
        self.__turnLabel = Label(self.__window, text="TEXT: Voici votre jeu :D")

        # Button to Start a new game
        self.__restart_button = Button(self.__window, text="New Game",
                                       command=self.init_layout, width=9)
        # Button to Stop the application
        self.__stop_button = Button(self.__window, text="Stop",
                                    command=self.__window.destroy, width=9)

        # Init the layout
        self.init_layout()

    def init_layout(self):
        # place all labels and buttons on the window: ONLY FOR GOOD DISPLAY
        self.__turnLabel.grid(row=1, column=3, columnspan=2)
        self.__restart_button.grid(row=self.__dimY + 1, column=3,
                                   sticky=W + E)
        self.__stop_button.grid(row=self.__dimY + 1, column=4,
                                sticky=W + E)

    def start(self):
        """
        The function called outside the class
        """
        self.__window.mainloop()


def main():
    """
    Main program:
    Create the object game and play
    """
    ui = Game()
    ui.start()

# execute the main function
main()