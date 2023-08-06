# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['h6']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'pyserial>=3.5,<4.0']

entry_points = \
{'console_scripts': ['h6 = h6.cli:send_command']}

setup_kwargs = {
    'name': 'h6',
    'version': '0.1.1',
    'description': 'A Python library to emulate a Zoom H6 recorder remote control',
    'long_description': '# H6\n\nA Python library to emulate a Zoom H6 recorder remote control\n\n## Introduction\n\nThis library allows you to control your Zoom H6 recorder from your computer using an USB to TTL adapter.\nFor this, you will need a few components to make a specific cable, but it\'s quite simple.\n\n## Cable\n\nYou will have to make a specific cable that connects a USB port from your computer to the Zoom H6 remote control port, but fear not. It\'s actually really simple.\n\nYou will need:\n\n- An FTDI USB to TTL converter:\n\n![FTDI USB to TTL](images/FT232RL-FTDI-USB-to-TTL.jpeg?raw=true "FTDI USB to TTL")\n\n- A 2.5mm jack screw terminal:\n\n![2.5mm jack screw terminal](images/2-5mm-Stereo-Jack.jpeg?raw=true "2.5mm jack screw terminal")\n\n- A simple 3 wire cable\n\nAll of these components are widely available to buy online and the overall cost is less than 5€.\n\nOnce you have all of the components, the wiring is also quite simple:\n\n| FTDI adapter | 2.5mm jack |\n|--------------|------------|\n| Rx           | L          |\n| Tx           | R          |\n| GND          | V          |\n\n![Wiring](images/wiring.jpeg?raw=true "Wiring")\n\n**IMPORTANT**: Make sure that the FTDI USB to TTL adapter jumper is set to **3.3v** before using the cable. Leaving it at 5v could damage your recorder.\n\n## Installation\n\nSimply install the library using `pip`:\n\n`pip install h6`\n\n## Usage\n\nYou can include this library in your Python project or run it directly as a CLI tool.\n\n### CLI\n\nTo execute commands using your command line run:\n\n`h6 -p /dev/cu.usbserial-alcdut1 -c stop`\n\nYou must specify the serial port using `-p` or `--port` and the command to send using `-c` or `--command`.\n\n### Importing the library\n\nUsage example:\n\n``` python\nfrom h6 import ZoomH6\nfrom time import sleep\n\n# Define the serial port\nserial_port = \'/dev/cu.usbserial-alcdut1\'\n\n# Instantiate recorder\nrecorder = ZoomH6(serial_port)\n\n# Initialize recorder\nrecorder.initialize()\n\n# Send \'rec\' command\nrecorder.send(\'record\')\n\n# wait for a while\nsleep(3)\n\n# Send \'stop\' command\nrecorder.send(\'stop\')\n```\n\nAs you can see, when instantiating the ZoomH6 class you will need to specify the serial port where your FTDI USB to TTL adapter is connected.\n\nThe `initialize()` function executes a specific handshake expected by the Zoom H6 recorder in order to accept incoming commands.\n\nYou can send any valid command to the recorder. Keep reading for a list with all the available commands.\n\n## Commands\n\nThe complete list of available commands is:\n\n| Command           | Button            |\n|-------------------|-------------------|\n| play_pause        | Play / Pause      |\n| stop              | Stop              |\n| record            | Record            |\n| forward           | Forward           |\n| reverse           | Reverse           |\n| vol_up            | Increase volume   |\n| vol_down          | Decrease volume   |\n| ch1               | Toggle Channel 1  |\n| ch2               | Toggle Channel 2  |\n| ch3               | Toggle Channel 3  |\n| ch4               | Toggle Channel 4  |\n| chr               | Toggle R Channel  |\n| chl               | Toggle L Channel  |\n\n## Compatibility\n\nThis library has only been tested with the **H6** model, but according to the Zoom support (see [#1](https://github.com/mattogodoy/h6/issues/1)) it should work with other models such as the **H4n** and the **H5**.\n\nIf you get to try with any other model than the **H6**, please write your experience in that issue\'s comments.\n\n## Changelog\n\n- **0.1.1**:\n  - Added 3 seconds timeout to avoid infinite handshake\n  - Improved the way commands are sent\n  - Renamed L and R channels commands for consistency\n  - Improved error handling\n  - Updated README file\n  - Bumped version to 0.1.1\n\n- **0.1.0**\n  - Initial release\n',
    'author': 'Matias Godoy',
    'author_email': 'mattogodoy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mattogodoy/h6/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
