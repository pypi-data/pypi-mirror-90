import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="distanceconverter",
    version="1.0",
    author="TheFlyingRat",
    author_email="joeyspp50@gmail.com",
    description="Convert time, distance and speed",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheFlyingRat/DistanceConverter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.0',
)