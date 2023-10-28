import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.background_music = None
        self.sound_effects = {}

    def load_background_music(self, file_path):
        pygame.mixer.music.load(file_path)
        self.background_music = file_path

    def play_background_music(self, loops=-1):
        if self.background_music:
            pygame.mixer.music.play(loops)

    def stop_background_music(self):
        pygame.mixer.music.stop()

    def load_sound_effect(self, name, file_path):
        sound_effect = pygame.mixer.Sound(file_path)
        self.sound_effects[name] = sound_effect

    def play_sound_effect(self, name):
        if name in self.sound_effects:
            self.sound_effects[name].play()
            
    def stop_sound_effect(self, name):
        if name in self.sound_effects:
            self.sound_effects[name].stop()
            
    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume / 100)
        for sound_effect in self.sound_effects.values():
            sound_effect.set_volume(volume / 100)
