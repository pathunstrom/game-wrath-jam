import ppb

from wrathjam import controls
from wrathjam import events


DEBUG = True


class Sprite(ppb.Sprite):
    size = 1
    image = ppb.Circle(100, 175, 50)

    base_speed = 6
    wrath = 0
    debug_wrath_level = 1

    @property
    def speed(self):
        return self.base_speed

    def on_update(self, event, signal):
        control_state = event.controls
        if control_state[controls.PRIMARY_ATTACK] or control_state[controls.SECONDARY_ATTACK]:
            pass
        else:
            self.move(event)

    def move(self, event):
        vertical = event.controls[controls.VERTICAL]
        horizontal = event.controls[controls.HORIZONTAL]
        control_direction = ppb.Vector(horizontal, vertical)
        if control_direction:
            control_direction = control_direction.normalize()
        self.position += control_direction * self.speed * event.time_delta

    @property
    def wrath_level(self):
        if DEBUG:
            return self.debug_wrath_level
        else:
            return 1

    def on_add_wrath_level(self, event, signal):
        if self.debug_wrath_level < 3:
            self.debug_wrath_level += 1
            signal(events.WrathLevelChanged(self.wrath_level))

    def on_remove_wrath_level(self, event, signal):
        if self.debug_wrath_level > 1:
            self.debug_wrath_level -= 1
            signal(events.WrathLevelChanged(self.wrath_level))
