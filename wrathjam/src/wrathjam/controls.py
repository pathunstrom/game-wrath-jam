from ppb import buttons, keycodes

from wrathjam.systems import controller

HORIZONTAL = "horizontal"
VERTICAL = "vertical"
PRIMARY_ATTACK = "primary_attack"
SECONDARY_ATTACK = "secondary_attack"

inputs = [
            controller.MomentarySwitch(PRIMARY_ATTACK, buttons.Primary),
            controller.MomentarySwitch(SECONDARY_ATTACK, buttons.Secondary),
            controller.ButtonAxis(HORIZONTAL, keycodes.A, keycodes.D),
            controller.ButtonAxis(VERTICAL, keycodes.S, keycodes.W)
        ]