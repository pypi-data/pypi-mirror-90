import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyhut",
    version="0.1.3",
    author="thunder4lpha",
    description="Package for Minehut Minecraft server API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thunder4lpha/pyhut",
    packages=['pyhut'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)