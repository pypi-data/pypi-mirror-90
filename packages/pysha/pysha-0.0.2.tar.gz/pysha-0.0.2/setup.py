import setuptools


setuptools.setup(
    name="pysha",
    version="0.0.2",
    author="Arshiatmi",
    author_email="1arhacker1@gmail.com",
    description="A New Born Python Micro Framework",
    long_description_content_type="text/markdown",
    long_description=''.join(open("README.md").readlines()),
    url="https://github.com/Arshiatmi/Pysha",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)