from typing import Literal

import ppb

from wrathjam import config
from wrathjam import controls
from wrathjam import damage
from wrathjam import events

DEBUG = config.DEBUG


class Sprite(ppb.Sprite):
    size = 1
    image = ppb.Circle(100, 175, 50)

    base_speed = 6
    wrath = 0
    debug_wrath_level: Literal[1, 2, 3] = 1
    primary_attacks: dict[Literal[1, 2, 3], damage.Attack] = {
        1: damage.Punch(),
        2: damage.Kick(),
        3: damage.RapidFire(-26, 26, 2),
    }

    secondary_attacks: dict[Literal[1, 2, 3], damage.Attack] = {
        1: damage.Attack(),
        2: damage.Attack(),
        3: damage.Attack(),
    }

    @property
    def speed(self):
        return self.base_speed

    def on_update(self, event, signal):
        control_state = event.controls
        attacked = False

        if not attacked and control_state[controls.PRIMARY_ATTACK]:
            attack = self.primary_attacks[self.wrath_level]
            attacked = attack(self, event.scene, signal)
        if not attacked and control_state[controls.SECONDARY_ATTACK]:
            attack = self.secondary_attacks[self.wrath_level]
            attacked = attack(self, event.scene, signal)
        self.move(event)

    def move(self, event):
        vertical = event.controls[controls.VERTICAL]
        horizontal = event.controls[controls.HORIZONTAL]
        control_direction = ppb.Vector(horizontal, vertical)
        if control_direction:
            control_direction = control_direction.normalize()
        self.position += control_direction * self.speed * event.time_delta

    def on_mouse_motion(self, event: ppb.events.MouseMotion, signal):
        direction = event.position - self.position
        if direction:
            direction = direction.normalize()
            self.facing = direction

    @property
    def wrath_level(self) -> Literal[1, 2, 3]:
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
