import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bnb-sheerin-bnb", 
    version="0.0.1",
    author="sheerin",
    author_email="sheerin@brainynbright.com",
    description="Test package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Brainy-N-Bright/python/tree/main/package",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
