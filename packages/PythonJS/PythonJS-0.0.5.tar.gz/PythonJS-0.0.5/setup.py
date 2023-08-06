import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PythonJS",
    version="0.0.5",
    author="VivinMeth L V",
    author_email="vivinmeth@gmail.com",
    description="JS Features [i.e Object, Map] in python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/vivinmeth/pythonjs",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)