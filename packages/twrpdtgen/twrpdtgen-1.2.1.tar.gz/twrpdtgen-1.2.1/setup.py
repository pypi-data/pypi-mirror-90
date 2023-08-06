# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['twrpdtgen', 'twrpdtgen.info_extractors', 'twrpdtgen.utils']

package_data = \
{'': ['*'], 'twrpdtgen': ['templates/*']}

install_requires = \
['GitPython>=3.1.11,<4.0.0', 'Jinja2>=2.11.2,<3.0.0']

setup_kwargs = {
    'name': 'twrpdtgen',
    'version': '1.2.1',
    'description': 'TWRP Device Tree Generator. A script that generates a TWRP-compatible device tree.',
    'long_description': "# TWRP device tree generator\n\n[![PyPi version](https://img.shields.io/pypi/v/twrpdtgen)](https://pypi.org/project/twrpdtgen/)\n[![PyPi version status](https://img.shields.io/pypi/status/twrpdtgen)](https://pypi.org/project/twrpdtgen/)\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/ded3a853b48b44b298bc3f1c95772bfd)](https://www.codacy.com/gh/SebaUbuntu/TWRP-device-tree-generator/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=SebaUbuntu/TWRP-device-tree-generator&amp;utm_campaign=Badge_Grade)\n\nCreate a [TWRP](https://twrp.me/)-compatible device tree only from an Android recovery image (or a boot image if the device uses non-dynamic partitions A/B) of your device's stock ROM\nIt has been confirmed that this script supports images built starting from Android 4.4 up to Android 11\n\n## Installation\n\n```\npip install twrpdtgen\n```\nThe module is supported on Python 3.6 and above.\n\nLinux only: Be sure to have cpio installed in your system (Install cpio using `sudo apt install cpio` or `sudo pacman -S cpio` based on what package manager you're using)\n\n## How to use\n\n```\n$ twrpdtgen -h\nTWRP device tree generator\n\nusage: twrpdtgen [-h] [-o OUTPUT] [-v] [-k] recovery_image\n\npositional arguments:\n  recovery_image        path to a recovery image (or boot image if the device\n                        is A/B)\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -o OUTPUT, --output OUTPUT\n                        custom output folder\n  -v, --verbose         enable debugging logging\n  -k, --keep-aik        keep AIK after the generation\n```\n\nWhen an image is provided, if everything goes well, there will be a device tree at `output/manufacturer/codename`\n\nYou can also use the module in a script, with the following code:\n\n```python\nfrom twrpdtgen.twrp_dt_gen import generate_device_tree\n\n# The function will return a DeviceTree object, you can find its declaration here:\nfrom twrpdtgen.utils.device_tree import DeviceTree\n\nresult = generate_device_tree(image_path, output_path)\n\n```\n",
    'author': 'Sebastiano Barezzi',
    'author_email': 'barezzisebastiano@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SebaUbuntu/TWRP-device-tree-generator',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
