from time import monotonic

import ppb

from wrathjam import config, utils


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
            self.grow_time = self.grow_time if self.grow_time is not None else self.life_span
            self._grow_start_time = self._spawn_time + self.grow_start
            self._grow_end_time = self._grow_start_time + self.grow_time

    def on_update(self, event, signal):
        now = monotonic()
        run_time = now - self._spawn_time
        if run_time >= self.life_span:
            event.scene.remove(self)

        # move
        if self.final_position is not None:
            normalized_run_time = utils.clamp_normal(run_time / (self._end_time - self._spawn_time))
            assert 0 <= normalized_run_time <= 1, "Normalized Run time outside of range."
            t = self.movement_ease(normalized_run_time)
            self.position = (t * (self.final_position - self._start_position)) + self._start_position

        if self.grow_end is not None:
            grow_run_time = now - self._grow_start_time
            grow_time = utils.clamp_normal(grow_run_time / (self._grow_end_time - self._grow_start_time))
            assert 0 <= grow_time <= 1, "Growth time outside of range."
            t = self.growth_ease(grow_time)
            self.size = (t * (self.grow_end - self._starting_size)) + self._starting_size

    def on_pre_render(self, event, signal):
        if self.image is None and config.DEBUG:
            self.image = ppb.Square(200, 50, 50)
