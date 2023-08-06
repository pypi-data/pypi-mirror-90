from setuptools import setup, find_packages


with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    name="fuzeepass",
    version="0.1.0",
    description="A command-line fuzzy finder for KeePassX",
    long_description=readme,
    author="Xuta Le",
    author_email="xuta.le@gmail.com",
    url="https://github.com/xuta/fuzeepass",
    packages=find_packages(),
    include_package_data=True,
    license="MIT license",
    zip_safe=False,
    keywords="fuzeepass",
    scripts=["bin/fp", "bin/fpassx.py"],
    install_requires=[
        "pykeepass==3.2.1",
        "click==7.1.2",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: System :: Systems Administration",
    ],
)
