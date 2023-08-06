import setuptools


with open("CrappyPython/README.md","r",encoding="utf-8") as fhandle:
  long_description=fhandle.read()

setuptools.setup(
    name="CrappyPython", #Package Name!
    version="0.0.1", # The version of your package!
    author="pkguploaders", # Your name here!
    author_email="pkguploaders@gmail.com", # Your e-mail here!
    description="Several Packages in one!", # A short description here!
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/awesome/CrappyPython", # Link your package website here! (most commonly a GitHub repo)
    packages=setuptools.find_packages(), # A list of all packages for Python to distribute!
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ], # Enter meta data into the classifiers list!
    python_requires='>=3.6', # The version requirement for Python to run your package!
)
