from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='itssutils',
    version='0.0.1',
    description='Utilities for analyzing Illinois Traffic Stop Study data.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://github.com/JustDSOrg/itssutils',
    author='Chris Kucharczyk',
    author_email='chris.kucharczyk@gmail.com',
    license='MIT',
    packages=find_packages(),
    classifiers=[
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
    ],
    install_requires=[
        "pandas",
        "numpy",
        "scipy",
        "matplotlib",
        "tqdm",
        "statsmodels",
    ],
)
