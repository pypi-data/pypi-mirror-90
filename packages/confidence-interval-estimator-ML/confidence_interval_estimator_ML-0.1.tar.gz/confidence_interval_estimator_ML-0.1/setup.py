from distutils.core import setup
setup(
  name = 'confidence_interval_estimator_ML',         # How you named your package folder (MyLib)
  packages = ['confidence_interval_estimator_ML'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='GNU General Public License (GPL)',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Simple utility to compute confidence intervals for machine learning models',   
  author = 'Giovanni Ciampi',                   # Type in your name
  author_email = 'giovanniciampi95@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/user/Confidence_Interval_Estimator_ML',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/GiovanniCiampi/confidence_interval_estimator_ML/archive/v0.1.tar.gz',# I explain this later on
  keywords = ['Confidence-Intervals', 'Confidence', 'Machine Learning', 'Accuracy', "Bootstrap", "MonteCarlo", 'Machine-Learning'],   
  install_requires=[            # I get to this in a second
          'tqdm',
          'numpy',
          "scipy",
          "matplotlib"
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License (GPL)',   # Again, pick a license Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)