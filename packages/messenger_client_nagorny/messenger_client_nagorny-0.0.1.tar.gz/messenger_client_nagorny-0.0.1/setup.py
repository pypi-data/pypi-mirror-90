from setuptools import setup, find_packages

setup(name="messenger_client_nagorny",
      version="0.0.1",
      description="messenger_client",
      author="Max Nagorny",
      author_email="m.a.nagorny@yandex.ru",
      packages=find_packages(),
      install_requires=['PyQt5', 'sqlalchemy', 'pycryptodome', 'pycryptodomex']
      )
