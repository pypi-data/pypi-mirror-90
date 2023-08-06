import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="comto_core",
    version="1.0.0",
    author="commercito",
    author_email="commercito@gmail.com",
    description="Набор полезных функций для повседневной работы и уменьшения размера кода",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://commercito.ru/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Natural Language :: Russian",
        "Intended Audience :: Developers",
        "License :: Freely Distributable",
        "Topic :: Utilities",
    ],
    python_requires='>=3.8',
)
