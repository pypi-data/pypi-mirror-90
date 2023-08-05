from setuptools import setup, find_packages

setup(
    name="IslandPy",
    version="0.0.0.dev6",
    author="ludwici",
    author_email="andrew.volski@gmail.com",
    packages=find_packages(),
    install_requires=[
        "pygame"
    ],
    project_urls={
        "Source": "https://github.com/ludwici/IslandPy",
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ]
)

