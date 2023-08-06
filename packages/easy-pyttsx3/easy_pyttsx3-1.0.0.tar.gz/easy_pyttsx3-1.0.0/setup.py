import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easy_pyttsx3", # Replace with your own username
    version="1.0.0",
    author="Akshat Tiwari",
    author_email="thealphacoding@gmail.com",
    description="This package can convert text to speeh in very easy way...",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires = ['pyttsx3'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.2',
)