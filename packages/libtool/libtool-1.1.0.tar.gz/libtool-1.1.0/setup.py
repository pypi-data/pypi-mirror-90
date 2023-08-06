import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='libtool',
    version='1.1.0',
    license='MIT',
    description='Create, version and upload library',
    author='matan h',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author_email='matan.honig2@gmail.com,',
    url='https://github.com/matan-h/libtool',
    packages=['libtool', "libtool._cmd_argv", "libtool.util", "libtool.pypi"],
    scripts=['libtool\\cmd\\libtool.bat'],
    package_data={'libtool': ["README_in.md"]},

    install_requires=["Markdown-Editor", "requests", "setuptools", "wheel", "twine"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
