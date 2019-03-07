# Amélie BERTIN

"""
    A connect 4 game (scalable version of a project)
    The game consists of a grid (6x7) where two players put one coin
    by turn in a column by clicking on the button at top of the column.
    The coin falls to the bottom of the grid, or on top of a previous coin.
    When 4 coins are aligned (on a line, column or diagonal), the game ends.
    If nobody has won but the grid is filled, the game is draw.
    The player 1 has red color, the player 2 has yellow color.
    The players can resize the grid by entering integers in 2 entries
    and selecting "Set Dimensions" button
"""

from tkinter import *

# for player turn
PLAYER_1 = 1
PLAYER_2 = 2


class Connect4:
    """
    The Class of the game: Connect4.
    It contains all the methods used by the game.
    """

    def __init__(self):
        """
        The initiation function, it is called at the beginning
        """

        # Create the window of the game
        self.__window = Tk()
        # Give it a name
        self.__window.title("Connect 4")

        # Dimensions of the grid
        self.__dimX = 7
        self.__dimY = 6

        # The grid, a list which contains labels
        self.__grid = []

        # Colors of coins
        self.__colors = ['red', 'yellow']

        # Display Text: Which player has to play
        self.__turnLabel = Label(self.__window)
        # If there is an error (like add in a filled column), display the explanation
        self.__infoLabel = Label(self.__window)

        # Button to Start a new game
        self.__restart_button = Button(self.__window, text="New Game",
                                       command=self.init_layout, width=9)
        # Button to Stop the application
        self.__stop_button = Button(self.__window, text="Stop",
                                    command=self.__window.destroy, width=9)

        # List of Buttons (for adding a coin in a column)
        self.__columnButtons = []
        # For all columns
        for i in range(self.__dimX):
            # Create the button (with its number on it)
            button = Button(self.__window, text=str(i + 1), width=3)
            # Set its size
            button.config(borderwidth=2)
            # Set its appearance
            button.config(relief="groove")
            # Set the function called when it's pressed
            button.config(command=lambda t=i: self.put_coin(t))

            # Add it to the list of buttons
            self.__columnButtons.append(button)

        # Only for a good layout
        Label(self.__window, width=2).grid(row=0, column=0)
        self.layout_label = Label(self.__window, width=2)
        self.__end_button_label = Label(self.__window, width=2)

        # Init the layout
        self.init_layout()

    def init_layout(self):
        # place all labels and buttons on the window: ONLY FOR GOOD DISPLAY
        self.layout_label.grid(row=self.__dimY + 2, column=self.__dimX + 5)
        self.__end_button_label.grid(row=1, column=self.__dimX + 2)
        self.__turnLabel.grid(row=1, column=self.__dimX + 3, columnspan=2)
        self.__infoLabel.grid(row=2, column=self.__dimX + 3, columnspan=2)
        self.__restart_button.grid(row=self.__dimY + 1, column=self.__dimX + 3,
                                   sticky=W + E)
        self.__stop_button.grid(row=self.__dimY + 1, column=self.__dimX + 4,
                                sticky=W + E)

        # place buttons
        for i in range(len(self.__columnButtons)):
            self.__columnButtons[i].grid(row=1, column=i + 1)

        # Initialize the game
        self.initialize_game()

    def initialize_game(self):
        # Keep track of the player
        self.__turn = PLAYER_1

        # How many coins are in the grid
        self.__coins = 0

        # The grid : destroy old elements (cells of previous game)
        for label in self.__grid:
            label.destroy()

        # Initialize the grid
        self.__grid = []
        # For all lines
        for i in range(self.__dimY):
            # For all columns
            for j in range(self.__dimX):
                # Initialize a cell
                cell = Label(self.__window, bd=1)
                # Set its size and appearance
                cell.config(height=2, width=4, relief='solid')
                # Set its position in the window
                cell.grid(row=i + 2, column=j + 1)
                # Add it to the list (the grid)
                self.__grid.append(cell)

        # Set the starting text
        self.__infoLabel.config(text="Select a column to put a coin")

        self.update_text()

    def update_text(self):
        # Show which player can play
        self.__turnLabel.config(text="Player " + str(self.__turn) + " turn")

    def put_coin(self, column):
        """ add a coin in the grid
        column = int (the x-position in the grid) """

        # TODO
        # look from the bottom where it can be put
        row = self.__dimY - 1
        while row >= 0 and self.__grid[row * self.__dimX + column].cget('bg') \
                in self.__colors:
            row -= 1

        # if the column is full: do nothing: return
        if row < 0:
            # can't add coin
            self.__infoLabel.config(text="Can't add in this column")
            return

        # put color on the good cell
        self.__grid[row * self.__dimX + column] \
            .config(bg=self.__colors[self.__turn - 1])
        # add a coin to the total
        self.__coins += 1
        # TODO END

        # check if the game ends
        if self.__coins > 6:
            if self.game(column, row):
                return
        # end the player turn
        self.end_turn()

    def end_turn(self):
        # Change the player and show it
        self.__turn = 2 - self.__turn + 1
        self.update_text()
        self.__infoLabel.config(text="")

    def game(self, column, line):
        """ Check if the game is ended
        column = int (the x-position of the new coin in the grid)
        line = int (the y-position of the new coin in the grid)
        return bool : The game ends """

        # someone has won
        if self.check_column(column, line) or self.check_diagonal(column, line) \
                or self.check_line(column, line):
            self.__infoLabel.config(text="Player {0} wins !!".format(self.__turn))
            return True

        # the grid is filled
        if self.is_over():
            self.__infoLabel.config(text="The game is draw")
            return True

        return False

    def is_over(self):
        # Check if the grid is filled: check if the first line is full
        for i in range(self.__dimX):
            if not self.__grid[i].cget('bg') in self.__colors:
                return False

        return True

    def check_direction(self, column, line, direction_x, direction_y):
        # (not given)
        """ Count the number of coins in a direction after the player
            adds a coin
        column = int (the x-position of the new coin in the grid)
        line = int (the y-position of the new coin in the grid)
        directionX = int in [-1,1] (the x-direction where we check on the grid)
        directionY = int in [-1,1] (the x-direction where we check on the grid)
        return int (the number of player's coins in that direction)"""

        coins_player = 0
        while coins_player < 4 and column < self.__dimX and \
                line < self.__dimY and \
                self.__grid[line * self.__dimX + column].cget('bg') == \
                self.__colors[self.__turn - 1]:
            coins_player += 1
            column += direction_x
            line += direction_y
        return coins_player

    def check_column(self, column, line):
        # TODO
        """ Check if the player wins by adding a coin in this position
            in the column
        column = int (the x-position of the new coin in the grid)
        line = int (the y-position of the new coin in the grid)
        return bool (player wins)"""
        return self.check_direction(column, line, 0, 1) >= 4

    def check_line(self, column, line):
        # TODO
        """ Check if the player wins by adding a coin in this position
            in the line
        column = int (the x-position of the new coin in the grid)
        line = int (the y-position of the new coin in the grid)
        return bool (player wins)"""
        coins = self.check_direction(column, line, 1, 0)
        coins += self.check_direction(column, line, -1, 0) - 1
        return coins >= 4

    def check_diagonal(self, column, line):
        # TODO : BONUS
        """ Check if the player wins by adding a coin in this position
            by looking the two diagonals
        column = int (the x-position of the new coin in the grid)
        line = int (the y-position of the new coin in the grid)
        return bool (player wins)"""

        # Check first diagonal
        coins = self.check_direction(column, line, 1, 1)
        coins += self.check_direction(column, line, -1, -1) - 1
        # If 4 : win
        if coins >= 4:
            return True

        # Check second diagonal
        coins = self.check_direction(column, line, -1, 1)
        coins += self.check_direction(column, line, 1, -1) - 1
        return coins >= 4

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
    ui = Connect4()
    ui.start()

# execute the main function
main()