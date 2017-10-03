from random import choice

class TicTacToe:
    
    winning_rows = (
            [0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], 
            [0, 4, 8], [6, 4, 2])
    
    error = "\nOops! That was an invalid response. Please try again"
    
    board_layout = """\n {} | {} | {}\n---+---+---\n {} | {} | {}\n---+---+---\n {} | {} | {}\n"""
    
    
    def __init__(self, board=None, player_marker=None):
        if board:
            self.board = board
        else:
            self.board = ['-'] * 9
            
        if player_marker:
            self.player_marker = player_marker
        else:
            self.player_marker = self.get_marker()
        
        self.ai_marker = switch_marker(self.player_marker)
            
    def print_board(self, board=None):
        print(self.board_layout.format(*self.board))
        
    def get_marker(self):
        marker = input("\nWould you like to be X or O?: ").upper()
        while marker not in {'X', 'O'}:
            print(self.error)
            marker = input("\nWould you like to be X or O?: ").upper()
        return marker
    
    def empty_spaces(self):
        return [k for k, v in enumerate(self.board, 1) if v == '-']
    
    def is_valid(self, response):
        return response in range(1, 10) and response in self.empty_spaces()
    
    def make_move(self, space, marker):
        self.board[space-1] = marker
        
    def is_complete(self):
        if '-' not in self.board or self.winner() != None:
            return True
        else:
            return False
        
    def winner(self):
        for row in self.winning_rows:
            if self.board[row[0]] != '-':
                if self.board[row[0]] == self.board[row[1]] == self.board[row[2]]:
                    return self.board[row[0]]
        return None

        
    def minmax(self, node, player):
        if node.is_complete():
            if node.winner() == node.ai_marker:
                return 1
            elif node.winner() == None:
                return 0
            else:
                return -1
            
        best = -2
        for space in node.empty_spaces():
            node.make_move(space, player)
            val = self.minmax(node, switch_marker(player))
            node.make_move(space, '-')
            
            if player == node.ai_marker:
                #if val > best:
                    #best = val
                best = max(val, best)
            else:
                #if val < best:
                    #best = val
                best = min(val, best)
                    
            return best
        
def switch_marker(marker):
    if marker == 'X':
        return 'O'
    else:
        return 'X'

def get_move(board, player):
    base = -2
    choices = []
    for space in board.empty_spaces():
        board.make_move(space, player)
        val = board.minmax(board, switch_marker(player))
        board.make_move(space, '-')
        
        if val > base:
            base = val
            choices = [space]
        elif val == base:
            choices.append(space)
    return choice(choices)
    
        
            
        
if __name__ == "__main__":
    board = TicTacToe()
    board.print_board()
    
    
    while not board.is_complete():
        player_move = input("pick: ")
        board.make_move(int(player_move), board.player_marker)
        board.print_board()
        
        if board.is_complete():
            break
        computer_move = get_move(board, board.ai_marker)
        board.make_move(computer_move, board.ai_marker)
        board.print_board()
    print("game over")
