import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='parseudr',
     version='0.1.8',
    #  scripts=['storagemodel', 'trainmodel'] ,
     author="Arvind Ravish",
     author_email="arvind.ravish@gmail.com",
     description="A simple package to get Databricks FQDN IP addresses",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="",
     packages=['parseudr'],  #setuptools.find_packages(),
      #  py_modules=['storagemodel'],
    install_requires=[
        'pandas', 'lxml'
    ],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )