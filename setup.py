from setuptools import setup, find_packages

from ccivr import __version__

with open("README.md", mode="r", encoding="utf-8") as fh:
    readme = fh.read()

setup(
        name="ccivr",
        version=__version__,
        license="MIT license",
        author="Maya Suzuki / Tatsuya Ohhata",
        author_email="ohhata@hama-med.ac.jp",
        description="Identification of total cis-NATs based on genome annotation",
        long_description=readme,
        long_description_content_type="text/markdown",
        url="https://github.com/CCIVR/ccivr.git",
        packages=find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent"
        ],
        install_requires=['pandas'],
        entry_points={
            "console_scripts":[
                "ccivr = ccivr.ccivr:main"
            ]
        },
    )
