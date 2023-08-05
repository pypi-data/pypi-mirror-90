import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easydataframe_lipsum",
    version="0.0.1",
    install_requires=["pandas"],
    author="lipsum",
    description="A library that handles small xlsx files as a DataFrame.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/NilPointer/easydataframe",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: BSD License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
    ],
    python_requires='>=3.8',
)
