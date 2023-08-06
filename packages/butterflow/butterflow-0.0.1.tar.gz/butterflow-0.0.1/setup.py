import re

from pathlib import Path
from textwrap import dedent
from typing import List

from setuptools import (
    find_packages,
    setup,
)

import butterflow as root


def read_requirements(file: str) -> List[str]:
    if not Path(file).is_file():
        raise FileNotFoundError(file)
    with open(file) as fd:
        unparsed_requirements = fd.read()
        return re.findall(r"[\w-]+==[\d.]+", unparsed_requirements)

setup_params = dict(
    name='butterflow',

    version=root.__version__,

    description='Python project',

    long_description=dedent("""
        The boilerplate Python project that aims to create facility for maintaining of the package
        easily. It considering tools for building, testing and distribution.
        """).strip(),
    long_description_content_type='text/markdown',
    author='Kristian Boda',
    author_email='kristian.boda@babylonhealth.com',
    url='https://john.doe.org',

    classifiers=["Programming Language :: Python :: 3"],
    license='MIT',
    keywords=[],

    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,

    entry_points={
        'console_scripts': [
            'butterflow = butterflow.__main__:main',
        ]
    },

    install_requires=read_requirements('requirements.txt'),
    extras_require={},
    setup_requires=[
        'wheel',
    ],
    tests_require=read_requirements('requirements-test.txt')
)


def main() -> None:
    setup(**setup_params)


if __name__ == '__main__':
    main()
