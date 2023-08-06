##import the setup function from pythons distrubution utility with set up function argument names
from distutils.core import setup

setup( 
        name         = 'nester-pkg-gjones1228',
        version      = '1.1.0',
        ## TODO: be sure to change these next few lines to match your details!
        py_modules   = ['nester-gjones1228'],
        author       = 'gjones1228',
        author_email = 'gjones1228@gmail.com',
        ## url          = 'http://www.headfirstlabs.com',
        description  = 'A simple printer of nested lists',
       ## long_description=long_description,
	##    long_description_content_type="text/markdown",
	    url="https://github.com/pypa/sampleproject",
	##    packages=setuptools.find_packages(),
	##    classifiers=[
	##	"Programming Language :: Python :: 3",
	##        "License :: OSI Approved :: MIT License",
	##        "Operating System :: OS Independent",
	##    ],
    	##python_requires='>=3.6',
     )
