class NoSolutionException(Exception):
    """Custom exception for no solution."""
    pass


class KnightsTourPuzzle:
    """Class that handles playing Knights Tour Puzzle game in console. With x, y dimensions defined."""
    def __init__(self, x, y):
        self.mat_x_dim = x
        self.mat_y_dim = y
        self.dimension = self.mat_x_dim * self.mat_y_dim
        self.empty_sqr = len(str(self.dimension)) * "_"
        self.occupied_position = (len(str(self.dimension)) - 1) * ' ' + "X"
        self.ex_position = (len(str(self.dimension)) - 1) * " " + "*"
        self.sqr_length = len(self.empty_sqr)
        self.field = [[self.empty_sqr for _ in range(self.mat_x_dim)] for _ in range(self.mat_y_dim)]
        self.copy_field = [[self.empty_sqr for _ in range(self.mat_x_dim)] for _ in range(self.mat_y_dim)]
        self.moves = []

    def field_print(self, field):

        """Prints game field, from back to the beginning of the chessboard."""

        max_length = len((str(self.mat_y_dim) + '| ' + ' '.join(field[-1]) + ' |'))
        border = ((self.mat_x_dim * (self.sqr_length + 1) + 3) * "-")
        print(border.rjust(max_length))
        for i in range(self.mat_y_dim, 0, -1):
            print((str(i) + '| ' + ' '.join(field[i - 1]) + ' |').rjust(max_length))
        print(border.rjust(max_length))
        print(" ".join(str(i).rjust(self.sqr_length) for i in range(1, self.mat_x_dim + 1)).rjust(max_length - 2))

    @staticmethod
    def input_dimensions():

        """
        Subprogram that take user input and checks it,according to properties:
        If the board's dimensions contain non-integer numbers print Invalid dimensions!.
        If the board's dimensions contain more than 2 numbers print Invalid dimensions!.
        If the board's dimensions contain negative numbers print Invalid dimensions!.
        If invalid dimensions were provided by the user,
        ask them for valid dimensions again after outputting Invalid dimensions!
        """

        while True:
            try:
                f_row, f_col = [int(i) for i in input("Enter your board dimensions:").split()]
                if f_row <= 0 or f_col <= 0:
                    raise ValueError
                else:
                    return f_row, f_col
            except ValueError:
                print("Invalid dimensions")

    def input_position(self):

        """
        Subprogram that take user input and checks it,according to properties:
        If the user input contains non-integer numbers you should print Invalid position!.
        If the user input contains more than 2 numbers you should print Invalid position!.
        If the user input numbers out of bounds of the game field you should print Invalid position!.
        """

        while True:
            try:
                x, y = [int(i) for i in input("Enter the knight's starting position:").split()]
                if not all((1 <= x <= self.mat_x_dim, 1 <= y <= self.mat_y_dim)):
                    raise ValueError
                else:
                    return x - 1, y - 1
            except ValueError:
                print("Invalid position!")

    def make_move(self, x, y):
    
        """Makes move on the board with coordinates (x, y) ."""
        
        self.field[y][x] = self.occupied_position
        self.moves.append([x, y])

    def possible_moves_calc(self, x, y):
    
        """This method calculates possible moves for (x, y) position and returns list of them."""
        
        all_possible_moves = [[x - 2, y + 1],
                              [x - 2, y - 1],
                              [x + 2, y - 1],
                              [x + 2, y + 1],
                              [x - 1, y + 2],
                              [x + 1, y + 2],
                              [x - 1, y - 2],
                              [x + 1, y - 2]]

        possible_moves = []
        for move in all_possible_moves:
            in_matrix = 0 <= move[0] < self.mat_x_dim and 0 <= move[1] < self.mat_y_dim
            if in_matrix and self.field[move[1]][move[0]] != self.ex_position:
                possible_moves.append(tuple(move))
        return possible_moves

    def pos_moves_position(self, moves: list):
    
        """This method calculates numbers of possible moves for moves in list. 
        And than takes this numbers to coordinates from moves list."""
        
        coord_dict = {}
        for move in moves:
            coord_dict[move] = self.possible_moves_calc(move[0], move[1])

        for move, moves_lst in coord_dict.items():
            possible_move = str(len(moves_lst) - 1).rjust(len(self.empty_sqr))
            x = move[0]
            y = move[1]
            self.field[y][x] = possible_move

    def field_cleaner(self):
    
        """This metod cleans gameboard from occupied position with X to *, 
        and from numbers of possible moves to empth square."""
        
        for i in range(self.mat_x_dim):
            for j in range(self.mat_y_dim):
                if self.field[j][i] == self.occupied_position:
                    self.field[j][i] = self.ex_position
                elif self.field[j][i][self.sqr_length - 1].isdigit():
                    self.field[j][i] = self.empty_sqr

    def move_checker(self, x, y):
    
        """This method checks (x, y) coordinates that knight was in this position,
        that this coordinates in dimensions of out gameboard,
        and that our move was made from our last position."""
        
        last_x = self.moves[-1][0]
        last_y = self.moves[-1][1]
        moves = self.possible_moves_calc(last_x, last_y)
        if self.field[y - 1][x - 1] == self.ex_position:
            raise AttributeError
        elif not all((1 <= x <= self.mat_x_dim, 1 <= y <= self.mat_y_dim)):
            raise AttributeError
        elif (x - 1, y - 1) not in moves:
            raise AttributeError

    def stars_counter(self):
    
        """Counts how many moves was made on the gameboard"""
        
        c = 0
        for i in range(self.mat_x_dim):
            for j in range(self.mat_y_dim):
                if self.field[j][i] == self.ex_position:
                    c += 1
        return c

    def next_move(self):
    
        """This method takes part of the game to inputing moves."""
        
        while True:
            self.field_cleaner()
            print("Enter your next move:", end="")
            x, y = [int(i) for i in input().split()]
            try:
                star_num = self.stars_counter()
                if star_num == (self.dimension - 1):
                    self.field_print(self.field)
                    print("What a great tour! Congratulations!")
                    break
                self.move_checker(x, y)
                self.make_move(x - 1, y - 1)
                poss_moves = self.possible_moves_calc(x - 1, y - 1)
                if len(poss_moves) == 0:
                    self.field_print(self.field)
                    print("No more possible moves!")
                    print(f"Your knight visited {len(self.moves)} squares!")
                    break
                self.pos_moves_position(poss_moves)
                self.field_print(self.field)
            except AttributeError:
                print("Invalid move!", end='')
                continue

    def validate(self, x, y):
    
        """This method validates (x, y) coordinates beeing in dimensions range 
        and being empty for our solver."""
        
        val_lst = [y < self.mat_y_dim, y >= 0,
                   x >= 0, x < self.mat_x_dim]
        if all(val_lst) and self.copy_field[y][x] == self.empty_sqr:
            return True

    def solve(self, x, y, counter):
        
        """This method solves Knights Tour Puzzle putting numbers 
        from move to move to the copy of our gameboard. If solution exists this method return True, else False."""

        move_x = [2, 1, -1, -2, -2, -1, 1, 2]
        move_y = [1, 2, 2, 1, -1, -2, -2, -1]

        if counter >= self.dimension + 1:
            return True

        for i in range(8):
            new_x = x + move_x[i]
            new_y = y + move_y[i]
            if self.validate(new_x, new_y):
                self.copy_field[new_y][new_x] = str(counter).rjust(len(self.empty_sqr))
                if self.solve(new_x, new_y, counter + 1):
                    return True
                else:
                    self.copy_field[new_y][new_x] = self.empty_sqr
        return False

    def solver(self, x, y, marker=None):
    
        """This method points first move to the copy of our gameboard. And then 
        if the game have solution and marker was "n" prints it, else raise exception No Solution"""
        
        self.copy_field[y][x] = "1".rjust(len(self.empty_sqr))
        if not self.solve(x, y, 2):
            raise NoSolutionException
        elif marker == "n":
            print("\n", "Here's the solution!")
            self.field_print(self.copy_field)

    @staticmethod
    def option():
        
        """This is a part of user interface wants from player to choose him playing game or not."""
        
        while True:
            ans = input("Do you want to try the puzzle? (y/n):")
            if ans not in ["y", "n"]:
                print("Invalid option, try again!")
                continue
            else:
                return ans


def main():
    a, b = KnightsTourPuzzle.input_dimensions()    # inputs and checks for correctness dimensions of gameboard
    new_game = KnightsTourPuzzle(a, b)             # creates gameboard
    move_x, move_y = new_game.input_position()     # inputs and check first position
    option = new_game.option()                     # gives player option to play game or discard
    try:
        if option == "y":                          
            new_game.solver(move_x, move_y)        # solving the game, if game have no solution raise error else continue playing
            new_game.make_move(move_x, move_y)     # making first move
            pos_moves_lst = new_game.possible_moves_calc(move_x, move_y) # calculating possible moves for first move
            new_game.pos_moves_position(pos_moves_lst)                 # mapping possible moves to the gameboard
            new_game.field_print(new_game.field)                       # printing gamefield
            new_game.next_move()                                       # handling players' other moves
        elif option == "n":
            new_game.solver(move_x, move_y, option)                    # solving the game and printing solution, raising error if it not exsist
    except NoSolutionException:
        print("No solution exists!")               # print if solution of the game not exsist 


if __name__ == '__main__':
    main()
