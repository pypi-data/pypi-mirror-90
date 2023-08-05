import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ConsoleQuestionPrompts",  # Replace with your own username
    version="2.0.0",
    author="Jonathan Elsner",
    author_email="jelsnerbusiness@outlook.com",
    description="Facilitates asking questions to the user through the console.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JEElsner/ConsoleQuestionPrompts",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
