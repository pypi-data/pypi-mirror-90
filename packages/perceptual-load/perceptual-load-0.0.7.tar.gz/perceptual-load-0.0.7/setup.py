import setuptools
from setuptools import setup

setup(
    name="perceptual-load", # Replace with your own username
    version="0.0.7",
    author="Rob Blumberg",
    description="Perceptual Load Experiment",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        'numpy>=1.18.2', 
        'pandas>=1.0.3', 
        'psychopy>=2020.2.10'
    ],
    python_requires='>=3.7',
)
