from setuptools import setup, find_packages

with open("README.md", mode="r", encoding="utf-8") as fh:
    readme = fh.read()

setup(
        name="ccivr",
        version="0.1.0",
        license="MIT license",
        author="Maya Suzuki",
        author_email="ohhata@hama-med.ac.jp",
        description="Extract cisNats from RNA-seq data",
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
        python_requires='>=3.8',
    )