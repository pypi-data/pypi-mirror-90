import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MegaLib2", # Replace with your own username
    version="0.0.2",
    author="Mega145",
    author_email="kacpermi@poczta.fm",
    description="Package that helps me with my projects feel free to use it yourself",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mega145/MegaLib",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: Free For Educational Use",
        "Operating System :: OS Independent",
        "Development Status :: 1 - Planning",
        "Intended Audience :: Education",
        "Natural Language :: Polish",
        "Topic :: Utilities"
    ],
    python_requires='>=3.8',
)
