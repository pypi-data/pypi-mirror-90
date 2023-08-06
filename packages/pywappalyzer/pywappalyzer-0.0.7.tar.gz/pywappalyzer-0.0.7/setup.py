import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pywappalyzer",
    version="0.0.7",
    author="Kel0",
    author_email="rozovdima123@gmail.com",
    description="Easy identify site's technologies.json",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kel0/pywappalyzer",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=[
        "geckodriver-autoinstaller==0.1.0",
        "lxml==4.6.1",
        "selenium==3.141.0",
        "requests==2.24.0",
        "requests-toolbelt==0.9.1",
        "lxml==4.6.1"
    ]
)
