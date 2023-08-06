import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="oomodelling",
    version="0.0.8",
    author="Claudio Gomes",
    author_email="claudio.gomes@eng.au.dk",
    description="An object oriented modelling package for causal models.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.au.dk/clagms/oomodellingpython",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
