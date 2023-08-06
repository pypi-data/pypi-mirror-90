import setuptools
from python_script_manager.package import PSMReader

with open("README.md","r") as fh:
    long_description = fh.read()

psm = PSMReader('psm.json')

setuptools.setup(
    name="python-script-manager",
    version=psm.get_version(),
    author="YunisDEV",
    author_email="yunisdev.04@gmail.com",
    description="Run scripts easily...",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YunisDEV/python-script-manager",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Natural Language :: English"
    ],
    python_requires='>=3.6',
    entry_points='''
        [console_scripts]
        psm=python_script_manager.__main__:main
    ''',
)