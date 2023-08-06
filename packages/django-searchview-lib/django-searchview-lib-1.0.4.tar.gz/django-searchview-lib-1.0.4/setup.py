import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django-searchview-lib", # Replace with your own username
    version="1.0.4",
    author="Arisophy",
    author_email="arisophy@is-jpn.com",
    description="SearchView is a multiple inheritance class of FormView and ListView",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Arisophy/django-searchview",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)