import ppb


class Scene(ppb.Scene):
    background_color = 200, 50, 50
    title_font = ppb.Font("wrathjam/resources/EvilEmpire-4BBVK.ttf", size=256)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add(
            ppb.Sprite(
                image=ppb.Text("WRATH", font=self.title_font, color=(14, 0, 51)), size=4
            )
        )

    def on_update(self, event, signal):
        for value in event.controls.values():
            if value:
                from wrathjam.scenes import sandbox

                signal(ppb.events.StartScene(sandbox.Scene()))
