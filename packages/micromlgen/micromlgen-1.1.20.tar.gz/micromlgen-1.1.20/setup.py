from distutils.core import setup


setup(
  name = 'micromlgen',
  packages = ['micromlgen'],
  version = '1.1.20',
  license='MIT',
  description = 'Generate C code for microcontrollers from Python\'s sklearn classifiers',
  author = 'Simone Salerno',
  author_email = 'eloquentarduino@gmail.com',
  url = 'https://github.com/eloquentarduino/micromlgen',
  download_url = 'https://github.com/eloquentarduino/micromlgen/blob/master/dist/micromlgen-1.1.20.tar.gz?raw=true',
  keywords = [
    'ML',
    'microcontrollers',
    'sklearn',
    'machine learning'
  ],
  install_requires=[
    'jinja2',
  ],
  package_data={
    'micromlgen': ['templates/vote.jinja', 'templates/dot.jinja', 'templates/_skeleton.jinja', 'templates/classmap.jinja', 'templates/trainset.jinja', 'templates/testset.jinja', 'templates/pca/pca.jinja', 'templates/linearregression/linearregression.jinja', 'templates/wifiindoorpositioning/wifiindoorpositioning.jinja', 'templates/gaussiannb/vote.jinja', 'templates/gaussiannb/gaussiannb.jinja', 'templates/rvm/rvm.jinja', 'templates/xgboost/tree.jinja', 'templates/xgboost/xgboost.jinja', 'templates/decisiontree/tree.jinja', 'templates/decisiontree/decisiontree.jinja', 'templates/randomforest/randomforest.jinja', 'templates/randomforest/tree.jinja', 'templates/sefr/sefr.jinja', 'templates/sefr/dot.jinja', 'templates/svm/svm.jinja', 'templates/svm/computations/class.jinja', 'templates/svm/computations/decisions.jinja', 'templates/svm/computations/votes.jinja', 'templates/svm/computations/kernel/attiny.jinja', 'templates/svm/computations/kernel/arduino.jinja', 'templates/svm/kernel/attiny.jinja', 'templates/svm/kernel/arduino.jinja', 'templates/svm/kernel/kernel.jinja', 'templates/logisticregression/vote.arduino.jinja', 'templates/logisticregression/logisticregression.jinja', 'templates/logisticregression/vote.attiny.jinja', 'templates/principalfft/lut.jinja', 'templates/principalfft/principalfft.jinja', 'templates/principalfft/lut_bool.jinja']
  },
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Code Generators',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
