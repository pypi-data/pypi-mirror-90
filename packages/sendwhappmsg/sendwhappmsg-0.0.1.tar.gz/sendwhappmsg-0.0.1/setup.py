import setuptools

with open("README.md") as fh:
    long_description = fh.read()

setuptools.setup(
    name='sendwhappmsg',
    version="0.0.1",
    author="Ankit Singh",
    author_email="ankitsingh300307@gmail.com.com",
    description="This module will send any whatsapp message to any mobile no.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ankitsinghprograms/sendwhatsappmsg",
    install_requires=["webbrowser"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)