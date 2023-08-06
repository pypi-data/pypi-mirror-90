import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fthelper",
    version="0.1.2",
    author="Fatih IRDAY",
    author_email="fatihirday@gmail.com",
    description="Dict, list and string helper package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/fatihirday/fthelper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
