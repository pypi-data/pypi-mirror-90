import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="limeutils", # Replace with your own username
    version="0.1.8",
    author="enchance",
    author_email="enchance@gmail.com",
    description="A collection of my utility functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/enchance/limeutils.git",
    packages=setuptools.find_packages(),
    install_requires=['redis', 'pydantic', 'limeutils'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)