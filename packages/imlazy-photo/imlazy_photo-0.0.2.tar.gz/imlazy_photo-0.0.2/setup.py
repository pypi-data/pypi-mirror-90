import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="imlazy_photo", # Replace with your own username
    version="0.0.2",
    author="cosmos2",
    author_email="playnstop.s@gmail.com",
    description="Make directory and put in photo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cosmos2/imlazy_photo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3.7',
)