from setuptools import setup, find_packages
from jpe_types.setup import run as postSetup
from atexit import register
from Cython.Build import cythonize
from os.path import dirname, join

register(postSetup)

path = dirname(__file__)

setup(
    name = "jpe_types",
    packages=["jpe_types/paralel",
              "jpe_types",
              "jpe_types/conversions",
              "jpe_types/logging",
              "jpe_types/caching",
              "jpe_types/utils",
              "jpe_types/utils/Optimizations"],
    
    version="0.0.0.4.6",
    license='wtfpl',
    description="slitly improved python types",
    long_description="""s
    # Threading
    -   adds thread inharitance and return posibility
    -   logging filteter for thread inheritance
    -   a thread and a lock in the same class to make it slitly easyer to work with threads

    # conversions
    - adds the abilty to convert ints to any base

    # logging:
    - logging.log() decorator witch logs function calles
    - logging.createDefaultLogger creats a default logger to logg cals curently rather restricted

    # utils:
    log scanning:
    - adds the ability to scan all log files for keywords
    copy:
    - fix fore schalow copy bug in lists see doc
    
    """,
    include_package_data = True,
    author = 'Julian Wandhoven',                   # Type in your name
    author_email = 'julian.wandhoven@fgz.ch',
    install_requires = [
        "cython",
    ],

    url="https://github.com/JulianWww/jpe_types",
    download_url="https://github.com/JulianWww/jpe_types/archive/loggingPathc.tar.gz",
    keywords=["dtypes", "jpe", "utils", "paralel", "logging"],
    classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.6' ,
    'Programming Language :: Python :: 3'],#Specify which pyhton versions that you want to support
)

#setup.py sdist bdist_wheel