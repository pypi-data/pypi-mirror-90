import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ez_settings",
    version="1.0.2",
    author="Niels Vaes",
    license='MIT',
    author_email="nielsvaes@gmail.com",
    description="Easy settings module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nielsvaes/ez_settings",
    install_requires=[],
    packages=setuptools.find_packages(),
    classifiers=[
        "Operating System :: OS Independent",
    ]
)