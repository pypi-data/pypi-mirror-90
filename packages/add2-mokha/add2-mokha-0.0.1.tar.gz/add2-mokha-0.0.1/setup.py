import setuptools
setuptools.setup(
    name="add2-mokha", # Replace with your own username
    version="0.0.1",
    author="omar",
    author_email="omar@hwtech.club",
    scripts = ['add'],
    description="A small example package to add 2 numbers",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
 )
