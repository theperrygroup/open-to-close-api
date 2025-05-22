from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="open-to-close-api",
    version="0.1.0",
    author="John Perry",
    author_email="john@theperry.group",
    description="A Python client for the Open To Close API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/theperrygroup/open-to-close-api", # Placeholder URL, update if you have a repo
    packages=find_packages(where="."), # find packages in current directory
    package_dir={'': '.'}, # tell distutils packages are under current directory
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", # Assuming MIT, update if different
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "python-dotenv>=0.15.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "types-requests", # For request stubs if you use type checking in tests
        ]
    },
    project_urls={
        'Bug Reports': 'https://github.com/theperrygroup/open-to-close-api/issues', # Placeholder
        'Source': 'https://github.com/theperrygroup/open-to-close-api/', # Placeholder
    },
) 