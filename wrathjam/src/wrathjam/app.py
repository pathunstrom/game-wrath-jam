"""
A top down shooter about using your anger.
"""

import os
import sys

try:
    from importlib import metadata as importlib_metadata
except ImportError:
    # Backwards compatibility - importlib.metadata was added in Python 3.8
    import importlib_metadata

import ppb
import pathunstrom_splash as splash

from wrathjam.scenes import main_menu
from wrathjam.systems import controller
from wrathjam import controls


def main():
    # Linux desktop environments use app's .desktop file to integrate the app
    # to their application menus. The .desktop file of this app will include
    # StartupWMClass key, set to app's formal name, which helps associate
    # app's windows to its menu item.
    #
    # For association to work any windows of the app must have WMCLASS
    # property set to match the value set in app's desktop file. For PPB this
    # is set using environment variable.

    # Find the name of the module that was used to start the app
    app_module = sys.modules["__main__"].__package__
    # Retrieve the app's metadata
    metadata = importlib_metadata.metadata(app_module)

    os.environ["SDL_VIDEO_X11_WMCLASS"] = metadata["Formal-Name"]

    ppb.run(
        starting_scene=splash.Splash(next_scene=main_menu.Scene),
        title="Wrath Jam",
        resolution=(1600, 900),
        systems=[controller.ControllerSystem],
        inputs=controls.inputs,
    )
