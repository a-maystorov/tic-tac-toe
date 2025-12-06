import sys

import pygame

from ai import AI
from button import Button
from grid import Grid
from message import Message
from settings import Settings


class Game:
    """Overall class to manage game assets and behaviour."""

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Tic Tac Toe")

        self.grid = Grid(self)
        self.ai = None  # Will be created when PvAI mode is selected
        self.winner = None
        self.game_result_msg = None

        # Game mode: None (start screen), "PVP", or "PVAI"
        self.game_mode = None

        # Buttons
        self.pvp_button = Button(
            self,
            "Player vs Player",
            center=(
                self.settings.screen_width / 2,
                self.settings.screen_height / 2 - 40,
            ),
        )
        self.pvai_button = Button(
            self,
            "Player vs AI",
            center=(
                self.settings.screen_width / 2,
                self.settings.screen_height / 2 + 40,
            ),
        )
        self.play_again_button = Button(
            self,
            "Play again",
            center=(
                self.settings.screen_width / 2,
                self.settings.screen_height / 2 + 40,
            ),
        )

        # Start at the menu screen
        self.game_active = False

    def _check_start_buttons(self, mouse_pos):
        """Check if player clicked a game mode button."""
        if self.pvp_button.rect.collidepoint(mouse_pos):
            self.game_mode = "PVP"
            self.game_active = True
            self.grid.reset()
            self.ai = None
        elif self.pvai_button.rect.collidepoint(mouse_pos):
            self.game_mode = "PVAI"
            self.game_active = True
            self.grid.reset()
            self.ai = AI(self.grid, symbol="O")  # AI plays as O

    def _check_play_again_button(self, mouse_pos):
        """Return to start screen when player clicks Play Again."""
        if self.play_again_button.rect.collidepoint(mouse_pos):
            self.game_mode = None  # Back to start screen
            self.game_active = False
            self.grid.reset()
            self.ai = None
            self.winner = None
            self.game_result_msg = None

    def _check_mouse_button_down_events(self, event):
        """Respond to mouse button presses."""
        mouse_pos = event.pos

        # If on start screen, check menu buttons
        if self.game_mode is None:
            self._check_start_buttons(mouse_pos)
        # If game is over, check play again button
        elif not self.game_active:
            self._check_play_again_button(mouse_pos)
        # If game is active, update grid
        else:
            self.grid.update(mouse_pos)

            # Check for winner after player's move (BEFORE AI moves)
            self._check_winner()

            # If playing against AI, it's O's turn, and game is still active, let AI play
            if (
                self.game_mode == "PVAI"
                and self.grid.current_turn == "O"
                and self.game_active
                and self.ai
            ):
                self.ai.make_move()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_mouse_button_down_events(event)

    def _check_winner(self):
        """Check if a player has won or not and display the proper message."""
        if not self.game_active:
            return

        winner = self.grid.check_winner()
        if winner:
            self.winner = winner
            winner_text = (
                f"Player {self.winner} wins!"
                if self.game_mode == "PVP"
                else ("You win!" if winner == "X" else "AI wins!")
            )
            self.game_result_msg = Message(
                self,
                winner_text,
                center=(
                    self.settings.screen_width / 2,
                    self.settings.screen_height / 2 - 60,
                ),
            )
            self.game_active = False
        elif self.grid.is_full() and not winner:
            self.game_result_msg = Message(
                self,
                "It's a tie!",
                center=(
                    self.settings.screen_width / 2,
                    self.settings.screen_height / 2 - 60,
                ),
            )
            self.game_active = False

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)

        if self.game_mode is None:
            # Draw start screen
            title = Message(
                self,
                "Tic Tac Toe",
                font_size=64,
                center=(
                    self.settings.screen_width / 2,
                    self.settings.screen_height / 2 - 100,
                ),
            )
            title.draw()
            self.pvp_button.draw()
            self.pvai_button.draw()
        elif self.game_active:
            # Draw active game
            self.grid.draw()
        else:
            # Draw game over screen
            if self.game_result_msg:
                self.game_result_msg.draw()
            self.play_again_button.draw()

        pygame.display.flip()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self._check_winner()  # Check again in main loop in case AI just moved
            self._update_screen()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run_game()
