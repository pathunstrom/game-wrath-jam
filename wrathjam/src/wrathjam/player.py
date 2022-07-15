import ppb

from wrathjam import controls


class Sprite(ppb.Sprite):
    size = 1
    image = ppb.Circle(100, 175, 50)

    base_speed = 6

    @property
    def speed(self):
        return self.base_speed

    def on_update(self, event, signal):
        control_direction = ppb.Vector(
            event.controls[controls.HORIZONTAL],
            event.controls[controls.VERTICAL]
        )
        if control_direction:
            control_direction = control_direction.normalize()
        self.position += control_direction * self.speed * event.time_delta
