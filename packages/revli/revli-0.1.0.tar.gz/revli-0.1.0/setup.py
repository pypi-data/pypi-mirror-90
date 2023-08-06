import setuptools
import os


def get_data_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        path = path.split(os.path.sep, 1)[-1]
        for filename in filenames:
            paths.append(os.path.join(path, filename))
    return paths


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="revli",
    version="0.1.0",
    author="Akida31",
    description="revli is a cli tool to create reveal.js presentations and manage their plugins",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Akida31/revli",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={"": get_data_files(os.path.join("revli", "data"))},
    python_requires='>=3.8',
    install_requires=["beautifulsoup4", "chompjs"],
    entry_points={"console_scripts": [
        "revli = revli.cli:main"
    ]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Graphics :: Presentation"
    ]
)
