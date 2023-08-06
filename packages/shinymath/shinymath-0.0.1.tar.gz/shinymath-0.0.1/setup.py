import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="shinymath",  # Replace with your own username
    version="0.0.1",
    author="Davoud Nasrabadi",
    author_email="davoud.nasrabadi@gmail.com",
    description="A small math package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/davoudnasrabadi/shinymath",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
