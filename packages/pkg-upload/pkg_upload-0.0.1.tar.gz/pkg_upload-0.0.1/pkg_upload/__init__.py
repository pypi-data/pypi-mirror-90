def upload(folder_name,type_="in_folder"):
  import os
  os.system("pip install --upgrade pip")
  os.system("pip install twine")
  if type_=="in_folder":
    os.system('python ' +folder_name+'/setup.py sdist bdist_wheel')
  else:
    os.system("python setup.py sdist bdist_wheel")
  os.system('twine upload dist/*')



def package(pkg_name,author,email,version,short_description,long_description,github_url,python_requirment):
  import setuptools
  setuptools.setup(
      name=pkg_name, 
      version=version, 
      author=author, 
      author_email=email, 
      description=short_description, 
      long_description=long_description,
      long_description_content_type="text/markdown",
      url=github_url, 
      packages=setuptools.find_packages(),
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
  )