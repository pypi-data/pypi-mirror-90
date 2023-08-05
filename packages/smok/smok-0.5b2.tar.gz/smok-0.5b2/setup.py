from setuptools import find_packages
from distutils.core import setup
from smok import __version__


setup(version=__version__,
      url='https://github.com/smok-serwis/smok-client/',
      packages=find_packages(include=['smok', 'smok.*']),
      package_data={'smok': ['certs/dev.crt', 'certs/root.crt']},
      install_requires=['requests', 'satella>=2.14.25', 'pytz',
                        'pyasn1', 'cryptography', 'pyopenssl',
                        'ujson'],
      python_requires='!=2.7.*,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*,!=3.5.*',
      zip_safe=False
      )
