import setuptools
with open("README.md","r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Ahao",
    version="0.0.1",
    author = "Ahao",
    author_email = "ttt4336@126.com",
    descrition = "Ahao, test in 20210104",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/Kevin-777/hello-world",
    packages = setuptools.find_packages(),
    clssifiers = [
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: BSD License',
        "Operating System :: Windows 10",
    ],
)