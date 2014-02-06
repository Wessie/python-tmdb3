from setuptools import setup


setup(
    name="tmdb",
    version="0.1",
    author="Wesley Bitter",
    description="Python library to access the TMDB API.",
    license="MIT",
    install_requires=[
        "requests",
    ],
    packages=["tmdb"],
)
