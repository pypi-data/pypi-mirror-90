from setuptools import setup, find_packages
from pathlib import Path

setup(
    name='comentarios-variados',
    version=1.0,
    descriptio='Este pacote irá fornecer duas listas de comentarios variados',
    long_description=Path('README.md').read_text(),
    author='Eduardo Silva de Abreu',
    author_email='edwards.s.a@hotmail.com',
    keywords=['comentarios', 'listas'],
    packages=find_packages()
)
