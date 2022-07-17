from dataclasses import dataclass
from time import monotonic
from typing import Literal, Callable, Union

import ppb

from wrathjam import config
from wrathjam import controls
from wrathjam import events

DEBUG = config.DEBUG


@dataclass
class Attack:
    last_used: Union[float, int] = 0
    cool_down: Union[float, int] = 1
    tag: str = ""

    def __call__(self, player: 'Sprite', scene: ppb.Scene, signal_function: Callable[[type], None]) -> bool:
        if monotonic() <= self.last_used + self.cool_down:
            return False
        if DEBUG:
            print(f"{self.name} fired at wrath level {player.wrath_level}.")
        self.effect(player, scene, signal_function)
        self.last_used = monotonic()
        return True

    def effect(self, player: 'Sprite', scene: ppb.Scene, signal_function: Callable[[type], None]) -> None:
        pass

    @property
    def name(self):
        return f"Generic Attack {self.tag}"


class Punch(Attack):

    def effect(self, player: 'Sprite', scene: ppb.Scene, signal_function: Callable[[type], None]) -> None:
        pass

    @property
    def name(self):
        return "Punch"


class Sprite(ppb.Sprite):
    size = 1
    image = ppb.Circle(100, 175, 50)

    base_speed = 6
    wrath = 0
    debug_wrath_level: Literal[1, 2, 3] = 1
    primary_attacks: dict[Literal[1, 2, 3], Attack] = {
        1: Attack(tag="p1"),
        2: Attack(tag="p2"),
        3: Attack(tag="p3")
    }

    secondary_attacks: dict[Literal[1, 2, 3], Attack] = {
        1: Attack(tag="s1"),
        2: Attack(tag="s2"),
        3: Attack(tag="s3")
    }

    @property
    def speed(self):
        return self.base_speed

    def on_update(self, event, signal):
        control_state = event.controls
        attacked = False

        if not attacked and control_state[controls.PRIMARY_ATTACK]:
            attack = self.primary_attacks[self.wrath_level]
            attacked = attack(self, event, signal)
        if not attacked and control_state[controls.SECONDARY_ATTACK]:
            attack = self.secondary_attacks[self.wrath_level]
            attacked = attack(self, event, signal)
        self.move(event)

    def move(self, event):
        vertical = event.controls[controls.VERTICAL]
        horizontal = event.controls[controls.HORIZONTAL]
        control_direction = ppb.Vector(horizontal, vertical)
        if control_direction:
            control_direction = control_direction.normalize()
        self.position += control_direction * self.speed * event.time_delta

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
