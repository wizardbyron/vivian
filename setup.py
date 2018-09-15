from setuptools import setup, find_packages  

# chardet's setup.py
from distutils.core import setup

setup(
    name = "vivian",
    packages = find_packages(),
    version = "0.0.1.dev8",
    description = "vivian is CLI for veirfying URLs redirection from file in multi-thread mode. It's easy to integrated with CI in smoke or regression test.",
    author = "wizardbyron",
    author_email = "wizard0530@gmail.com",
    url = "https://github.com/wizardbyron/vivian",
    keywords = ["url", "redirection", "redirect", "verify", "test", "tests"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Topic :: Internet :: WWW/HTTP :: Site Management :: Link Checking",
        "Topic :: Software Development :: Testing",
        "Topic :: Utilities"
        ],
    install_requires=['requests'],
    entry_points={  
        'console_scripts':[ 
            'vivian = vivian.vivian:main'      
        ] 
    },
    python_requires='>=2.6, !=3.0.*, !=3.1.*, !=3.2.*, <4',
    long_description = "vivian is CLI for veirfying URLs redirection from file in multi-thread mode. It's easy to integrated with CI in smoke or regression test."
)