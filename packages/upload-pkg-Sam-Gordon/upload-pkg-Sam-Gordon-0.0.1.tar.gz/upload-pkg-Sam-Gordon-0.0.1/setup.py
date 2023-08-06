# TODO: Fill out this file with information about your package
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="upload-pkg-Sam-Gordon",
    version="0.0.1",
    user="Sam Gordon",
    user_email="samcrebs@gmail.com",
    description="Uploading py for Udacity",
    long_description=long_description,
    url="https://test.pypi.org/legacy/ dist/*",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
    
# HINT: Go back to the object-oriented programming lesson "Putting Code on PyPi" and "Exercise: Upload to PyPi"

# HINT: Here is an example of a setup.py file
# https://packaging.python.org/tutorials/packaging-projects/
