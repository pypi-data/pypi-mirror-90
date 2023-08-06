import ast
from pathlib import Path
import re
import setuptools
from typing import Dict


MODULE_NAME = 'mx-notes'
REPOSITORY_URL = 'https://github.com/amunger3/{:s}'.format(MODULE_NAME)
ENCODING = 'utf-8'
SRC_DIR = Path() / 'mx'

pkg_info = {} # type: Dict[str, str]


with open(SRC_DIR / '__version__.py') as f:
    exec(f.read(), pkg_info)

with open('README.md', encoding=ENCODING) as f:
    readme = f.read()

with open('CHANGELOG.md', encoding=ENCODING) as f:
    history = f.read()

with open(Path() / 'docs' / 'summary.txt', encoding=ENCODING) as f:
    summary = f.read().strip()

with open('requirements.txt') as f:
    install_requires = [l.replace('==','>=').strip() for l in f if l.strip()]


setuptools.setup(
    name=MODULE_NAME,
    version=pkg_info['__version__'],
    url='https://github.com/amunger3/mx-notes',
    author=pkg_info['__author__'],
    author_email=pkg_info['__email__'],
    description=summary,
    include_package_data=True,
    keywords=[
        'notes',
        'math',
        'mathjax',
        'tex',
        'latex',
        'browser',
    ],
    long_description='\n\n'.join((readme, history)),
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(exclude=['test*']),
    package_data={
        'mx': [
            'static/*',
            'templates/*.j2.html',
        ],
    },
    entry_points={
        'console_scripts':[
            'mx = mx.cli:run',
        ],
    },
    python_requires='>=3.8',
    install_requires=install_requires,
    license=pkg_info['__license__'],
    classifiers=[
        'Development Status :: 1 - Planning',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Text Editors',
        'Topic :: Text Processing :: Markup :: LaTeX',
    ]
)