import setuptools

with open("README.md", "r") as file:
    long_description = file.read()

setuptools.setup(
    name="genshin-account-switcher",
    version="1.0.1",
    entry_points={
        "console_scripts": ["genshin-account-switcher=src.main:main"]
    },
    author="Christopher Kaster",
    author_email="me@atomicptr.de",
    description="CLI based account switcher for Genshin Impact on Linux.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/atomicptr/genshin-account-switcher",
    install_requires=[
        "appdirs==1.4.4",  # TODO: create this from requirements.txt
    ],
    packages=["src"],
    python_requires=">=3.10",
    classifiers=[
        "Topic :: Games/Entertainment",
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ]
)
