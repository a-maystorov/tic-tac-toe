import pygame.font


class Button:
    def __init__(
        self,
        game,
        msg,
        width=200,
        height=50,
        bg_color=(200, 200, 200),
        text_color=(255, 255, 255),
        font_size=48,
    ):
        """Initialize button attributes."""
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        # Set the dimensions and properties of the button.
        self.width, self.height = width, height
        self.bg_color = bg_color
        self.text_color = text_color
        self.font = pygame.font.SysFont(None, font_size)

        # Build the button's rect object and center it.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # The button message needs to be prepped only once.
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_color, self.bg_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw(self):
        # Draw blank button and then draw message.
        self.screen.fill(self.bg_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
