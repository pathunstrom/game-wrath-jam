from random import randrange
from time import monotonic
from typing import Callable, Union

import ppb

from wrathjam import config, utils

DEBUG = config.DEBUG


class Attack:
    last_used: Union[float, int] = 0
    cool_down: Union[float, int] = 1

    def __call__(
        self,
        source: ppb.Sprite,
        scene: ppb.Scene,
        signal_function: Callable[[type], None],
        tags: list = None,
    ) -> bool:
        now = monotonic()
        if now <= self.last_used + self.cool_down:
            return False
        if DEBUG:
            print(f"{self.name} fired at {now}.")
        self.initiate(source, scene, signal_function)
        self.last_used = now
        return True

    def initiate(
        self,
        source: ppb.Sprite,
        scene: ppb.Scene,
        signal_function: Callable[[type], None],
    ) -> None:
        pass

    def apply(
        self, hit: ppb.Sprite, scene: ppb.Scene, signal_function: Callable[[type], None]
    ) -> None:
        pass

    def end(self):
        pass

    @property
    def name(self):
        return type(self).__name__


class Punch(Attack):
    cool_down = 0.75

    def initiate(
        self,
        source: ppb.Sprite,
        scene: ppb.Scene,
        signal_function: Callable[[type], None],
    ) -> None:
        scene.add(
            Hurtbox(
                final_position=source.position + (source.facing * 1),
                life_span=0.30,
                position=source.position + (source.facing * 0.5),
                size=0.5,
                grow_end=1.5,
            )
        )


class Kick(Attack):
    cool_down = 0.4

    def initiate(
        self,
        source: ppb.Sprite,
        scene: ppb.Scene,
        signal_function: Callable[[type], None],
    ) -> None:
        scene.add(
            Hurtbox(
                final_position=source.position + (source.facing * 3),
                life_span=0.3,
                position=source.position + (source.facing * 0.5),
                size=1,
                source=source,
                attack=self,
            )
        )


class RapidFire(Attack):
    cool_down = 0.12

    def __init__(self, min, max, step):
        self.min = min
        self.max = max
        self.step = step

    def initiate(
        self,
        source: ppb.Sprite,
        scene: ppb.Scene,
        signal_function: Callable[[type], None],
    ) -> None:
        drifted_rotation: ppb.Vector = source.facing.rotate(self.random_degrees())
        scene.add(
            Hurtbox(
                final_position=source.position + (drifted_rotation * 8),
                position=source.position + (source.facing * 0.5),
                life_span=0.6,
                size=0.5,
                grow_end=0.6,
            )
        )

    def random_degrees(self):
        return randrange(self.min, self.max, self.step)


class Hurtbox(ppb.Sprite):
    image = None
    life_span = 0.25
    final_position = None
    movement_ease = utils.smoother_step
    grow_end = None
    grow_start = 0
    grow_time = None
    growth_ease = utils.smoother_step
    layer = -1
    attack = None
    source = None

    _spawn_time = None
    _end_time = None
    _starting_size = None
    _start_position = None
    _grow_start_time = None
    _grow_end_time = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._spawn_time = monotonic()
        self._end_time = self._spawn_time + self.life_span
        self._starting_size = self.size
        self._start_position = self.position
        if self.grow_end is not None:
            self.grow_time = (
                self.grow_time if self.grow_time is not None else self.life_span
            )
            self._grow_start_time = self._spawn_time + self.grow_start
            self._grow_end_time = self._grow_start_time + self.grow_time

    def on_update(self, event, signal):
        now = monotonic()
        run_time = now - self._spawn_time
        if run_time >= self.life_span:
            event.scene.remove(self)

        # move
        if self.final_position is not None:
            normalized_run_time = utils.clamp_normal(
                run_time / (self._end_time - self._spawn_time)
            )
            assert (
                0 <= normalized_run_time <= 1
            ), "Normalized Run time outside of range."
            t = self.movement_ease(normalized_run_time)
            self.position = (
                t * (self.final_position - self._start_position)
            ) + self._start_position

        if self.grow_end is not None:
            grow_run_time = now - self._grow_start_time
            grow_time = utils.clamp_normal(
                grow_run_time / (self._grow_end_time - self._grow_start_time)
            )
            assert 0 <= grow_time <= 1, "Growth time outside of range."
            t = self.growth_ease(grow_time)
            self.size = (
                t * (self.grow_end - self._starting_size)
            ) + self._starting_size

    def on_pre_render(self, event, signal):
        if self.image is None and config.DEBUG:
            self.image = ppb.Square(200, 50, 50)
