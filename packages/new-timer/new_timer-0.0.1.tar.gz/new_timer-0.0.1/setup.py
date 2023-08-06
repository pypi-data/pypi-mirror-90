import setuptools

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="new_timer", # 
    version="0.0.1",
    author="Overcomer",
    author_email="newjerusalem0722@gmail.com",
    description="Program timer.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Michael07220823/new_timer.git",
    keywords="timer",
    python_requires='>=3',
    install_requires=['numpy'],
    packages=setuptools.find_packages(include=["new_timer", "new_timer.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],

)