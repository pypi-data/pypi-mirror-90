import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

packages = ['hpcomt']

requires = [
    'platform'
]

setuptools.setup(
    name="hpcomt",
    version="0.0.1",
    author="Honey Pots",
    author_email="honeypots124@gmail.com",
    description="Detect OS Name, E.g. 'Android', 'Linux', 'Windows' or 'Java' , Etc.",
    long_description="Detect OS Name, E.g. 'Android', 'Linux', 'Windows' or 'Java' , Etc. Special Thing In This Module It Can Be Detect Android OS",
    long_description_content_type="text/markdown",
    url="https://github.com/honeypots0/hpcomt",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
) 
