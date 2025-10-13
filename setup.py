from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vloex",
    version="0.1.4",
    author="VLOEX",
    author_email="sats@vloex.com",
    description="VLOEX SDK - Video generation as a computing primitive",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://api.vloex.com/docs",
    project_urls={
        "Documentation": "https://api.vloex.com/docs",
        "Source": "https://github.com/vloex/vloex-python",
        "Bug Reports": "https://github.com/vloex/vloex-python/issues",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
    ],
    keywords="vloex video generation api ai avatar",
)
