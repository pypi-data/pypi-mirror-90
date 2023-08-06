import pathlib
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


# This call to setup() does all the work
setuptools.setup(
   name='seismopy',
   version='1.0.1',
   author='Mohsen Azimi',
   author_email='mohsen.azimi@nevada.unr.edu',
   license='MIT',
   description="A Package for Structural and Earthquake Engineering",
   long_description=long_description,
   long_description_content_type="text/markdown",
   url='https://github.com/mohsen-azimi/SeismoPy',
   packages=setuptools.find_packages(),
   classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
   include_package_data=True,
   install_requires=[],
   python_requires='>=3.6',

)
