from setuptools import setup

# This call to setup() does all the work
setup(
    name="Wikipedia Scraper",
    version="1.0.0",
    description="Google Tasks Submission",
    download_url="https://github.com/edwinjoshua2003/WikipediaScrapper.git",
    author="Edwin Joshua Samraj",
    author_email="edwinjoshua2003@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["WikipediaScrapper"],
    py_modules=["wikiscrapper"],
    install_requires=["wikipedia", "bs4"],
)
