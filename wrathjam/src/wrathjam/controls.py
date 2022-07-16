from ppb import buttons, keycodes

from wrathjam import events
from wrathjam.systems import controller

HORIZONTAL = "horizontal"
VERTICAL = "vertical"
PRIMARY_ATTACK = "primary_attack"
SECONDARY_ATTACK = "secondary_attack"

DEBUG_ADD_WRATH_LEVEL = "add_wrath"
DEBUG_REMOVE_WRATH_LEVEL = "remove_wrath"

inputs = [
            controller.MomentarySwitch(PRIMARY_ATTACK, buttons.Primary),
            controller.MomentarySwitch(SECONDARY_ATTACK, buttons.Secondary),
            controller.ButtonAxis(HORIZONTAL, keycodes.A, keycodes.D),
            controller.ButtonAxis(VERTICAL, keycodes.S, keycodes.W),
            controller.FireEvent(DEBUG_ADD_WRATH_LEVEL, keycodes.BracketRight, events.AddWrathLevel),
            controller.FireEvent(DEBUG_REMOVE_WRATH_LEVEL, keycodes.BracketLeft, events.RemoveWrathLevel)
        ]
