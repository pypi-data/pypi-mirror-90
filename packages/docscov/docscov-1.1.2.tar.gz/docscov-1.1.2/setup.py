import setuptools

setuptools.setup(
    name="docscov",
    version="1.1.2",
    author="Akib Azmain",
    author_email="akib8492@gmail.com",
    description="Sphinx extension to make a dynamic documentation coverage badge",
    long_description=open("README.rst", "r").read(),
    long_description_content_type="text/x-rst",
    url="https://gitlab.com/AkibAzmain/docscov",
    packages=setuptools.find_packages(),
    install_requires=[
        "coverxygen",
        "sphinx"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.8"
)
