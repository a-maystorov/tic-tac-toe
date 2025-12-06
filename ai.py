import random


class AI:
    """A simple AI opponent for Tic Tac Toe."""

    def __init__(self, grid, symbol="O"):
        """Initialize the AI with a reference to the grid."""
        self.grid = grid
        self.symbol = symbol
        self.opponent_symbol = "X" if symbol == "O" else "O"
        self.first_move = True  # Track if this is AI's first move

    def make_move(self):
        """
        Make the AI's move using a simple strategy.

        Strategy priority:
        1. On first move: pick a random position
        2. Try to win
        3. Block opponent from winning
        4. Take center if available
        5. Take any available cell
        """
        # First move: random position
        if self.first_move:
            self.first_move = False
            self._make_random_move()
            return

        # Try to win
        move = self._find_winning_move(self.symbol)
        if move:
            self._place_move(move)
            return

        # Block opponent
        move = self._find_winning_move(self.opponent_symbol)
        if move:
            self._place_move(move)
            return

        # Take center if available
        if self.grid.cells[1][1] is None:
            self._place_move((1, 1))
            return

        # Take any available cell
        for row in range(3):
            for col in range(3):
                if self.grid.cells[row][col] is None:
                    self._place_move((row, col))
                    return

    def _make_random_move(self):
        """Make a random move on an empty cell."""
        available_moves = []
        for row in range(3):
            for col in range(3):
                if self.grid.cells[row][col] is None:
                    available_moves.append((row, col))

        if available_moves:
            move = random.choice(available_moves)
            self._place_move(move)

    def _find_winning_move(self, player):
        """
        Find if a player can win in the next move.

        Returns (row, col) tuple if winning move exists, None otherwise.

        How it works:
        - Try placing the player's symbol in each empty cell
        - Check if that placement creates a winning combination
        - If yes, return that position
        - If no, undo and try the next cell
        """
        for row in range(3):
            for col in range(3):
                if self.grid.cells[row][col] is None:
                    # Temporarily place the player's symbol
                    self.grid.cells[row][col] = player

                    # Check if this creates a win
                    is_winning = self.grid.check_winner() == player

                    # Undo the temporary placement
                    self.grid.cells[row][col] = None

                    if is_winning:
                        return (row, col)

        return None

    def _place_move(self, move):
        """Place the AI's symbol at the given position and switch turns."""
        row, col = move
        self.grid.cells[row][col] = self.symbol
        self.grid.current_turn = self.opponent_symbol
