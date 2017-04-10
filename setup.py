try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

with open('readme.org') as reader:
    long_description = reader.read()
    
setup(name='smem',
      long_description=long_description,
      version= '2017.04.09',
      description="smem memory command updated for python 3",
      author="Matt Mackall/cloisteredmonkey",
      platforms=['linux'],
      url = 'https://github.com/necromuralist/smem',
      author_email="necromuralist@hp.com",
      license = "GPLv2",
      install_requires = 'future'.split(),
      packages = find_packages(),
      entry_points = """
	  [console_scripts]
      smem=smem.main:main
      """
      )

# if you have an egg somewhere other than PyPi that needs to be installed as a dependency, point to a page where you can download it:
# dependency_links = ["http://<url>"]
