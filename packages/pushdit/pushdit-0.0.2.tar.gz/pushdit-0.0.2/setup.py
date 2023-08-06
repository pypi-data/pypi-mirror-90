import setuptools

with open('README.md', 'r', encoding="utf=8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "pushdit",
    version = "0.0.2",
    author = "Antsthebul",
    author_email = "anthony.allen.srt@gmail.com",
    description = "pushd command like Linux",
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = "",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_require = '>=python3.6'
)