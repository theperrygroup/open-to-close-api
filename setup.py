from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="open-to-close-api",
    version="1.0.1",
    author="John Perry",
    author_email="john@theperry.group",
    description="A Python client for the Open To Close API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/theperrygroup/open-to-close-api",  # Placeholder URL, update if you have a repo
    packages=find_packages(),  # find packages in current directory
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Assuming MIT, update if different
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "python-dotenv>=0.19.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            "responses>=0.23.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "isort>=5.12.0",
            "pylint>=2.17.0",
            "types-requests>=2.25.0",
        ]
    },
    project_urls={
        "Bug Reports": "https://github.com/theperrygroup/open-to-close-api/issues",  # Placeholder
        "Source": "https://github.com/theperrygroup/open-to-close-api/",  # Placeholder
    },
)
