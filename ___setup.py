import sys
from cx_Freeze import setup, Executable

setup(
    name="BlackJack",
    version="1.0.0",
    description="Singleplayer BlackJack with GUI",
    long_description='',
    long_description_content_type="text/markdown",
    url="https://github.com/Kasyx709/BlackJack",
    author="Rick C",
    author_email="",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=["BlackJack"],
    include_package_data=True,
    install_requires=[
        "numpy", "Pillow", "future", "matplotlib",
        "pandas", "opencv-python", "six", "scipy",
        "multiprocess",
    ],
    entry_points={"console_scripts": ["BlackJack=BlackJack.__main__:main"]},
    executables=[Executable("BlackJack/__main__.py", base="Win32GUI")]
)
