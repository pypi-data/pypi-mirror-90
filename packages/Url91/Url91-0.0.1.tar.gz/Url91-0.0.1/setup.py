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
package(pkg_name="Url91",author="PkgDev",email="example@example.com",version="0.0.1",short_description="A simplified url package made with request and urllib",long_description="""
#Url91

```py
import Url91

print(Url91.content("https://pypi.org"))
```
""",github_url="https://github.com",python_requirment=">=3.6")