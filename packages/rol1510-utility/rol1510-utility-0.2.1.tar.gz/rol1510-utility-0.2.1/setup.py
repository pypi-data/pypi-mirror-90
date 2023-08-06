import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rol1510-utility",
    version="0.2.1",
    author="Roland Strasser",
    author_email="roland1510s@gmail.com",
    description="Usefull stuff for simple helper scripts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rol1510/utility",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>=3.6',
    install_requires=[]
)