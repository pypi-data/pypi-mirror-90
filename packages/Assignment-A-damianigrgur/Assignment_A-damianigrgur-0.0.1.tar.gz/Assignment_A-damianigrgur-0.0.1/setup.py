import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Assignment_A-damianigrgur",
    version="0.0.1",
    author="Grgur Damiani",
    author_email="damianigrgur@gmail.com",
    description="Simple handwritten equation solver",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gdamiani1/AssignmentA-main",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)