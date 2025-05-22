from setuptools import setup, find_packages

setup(
    name="tools",
    version="0.1.0",
    description="A collection of useful tools.",
    author="Steezy Punk",
    author_email="steezypunk@gmail.com",
    packages=find_packages(),
    install_requires=[
        "boto3",
        "argparse",
        "requests"
        # Add your dependencies here, e.g. 'requests>=2.0.0'
    ],
    python_requires=">=3.7",
    entry_points={
        # Example for CLI scripts:
        'console_scripts': [
            'tools-cli=tools.cli:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)