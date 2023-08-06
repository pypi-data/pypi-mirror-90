##import the setup function from pythons distrubution utility with set up function argument names
from distutils.core import setup

setup( 
        name         = 'nester-pkg-gjones1228',
        version      = '1.0.0',
        ## TODO: be sure to change these next few lines to match your details!
        py_modules   = ['nester'],
        author       = 'gjones1228',
        author_email = 'gjones1228@gmail.com',
        url          = 'http://www.headfirstlabs.com',
        description  = 'A simple printer of nested lists',
     )
