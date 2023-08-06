from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(name= "wpm_probability",
      version = "0.1.1",
      description = "Probability distributions objects: Gaussian, Binomial.",
      long_description= long_description,
      long_description_content_type = "text/markdown",
      author = "Wisnu Mulya",
      author_email = "wisnu@wisnumulya.com",
      url="https://github.com/WisnuMulya/Probability-Distribution-Package",
      packages=["wpm_probability"],
      license="MIT License",
      install_requires=["matplotlib"],
      zip_safe = False)
