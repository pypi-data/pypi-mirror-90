# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bumblebee',
 'bumblebee.bases',
 'bumblebee.datasets',
 'bumblebee.effects',
 'bumblebee.managers',
 'bumblebee.misc',
 'bumblebee.sources']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.19.0,<2.0.0', 'opencv-python>=4.4.0,<5.0.0']

entry_points = \
{'console_scripts': ['hi = hello:hello']}

setup_kwargs = {
    'name': 'eyecu-bumblebee',
    'version': '0.4.1',
    'description': 'Advanced pipelines for video datasets',
    'long_description': '# Bumblebee\n[![PyPI](https://img.shields.io/pypi/v/eyecu_bumblebee.svg)](https://pypi.python.org/pypi/eyecu_bumblebee)\n[![Downloads](http://pepy.tech/badge/eyecu_bumblebee)](https://pepy.tech/project/eyecu_bumblebee) \\\n![Bumblebee image](./docs/bumblebee.png)\n\nBumblebee provides high level components to construct training pipelines for videos conveniently.\n\n\n- [Install](#install)\n- [Motivation](#motto)\n- [Our Websites](#our-websites)\n- [Examples](#examples)\n    - [A Pipeline with basic elements](#a-pipeline-with-basic-elements)\n    - [Using Manager API](#using-manager-api)\n    - [Read Limited Section of Video](#read--limited-section-of-video)\n- [Team](#team)\n- [License](#license)\n\n\n\n## Install\n\n```\npip install eyecu_bumblebee\n```\n\n## Motivation\n\nEverything should be made as simple as possible, but no simpler. - Albert Einstein\n\n## Our Websites\n\n[EyeCU Vision](https://eyecuvision.com/) \\\n[EyeCU Future](https://eyecufuture.com/) \n\n\n## Examples\n\n### A pipeline with basic elements\n\n```python\nfrom bumblebee import *\n\n\nif __name__ == "__main__":\n    \n    VIDEO_PATH = "/path/to/video.mp4"\n\n    # Create a source\n    file_stream = sources.FileStream(VIDEO_PATH)\n\n    # Add an effect\n    goto = effects.GoTo(file_stream)\n\n    END_OF_VIDEO = file_stream.get_duration()\n    goto(END_OF_VIDEO)\n\n    # Create a dataset\n    single_frame = datasets.SingleFrame(file_stream)\n\n    last_frame = single_frame.read()\n\n```\n\n### Using Manager API\n\n```python\nfrom bumblebee import *\n\n\nif __name__ == "__main__":\n    \n    # Create a training manager\n    manager = managers.BinaryClassification(\n        ["path/to/video_dir","path/to/another_dir"],\n        ["path/to/labels"]\n    )\n\n    number_of_epochs = 300\n    \n    for epoch,(frame_no,frame,prob) in manager(number_of_epochs):\n        # Use data stuff\n        ...    \n\n```\n\n\n### Read  limited section of video\n```python\nfrom bumblebee import *\nfrom\nif __name__ == "__main__":\n  \n    VIDEO_PATH = "/path/to/video.mp4"\n    start_frame = 35\n    end_frame = 40\n    \n    file_stream = sources.FileStream(VIDEO_PATH)\n    \n    limited_stream = effects.Start(file_stream,start_frame)\n    limited_stream = effects.End(limited_stream,end_frame)\n\n    single_frame = datasets.SingleFrame(file_stream)\n\n    for frame in single_frame:\n        ...  \n\n```\n\n## Team\nThis project is currently developed and maintained by [ovuruska](https://github.com/ovuruska).\n\n\n## License\nBumblebee has MIT license. You can find further details in [LICENSE](LICENSE).\n\n',
    'author': 'Oguz Vuruskaner',
    'author_email': 'ovuruska@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Eye-C-U/bumblebee/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
