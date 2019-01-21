from setuptools import setup, find_packages

setup(
    name="runcible",
    version="0.1.0",
    author="Drew Bednar",
    author_email="drew@androiddrew.com",
    description="A development  API to be used in vuejs courses and tutorials.",
    packages=find_packages(exclude=["tests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT license",
        "Operating System :: OS Independent",
    ],
)
