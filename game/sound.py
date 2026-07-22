import pygame
 
import settings as cfg
 
 
class SoundManager:
    """ Loads and plays all game sounds, and handles the mute toggle. """
 
    def __init__(self) -> None:
        pygame.mixer.init()
        self.muted = False
 
        self.sounds = {
            "hit": pygame.mixer.Sound(str(cfg.ASSETS_DIR / "hit.mp3")),
            "bonus": pygame.mixer.Sound(str(cfg.ASSETS_DIR / "bonus.mp3")),
            "laser": pygame.mixer.Sound(str(cfg.ASSETS_DIR / "laser.mp3")),
        }
 
        pygame.mixer.music.load(str(cfg.ASSETS_DIR / "music.mp3"))
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)  # -1 = loop forever
 
    def play(self, name: str) -> None:
        """ Plays a sound effect by name, unless muted. """
        if not self.muted and name in self.sounds:
            self.sounds[name].play()
 
    def toggle_mute(self) -> None:
        """ Mutes/unmutes both sound effects and background music. """
        self.muted = not self.muted
        pygame.mixer.music.set_volume(0 if self.muted else 0.4)
 