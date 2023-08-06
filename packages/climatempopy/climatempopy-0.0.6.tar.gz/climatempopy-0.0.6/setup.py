import setuptools
from pathlib import Path

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="climatempopy", 
    version="0.0.6",
    scripts=["bin/get_weather_georeferenced","bin/get_weather_by_localeID","bin/get_localeID"],
    author="Antonio Campos",
    author_email="tonyldo@gmail.com",
    description="A Clima Tempo API Python Wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tonyldo/climatempopy",
    packages=setuptools.find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        l.strip() for l in Path('requirements.txt').read_text('utf-8').splitlines()
    ],
)