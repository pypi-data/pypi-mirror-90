import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fick1d", # Replace with your own username
    packages = ['fick1d'],
    version="0.0.1",
    author="Kieran Nehil",
    author_email="nehilkieran@gmail.com",
    description="A small package for solving Fick's Second law in 1-dimension for various geometries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kierannp/fick1d",
    download_url ="https://github.com/kierannp/fick1d/archive/0.0.1.tar.gz",
    keywords = ['diffusion', '1-dimension', 'material-science'],   # Keywords that define your package best
    install_requires=[            # I get to this in a second
        'numpy',
        'scipy',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
