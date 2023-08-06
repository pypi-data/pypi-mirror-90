import setuptools

setuptools.setup(
  name = "nanotts",
  version = "0.0.1",
  author = "Volker Austrup",
  author_email = "volkeraustrup@gmail.com",
  description = "Python wrapper for the NanoTTS speech synthesizer",
  long_description = open('README.md').read(),
  long_description_content_type = "text/markdown",
  url = "https://github.com/VolkaRacho/nanotts",
  packages = setuptools.find_packages(),
  classifiers = [
    "Topic :: Multimedia :: Sound/Audio :: Sound Synthesis",
    "Topic :: Multimedia :: Sound/Audio :: Speech",
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: POSIX :: Linux",
  ],
  python_requires = ">=3.6",
)
  
