from setuptools import setup,find_packages
from glob import glob

with open('README.md', 'r') as f:
    longdesc = f.read()

setup(
    name="nuri",
    version='0.3.0',
    description="Urban Magnetometry Software.",
    long_description=longdesc,
    long_description_content_type='text/markdown',
    author="Vincent Dumont",
    author_email="vincentdumont11@gmail.com",
    maintainer="Vincent Dumont",
    maintainer_email="vincentdumont11@gmail.com",
    url="http://citymag.gitlab.io/nuri",
    project_urls={
        "Source Code": "https://gitlab.com/citymag/nuri",
    },
    packages=['nuri'],
    scripts = glob('bin/*'),
    install_requires=["astropy","gwpy","h5py","matplotlib","numpy","scipy"],
    classifiers=[
        'Intended Audience :: Science/Research',
        "License :: OSI Approved :: MIT License",
        'Natural Language :: English',
        "Operating System :: OS Independent",
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: Physics',
    ],

)
