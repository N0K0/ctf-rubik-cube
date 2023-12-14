import setuptools

long_description = open("README.md").read()

setup_params = dict(
    name="ctf-rubik-cube",
    version="0.0.3",
    license="MIT",
    author="Nikolas Papaioannou",
    author_email="cube@hacky.software",
    url="https://github.com/pglass/cube",
    keywords="rubik cube solver - ctf edition",
    packages=["rubik"],
    package_data={"": ["LICENSE"]},
    package_dir={"rubik": "rubik"},
    include_package_data=True,
    description="A basic, pure-Python Rubik's cube solver, with support for arbitrary data on each sticker.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)

if __name__ == "__main__":
    setuptools.setup(**setup_params)
