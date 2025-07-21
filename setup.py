from setuptools import setup, find_packages

setup(
    name="cs2-stats-analyzer",
    version="1.0.0",
    description="CS2 match statistics analyzer and report generator",
    author="SnakeFist",
    author_email="github@snakefist.de",
    packages=find_packages(),
    install_requires=[
        # No external dependencies - uses only Python standard library
    ],
    entry_points={
        'console_scripts': [
            'cs2-stats=main:main',
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)