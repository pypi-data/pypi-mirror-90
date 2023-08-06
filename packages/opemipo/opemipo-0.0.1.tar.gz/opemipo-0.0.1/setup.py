import setuptools 

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "opemipo",
    version = "0.0.1",
    author = "Salami Samad",
    description = "this package shows the greater or less number",
    long_description=long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/kelvinace1/opemipo",
    download_url = "https://github.com/kelvinace1/opemipo/archive/v_01.tar.gz",
    packages = setuptools.find_packages(),
    classifiers=[
        #'Development Status :: 3 - Alpha',
        #'Intended Audience :: Developers',
        #'Topic :: Software Development :: Build Tools',
        #'license :: OSI Approved :: MIT License',
        #'Operating System :: OS Independent',
        #'Programming Language :: python :: 3',
        #'Programming Language :: python :: 3.5',
        #'Programming Language :: python :: 3.6',
        
    ],
    python_requires ='>=3.6'
)