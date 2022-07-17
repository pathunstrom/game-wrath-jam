from time import monotonic

import ppb

from wrathjam import config, utils


class Hitbox(ppb.Sprite):
    image = None
    life_span = 0.25
    final_position = ppb.Vector(0, 0)
    movement_ease = utils.linear
    grow_end = 2
    grow_start = 0
    grow_time = 0
    growth_ease = utils.linear

    _spawn_time = None
    _end_time = None
    _starting_size = None
    _start_position = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._spawn_time = monotonic()
        self._end_time = self._spawn_time + self.life_span
        self._starting_size = self.size
        self._start_position = self.position

    def on_update(self, event, signal):
        run_time = monotonic() - self._spawn_time
        if run_time >= self.life_span:
            event.scene.remove(self)
        normalized_run_time = run_time / (self._end_time - self._spawn_time)

    def on_pre_render(self, event, signal):
        if self.image is None and config.DEBUG:
            self.image = ppb.Square(200, 50, 50)
