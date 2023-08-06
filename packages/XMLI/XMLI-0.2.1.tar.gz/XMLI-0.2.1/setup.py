from distutils.core import setup

with open("README.md") as fh:
  long_description = fh.read()

version = '0.2.1'
  
setup(
  name = 'XMLI',
  packages = ['xmli', 'xmli.libs'],
  version = version,
  license='Custom',
  description = 'xmli module is used to manage XML files.',
  long_description = long_description,
  author = 'Kazafka/Kafajku/kzfka',
  author_email = 'caffiqu@gmail.com',
  url = 'https://github.com/Kafajku/xmli',
  download_url = 'https://github.com/Kafajku/xmli/archive/v_{}.tar.gz'.format(version),
  keywords = ["xmli", "XML", "XMLI", "eXtensible Markup Language"],
  classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.9',
  ]
)
