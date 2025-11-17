import sys

import pygame

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
        self.winner = None
        self.game_result_msg = None
        self.play_again_button = Button(self, "Play again")

        # Start game in an inactive state.
        self.game_active = True

    def _check_play_again_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_again_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.game_active = True
            self.grid.reset()

    def _check_mouse_button_down_events(self, event):
        """Respond to mouse button presses."""
        mouse_pos = event.pos
        self.grid.update(mouse_pos)
        self._check_play_again_button(mouse_pos)

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_mouse_button_down_events(event)

    def _check_winner(self):
        """Check if a player has won or not and display the proper message."""
        winner = self.grid.check_winner()
        if winner:
            self.winner = winner
            self.game_result_msg = Message(
                self,
                f"Player {self.winner} wins!",
                center=(
                    self.settings.screen_width / 2,
                    self.settings.screen_height / 2 - 60,
                ),
            )
            self.game_active = False
        elif (
            self.grid.is_full() and not winner
        ):  # Check if all cells are filled and no winner
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

        if self.game_active:
            self.grid.draw()
        else:
            self.game_result_msg.draw()
            self.play_again_button.draw()

        pygame.display.flip()

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self._check_winner()
            self._update_screen()
            self.clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run_game()
