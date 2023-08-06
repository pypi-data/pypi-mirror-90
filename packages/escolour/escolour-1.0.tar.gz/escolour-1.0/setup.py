import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='escolour',
    version='1.0',
    packages=setuptools.find_packages(),
    url='https://github.com/lewisyouldon/escolour',
    license='MIT Licence',
    author='Lewis Youldon',
    author_email='lewisyouldon@gmail.com',
    description='A basic package for having vars for all term colours. Useful for use in formatted strings i.e: f"{RED}This is red{RST}"',
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
