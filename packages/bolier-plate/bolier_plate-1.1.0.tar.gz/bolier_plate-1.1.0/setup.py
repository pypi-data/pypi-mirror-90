import setuptools


setuptools.setup(name='bolier_plate',
      version="1.1.0",
      url = "https://github.com/alexxfernandez13/boiler_plate",
      description='Template already set',
      author='Alejandro Fernandez',
      author_email='alexxfernandez@hotmail.es',
      packages=setuptools.find_packages(),
      install_requires=["numpy", "matplotlib", "scipy", "pandas", "scikit-learn", "pytest"],
      classifiers=[
       "Programming Language :: Python :: 3",
       "License :: OSI Approved :: MIT License",
       "Operating System :: OS Independent",
       ],
     )