import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nit-udasitharani",
    version="0.0.4",
    author="Udasi Tharani",
    author_email="udasitharani@gmail.com",
    description="A tool to generate tiles from name initials.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/udasitharani/name-initials-tile-generator",
    packages=setuptools.find_packages(),
    classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent"
    ],
    python_requires=">=3.6"
)
