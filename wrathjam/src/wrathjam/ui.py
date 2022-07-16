import ppb


class TextIndicator(ppb.RectangleSprite):
    image = None
    left_offset = 1
    top_offset = 1
    preferred_height = 1

    last_rendered = None
    font = ppb.Font("wrathjam/resources/EvilEmpire-4BBVK.ttf", size=64)
    color = (180, 180, 180)

    def on_pre_render(self, event, signal):
        message = self.message
        if message != self.last_rendered:
            self.image = ppb.Text(message, color=self.color, font=self.font)
            image = self.image.load().contents
            horizontal = image.w
            vertical = image.h
            self.height = self.preferred_height
            self.width = horizontal / vertical * self.height
            self.last_rendered = message
        camera = event.scene.main_camera
        self.left = camera.left + self.left_offset
        self.top = camera.top - self.top_offset

    @property
    def message(self):
        return "No message provided."


class WrathIndicator(TextIndicator):
    wrath = 0

    def on_wrath_changed(self, event, signal):
        wrath = event.wrath

    @property
    def message(self):
        return f"Wrath: {self.wrath}"


class WrathLevelIndicator(TextIndicator):
    wrath_level = 1

    def on_wrath_level_changed(self, event, signal):
        self.wrath_level = event.wrath_level

    @property
    def message(self):
        return f"Wrath Level: {self.wrath_level}"
