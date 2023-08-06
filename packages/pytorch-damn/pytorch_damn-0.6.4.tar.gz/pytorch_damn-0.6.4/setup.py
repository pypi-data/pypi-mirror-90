import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytorch_damn", 
    version="0.6.4",
    author="Bence Tilk",
    author_email="bence.tilk@gmail.com",
    description="Domain Attention Mixing Network: tool for domain adaptation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tilkb/damn",
    packages=setuptools.find_packages(),
    install_requires=['torch','pytorch-lightning', 'torchvision'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)