import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bryson", # Replace with your own username
    version="0.0.1",
    author="Jonathan Zavialov",
    author_email="jonzavialov@gmail.com",
    description="A package using various blockchains to generate a random number",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://bryson.studio/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)