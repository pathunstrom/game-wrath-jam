import ppb

from wrathjam import player


class Scene(ppb.Scene):
    background_color = (0, 0, 0)
    camera_set = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.add(player.Sprite())

    def on_pre_render(self, event, signal):
        if not self.camera_set:
            self.main_camera.width = 50
            self.camera_set = True
