from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='pyLearnAlgorithms',
    version = '0.3.0',
    url='https://github.com/Alyssonmach/pyLearnAlgorithms',
    license='MIT License',
    author='Alysson Machado',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='alysson.barbosa@ee.ufcg.edu.br',
    keywords=['Machine Learning', 'Regression', 'Classification', 'NeuralNetwork'],
    description=u'Python Machine Learning algorithms based on Numpy, Scipy and MatPlotLib.',
    packages=['pyLearnAlgorithms'],
    install_requires=['numpy', 'scipy', 'matplotlib'],)