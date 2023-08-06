import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="YTVdownload", # Replace with your own username
    version="1.0.1",
    author="Akshat Tiwari",
    author_email="thealphacoding@gmail.com",
    description="This package can Download YouTube videos in MP3 or MP4 format....",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url = 'https://github.com/alphacodingat/YTVdownload.git' ,
    packages=setuptools.find_packages(),
    install_requires = ['pafy'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.2',
)