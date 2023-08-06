import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gan_recover_image",
    version="0.1.5",
    author="Fujinet System SJC",
    author_email="tumeotl@gmail.com",
    description="A package use to recovery image",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires=[
           "tensorflow == 2.4.0",
           "Pillow == 8.0.1",
           "numpy == 1.19.4",
       ],
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.xml', '*.special', '*'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)