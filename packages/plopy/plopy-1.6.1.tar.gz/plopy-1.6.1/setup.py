import setuptools

with open("./plopy/README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="plopy",
    version="1.6.1",
    author="Finnventor",
    description="GUI for matplotlib graphing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Finnventor/plopy",
    packages=setuptools.find_packages(),
    package_data={'plopy': ['*.txt', '*.png']},
    install_requires=['matplotlib', 'PySide2'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent"
    ]
)
