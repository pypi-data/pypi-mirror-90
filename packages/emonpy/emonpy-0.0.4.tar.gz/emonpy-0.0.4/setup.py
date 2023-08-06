import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="emonpy",
    version="0.0.4",
    author="Jack",
    author_email="jack@gmail.com",
    description="Python library for the eMon Energy device",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/emonindonesai/emonpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "httpx==0.16.1"
    ],
    python_requires='>=3.8',
)