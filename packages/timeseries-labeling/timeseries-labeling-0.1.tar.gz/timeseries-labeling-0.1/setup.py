from setuptools import setup

setup(name='timeseries-labeling',
      version='0.1',
      description='Simple annotation/labeling of events in timeseries',
      url='https://github.com/matnil-star/timeseries_labeling',
      author='Mattias Nilsson',
      author_email='dan.mattias.nilsson@gmail.com',
      license='MIT',
      package_dir = {
            'tsl': 'tsl',
            'tsl.tsl_pylib': 'tsl/tsl_pylib',
            'tsl.tsl_pylib.io': 'tsl/tsl_pylib/io',
            'tsl.tsl_pylib.visualization': 'tsl/tsl_pylib/visualization'},
      packages=['tsl','tsl.tsl_pylib','tsl.tsl_pylib.io','tsl.tsl_pylib.visualization'],
      install_requires=[
          'numpy',
          'pandas',
          'dash',
          'plotly'
      ],
      python_requires='>=3.7',
      zip_safe=False,
      entry_points = {
        'console_scripts': ['tsl=tsl.app:main'],
    })