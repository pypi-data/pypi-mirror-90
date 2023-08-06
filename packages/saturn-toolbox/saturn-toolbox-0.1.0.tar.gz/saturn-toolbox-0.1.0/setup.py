import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="saturn-toolbox", # Replace with your own username
    version="0.1.0",
    author="Saturn Software",
    author_email="saturn.dev@protonmail.com",
    description="A toolbox for resekkers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/akavenus/saturn-toolbox",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': ['saturn-toolbox=saturn_toolbox.toolbox:main'], 
    },
    python_requires='>=3.6',
)
