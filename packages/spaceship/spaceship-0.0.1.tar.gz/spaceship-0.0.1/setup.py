from setuptools import find_packages, setup


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    author="Pavel Paranin",
    author_email="pavel@paran.in",
    name="spaceship",
    version="0.0.1",
    description="Cosmic web-ecosystem",
    long_description=long_description,
    long_description_content_type="text/markdown",
    setup_requires=["wheel", "setuptools"],
    packages=find_packages(),
    entry_points="""
    [console_scripts]
    spaceship=spaceship.control_center.dispatcher:control
    """,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
