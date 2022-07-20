from random import randrange, gauss
from time import monotonic
from typing import Literal, Callable, Union

import ppb

from wrathjam import config
from wrathjam import controls
from wrathjam import damage
from wrathjam import events

DEBUG = config.DEBUG


class Attack:
    last_used: Union[float, int] = 0
    cool_down: Union[float, int] = 1

    def __call__(self, player: 'Sprite', scene: ppb.Scene, signal_function: Callable[[type], None]) -> bool:
        now = monotonic()
        if now <= self.last_used + self.cool_down:
            return False
        if DEBUG:
            print(f"{self.name} fired at wrath level {player.wrath_level} at {now}.")
        self.effect(player, scene, signal_function)
        self.last_used = now
        return True

    def effect(self, player: 'Sprite', scene: ppb.Scene, signal_function: Callable[[type], None]) -> None:
        pass

    @property
    def name(self):
        return type(self).__name__


class Punch(Attack):
    cool_down = 0.75

    def effect(self, player: 'Sprite', scene: ppb.Scene, signal_function: Callable[[type], None]) -> None:
        scene.add(
            damage.Hurtbox(
                final_position=player.position + (player.facing * 1),
                life_span=0.30,
                position=player.position + (player.facing * 0.5),
                size=.5,
                grow_end=1.5
            )
        )


class Kick(Attack):
    cool_down = 0.4

    def effect(self, player: 'Sprite', scene: ppb.Scene, signal_function: Callable[[type], None]) -> None:
        scene.add(
            damage.Hurtbox(
                final_position=player.position + (player.facing * 3),
                life_span=0.3,
                position=player.position + (player.facing * 0.5),
                size=1
            )
        )


class RapidFire(Attack):
    cool_down = 0.12

    def effect(self, player: 'Sprite', scene: ppb.Scene, signal_function: Callable[[type], None]) -> None:
        drifted_rotation: ppb.Vector = player.facing.rotate(self.random_degrees())
        scene.add(
            damage.Hurtbox(
                final_position=player.position + (drifted_rotation * 8),
                position=player.position + (player.facing * 0.5),
                life_span=0.6,
                size=0.5,
                grow_end=0.6
            )
        )

    def random_degrees(self):
        return randrange(-26, 26, 2)


class Sprite(ppb.Sprite):
    size = 1
    image = ppb.Circle(100, 175, 50)

    base_speed = 6
    wrath = 0
    debug_wrath_level: Literal[1, 2, 3] = 1
    primary_attacks: dict[Literal[1, 2, 3], Attack] = {
        1: Punch(),
        2: Kick(),
        3: RapidFire()
    }

    secondary_attacks: dict[Literal[1, 2, 3], Attack] = {
        1: Attack(),
        2: Attack(),
        3: Attack()
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
