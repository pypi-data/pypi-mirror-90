"""
USAGE:
   o install in develop mode: navigate to the folder containing this file,
                              and type 'pip install -e . --user'.
                              (omit '--user' if you want to install for
                               all users)
"""
from setuptools import setup

setup(name='track-tools',
      version='0.0.5',
      description='Collection of scripts and wrappers around trackpy.',
      url='https://gitlab.gwdg.de/ikuhlem/track-tools',
      author=['Ilyas Kuhlemann'],
      author_email='ikuhlem@gwdg.de',
      license='GPLv3',
      packages=["track_tools",
                "track_tools.cli"],
      entry_points={
          "console_scripts": [
              'track-tools-extract-trajectories=track_tools.cli.extract_trajectories:main',
              'track-tools-drift-correction=track_tools.cli.drift_correction:main'
          ],
          "gui_scripts": [
          ]
      },
      install_requires=['matplotlib', 'trackpy', 'pims', 'pillow',
                        'numba', 'pandas', 'scikit-image'],
      zip_safe=False)
