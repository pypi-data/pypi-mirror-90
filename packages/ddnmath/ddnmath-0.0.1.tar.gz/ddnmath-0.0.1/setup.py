import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ddnmath",  # Replace with your own username
    version="0.0.1",
    author="Davoud Nasrabadi",
    author_email="davoud.nasrabadi@example.com",
    description="davoud nasrabadi math package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/davoudnasrabadi/ddnmath",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
