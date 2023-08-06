import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyaudiopdf", # Replace with your own username
    version="0.0.1",
    author="Akshat Tiwari",
    author_email="thealphacoding@gmail.com",
    description="This package can read out Pdf file..",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires = ['pyttsx3','pyPDF2'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)