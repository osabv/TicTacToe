from random import choice

class TicTacToe:
    
    def __init__(self):
        """Initializes board game, and other central parts of the game."""
        self.board = ['-'] * 9
        self.free_spaces = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.move = 0
        self.player_marker = ''
        self.ai_marker = ''
        self.markers = {'X', 'O'}
        self.winning_rows = (
            [0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], 
            [0, 4, 8], [6, 4, 2])
        self.corners = [0, 2, 6, 8]
        self.edges = [1, 3, 5, 7]
        self.center = 5
        self.layout = """\n {} | {} | {}\n---+---+---\n {} | {} | {}\n---+---+---\n {} | {} | {}\n"""
        self.error = "\nOops! That was an invalid response. Please try again"
        
    def print_board(self, board=None):
        """Prints out the game board."""
        print(self.layout.format(*self.board))
    
    def get_marker(self):
        """Prompts the player to choose a marker, and returns users response."""
        marker = input("\nWould you like to be X or O?: ").upper()
        while marker not in self.markers:
            print(self.error)
            marker = input("\nWould you like to be X or O?: ").upper()
        self.player_marker = marker
        if self.player_marker == 'X':
            self.ai_marker = 'O'
        else:
            self.ai_marker = 'X'
        return marker
    
    def is_valid_response(self, response):
        """Checks if the given response is a valid response."""
        return (response in range(1, 10) and self.is_not_occupied(response))
    
    def get_user_response(self):
        """Propmts the user for a response, and returns the reponse."""
        response = input("\nWhere would you like to move? (1-9): ")
        while not response.isdigit():
            response = input("\nThat doesnt look like a number. Try again: ")
        while not self.is_valid_response(int(response)):
            print(self.error)
            response = input("\nWhere would you like to move? (1-9): ")
        return response
    
    def is_not_occupied(self, space):
        """Retruns True iff if space is not occupied, otherwise returns False."""
        if space in self.free_spaces:
            return True
        return False
    
    def game_board_full(self):
        """Returns True if game board is full, otherwise returns False."""
        return '-' not in self.board
    
    def make_move(self, marker, space):
        """Moves the marker to the desired space on the board"""
        self.free_spaces.remove(space)
        self.board[int(space) - 1] = marker
        if space - 1 in self.edges:
            self.edges.remove(space - 1)
        elif space - 1 in self.corners:
            self.corners.remove(space - 1)
        return self.board
    
    def game_won(self):
        """Returns True if the game has been won, otherwie returns False."""
        for row in self.winning_rows:
            if self.board[row[0]] != '-':
                if self.board[row[0]] == self.board[row[1]] == self.board[row[2]]:
                    return True
        return False
    
    def extract_row(self, row):
        """Returns a row from the board in its str format."""
        return self.board[row[0]] + self.board[row[1]] + self.board[row[2]]
    
    def opposite_corners(self):
        """Checks if the opposite corners are occupied by the opposite player."""
        return (self.board[0] == self.board[8] == self.player_marker) or\
               (self.board[2] == self.board[6] == self.player_marker)
    
    def winning_move(self):
        """Checks if the next move can be a winning move."""
        for row in self.winning_rows:
            str_row = self.extract_row(row)
            if str_row.count(self.ai_marker) == 2 and str_row.count('-') == 1:
                return row[str_row.index('-')] + 1 
        return None
    
    def block_player_move(self):
        """Blocks the opponenets winning move."""
        for row in self.winning_rows:
            str_row = self.extract_row(row)
            if str_row.count(self.player_marker) == 2 and str_row.count('-') == 1:
                return row[str_row.index('-')] + 1
        return None
        
    def best_move(self):
        """Checks for the next best move."""
        winning_move = self.winning_move()
        if winning_move:
            return winning_move
        block_player_move = self.block_player_move()
        if block_player_move:
            return block_player_move
        return None
    
    def ai_move_first(self):
        """Returns moves for the AI, should the AI go first."""
        if self.move == 1 or self.move == 3 or len(self.corners) == 1:
            return choice(self.corners) + 1
        elif self.is_not_occupied(self.center):
            return 5
        elif len(self.corners) != 0:
            return choice(self.corners) + 1
        else:
            return choice(self.edges) + 1
            
    def ai_move_second(self):
        """Returns moves for the AI, should the AI go second."""
        if self.is_not_occupied(self.center):
            return 5
        elif self.opposite_corners() is True or len(self.corners) == 0:
            return choice(self.edges) + 1
        else:
            return choice(self.corners) + 1
    
    def ai_move(self):
        """Initiates the AI's next move."""
        move = self.best_move()
        if move:
            return move
        else:
            if self.ai_marker == 'X':
                move = self.ai_move_first()
                return move
            elif self.ai_marker == 'O':
                move = self.ai_move_second()
                return move
            
    def start_game(self):
        """Starts the game."""
        self.get_marker()
        if self.player_marker == 'X':
            player = 'p'
        else:
            player = 'a'
        while not self.game_won() and self.move < 9:
            
            if player == 'p':
                self.print_board()
                self.move += 1
                move = self.get_user_response()
                self.make_move(self.player_marker, int(move))
                if self.game_won():
                    break
                player = 'a'
            else:
                player == 'a'
                self.move += 1
                move = self.ai_move()
                self.make_move(self.ai_marker, move)
                if self.game_won():
                    break
                player = 'p'
        self.end_game(player)
        
    def end_game(self, player):
        """Ends the game."""
        self.print_board()
        if self.game_won() is True:
            if player == 'p':
                print("\nCongratulations. You won.")
            elif player == 'a':
                print("\nHehe. I won.")
        else:
            print("\n'Twas a draw")
        another_game = input("\nWould you like to play again? (y/n): ")
        if another_game == 'y':
            tictactoe.__init__()
            tictactoe.start_game()
        else:
            print("\nThanks for playing. Have a nice day!")
            
if __name__ == "__main__":
    tictactoe = TicTacToe()
    tictactoe.start_game()
