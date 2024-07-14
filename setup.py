import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="EdgeCollectionsEditor",
    version="0.0.1",
    author="AdamantLife",
    author_email="contact.adamantmedia@gmail.com",
    description="Python Utilities and GUI for managing Edge Collections",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AdamantLife/EdgeCollectionsEditor",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    install_requires=[
        
    ],
    python_requires=">=3.8",
    packages=setuptools.find_packages()
)