# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['omnigraffle_stencil']

package_data = \
{'': ['*'], 'omnigraffle_stencil': ['templates/*']}

install_requires = \
['PyPDF2==1.26.0', 'cairosvg==2.4.2']

entry_points = \
{'console_scripts': ['omnigraffle-stencil = '
                     'omnigraffle_stencil.converter:main']}

setup_kwargs = {
    'name': 'omnigraffle-stencil',
    'version': '1.1.0',
    'description': 'Tool to create OmniGraffle stencils from SVG icons',
    'long_description': '# OmniGraffle Stencil generator\n\nTool to create [OmniGraffle](https://www.omnigroup.com/omnigraffle/)\nstencils from SVG icons.\n\nFeatures:\n\n- create multiple sheets by directory\n- parametrize object magnets\n- filter images and format icon names\n\nIdea based on script from\n[AWS-OmniGraffle-Stencils](https://github.com/davidfsmith/AWS-OmniGraffle-Stencils/)\n\n## Usage\n\nRequires Python 3.8+.\n\nInstall:\n\n```bash\npip3 install omnigraffle-stencil\n```\n\nRun:\n\n```bash\nomnigraffle-stencil --help\n```\n\nto see all options:\n\n```\nusage: omnigraffle-stencil [-h] [--svg-dir SVG_DIR] [--stencil-file STENCIL_FILE] [--filename-includes [FILENAME_INCLUDES [FILENAME_INCLUDES ...]]] [--filename-excludes [FILENAME_EXCLUDES [FILENAME_EXCLUDES ...]]]\n                           [--stencil-name-remove [STENCIL_NAME_REMOVE [STENCIL_NAME_REMOVE ...]]] [--no-vertex-magnets] [--side-magnets SIDE_MAGNETS] [--text-output]\n\nConvert SVG files into OmniGraffle stencil\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --svg-dir SVG_DIR     svg files directory path (default: ./svg)\n  --stencil-file STENCIL_FILE\n                        name of output stencil file (default: output.gstencil)\n  --filename-includes [FILENAME_INCLUDES [FILENAME_INCLUDES ...]]\n                        strings to filter image file name by, taking only those which contains them all\n  --filename-excludes [FILENAME_EXCLUDES [FILENAME_EXCLUDES ...]]\n                        strings to filter image file name by, taking only those which do not contain any of them\n  --stencil-name-remove [STENCIL_NAME_REMOVE [STENCIL_NAME_REMOVE ...]]\n                        strings to be removed from image file name when creating stencil name (default: . - _)\n  --no-vertex-magnets   don\'t create magnets on vertices (NE, NW, SE, SW)\n  --side-magnets SIDE_MAGNETS\n                        number of magnets for each side (default: 5)\n  --text-output         write OmniGraffle data file as text instead of binary\n```\n\nInput files are taken from the given location (`./svg` by default)\nand should be grouped into directories.\nEvery directory will be parsed to a separate canvas in output stencil.\n\nSVG directories structure example:\n\n```\nsvg/\n├── Group 1/\n│   ├── icon1.svg\n│   ├── icon2.svg\n│   ├── icon3.svg\n└── Group 2/\n    ├── icon4.svg\n    └── icon5.svg\n```\n\n### AWS Architecture Icons example\n\nTo generate icons from\n[AWS Architecture Icons](https://aws.amazon.com/architecture/icons/)\ndownload SVG zip file\n(example: [AWS-Architecture-Assets-For-Light-and-Dark-BG_20200911](https://d1.awsstatic.com/webteam/architecture-icons/Q32020/AWS-Architecture-Assets-For-Light-and-Dark-BG_20200911.478ff05b80f909792f7853b1a28de8e28eac67f4.zip))\nand unpack it.\n\nRun script with options:\n\n```bash\nomnigraffle-stencil \\\n    --svg-dir "AWS-Architecture-Assets-For-Light-and-Dark-BG_20200911/AWS-Architecture-Service-Icons_20200911" \\\n    --stencil-file AWS_20200911_Services.gstencil \\\n    --filename-includes _48 \\\n    --stencil-name-remove Arch_ _48 . - _ \\\n    --group-name-remove Arch_ . - _\n```\n\nOutput stencil will be created as `AWS_20200911_Services.gstencil`.\n\nCheck out the [AWS stencil in Stenciltown](https://stenciltown.omnigroup.com/stencils/aws-2020-09-11-all/) -\nit contains all Service and Resource icons.\n\n## Development\n\nRequires Python 3.8+ and [Poetry](https://python-poetry.org/).\n\nInstall dependencies in virtual env:\n\n```bash\npoetry shell\npoetry install\n```\n\nTroubleshooting installing `pillow` library on MacOS:\nhttps://akrabat.com/installing-pillow-on-macos-10-15-calatalina/\n\nGet virtual env path for the IDE:\n\n```bash\npoetry env info -p\n```\n\nRun script:\n\n```bash\npoetry run omnigraffle-stencil\n```\n\n## Publishing\n\nBuild and publish package:\n\n```bash\npoetry build\npoetry publish\n```\n',
    'author': 'Maciej Radzikowski',
    'author_email': 'maciej@radzikowski.com.pl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/m-radzikowski/omnigraffle-stencil',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
