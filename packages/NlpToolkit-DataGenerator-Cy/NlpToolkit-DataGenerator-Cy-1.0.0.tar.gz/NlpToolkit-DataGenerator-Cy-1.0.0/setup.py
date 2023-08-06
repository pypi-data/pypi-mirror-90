from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize(["DataGenerator/Attribute/*.pyx",
                           "DataGenerator/CorpusGenerator/*.pyx",
                           "DataGenerator/InstanceGenerator/*.pyx",
                           "DataGenerator/DatasetGenerator/*.pyx"],
                          compiler_directives={'language_level': "3"}),
    name='NlpToolkit-DataGenerator-Cy',
    version='1.0.0',
    packages=['DataGenerator', 'DataGenerator.Attribute', 'DataGenerator.CorpusGenerator',
              'DataGenerator.DatasetGenerator', 'DataGenerator.InstanceGenerator'],
    package_data={'DataGenerator.Attribute': ['*.pxd', '*.pyx', '*.c'],
                  'DataGenerator.CorpusGenerator': ['*.pxd', '*.pyx', '*.c'],
                  'DataGenerator.DatasetGenerator': ['*.pxd', '*.pyx', '*.c'],
                  'DataGenerator.InstanceGenerator': ['*.pxd', '*.pyx', '*.c']},
    url='https://github.com/olcaytaner/DataGenerator-Cy',
    license='',
    author='olcaytaner',
    author_email='olcaytaner@isikun.edu.tr',
    description='Classification dataset generator library for high level Nlp tasks',
    install_requires=['NlpToolkit-AnnotatedSentence-Cy', 'NlpToolkit-AnnotatedTree-Cy', 'NlpToolkit-Classification-Cy',
                      'NlpToolkit-MorphologicalDisambiguation-Cy']
)
