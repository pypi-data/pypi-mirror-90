from setuptools import setup

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="da-xn-island",
    version="1.1.1",
    description="The Da-xn Island package allows you to get Da-xn Island API data instantly with simple functions!",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://da-xn.com/packages",
    author="Da-xn",
    author_email="dan@da-xn.com",
    maintainer="Da-xn Software",
    keywords="da-xn.com, da-xn, da-xn island, api, windows, mac, linux",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=["da_xn_island"],
    include_package_data=True,
    install_requires=["requests", "colorama"],
    python_requires=">=3.6"
)
