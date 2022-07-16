from dataclasses import dataclass

import ppb

@dataclass
class AddWrathLevel:
    scene: ppb.Scene = None


@dataclass
class RemoveWrathLevel:
    scene: ppb.Scene = None


@dataclass
class WrathLevelChanged:
    wrath_level: int
    scene: ppb.Scene = None


@dataclass
class WrathChanged:
    wrath: int
    scene: ppb.Scene = None
