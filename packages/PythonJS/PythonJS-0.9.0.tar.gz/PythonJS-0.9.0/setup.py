import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PythonJS",
    version="0.9.0",
    author="VivinMeth L V",
    author_email="vivinmeth@gmail.com",
    description="JS Features [like Object, Map] in python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="BSD-3-Clause",
    url="https://gitlab.com/vivinmeth/pythonjs",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    project_urls={
        'Documentation': 'https://gitlab.com/vivinmeth/pythonjs/-/wikis/home',
        'Source': 'https://github.com/vivinmeth/pythonjs',
        'Tracker': 'https://gitlab.com/vivinmeth/pythonjs/issues',
    },
)