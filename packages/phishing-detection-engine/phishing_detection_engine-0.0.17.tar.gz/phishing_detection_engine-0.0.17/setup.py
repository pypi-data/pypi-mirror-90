from setuptools import find_packages, setup
long_line = """The project is using different techniques to identify phishing URLs.
               Machine Learning and use of different APIs is done to get good results.
               At first, model checks the URL in databases of phishing URLs. 
               If URL is found in database, user is given output immediaately.
               If URL is not categorized at that point, then it is categorized using
               machine learning model whcih is trained on dataset of above 18000 Websites"""
setup(
    name='phishing_detection_engine',
    packages=find_packages(),
    version='0.0.17',
    author_email="hamzaanjum1@gmail.com",
    description='Library for Detecting Phishing URLs',
    long_description=long_line,
    author='HamzaAnjum_hamzaanjum9696',
    license='MIT',
    install_requires=
    [
        'requests',
        'IPy',
        'bs4',
        'tld',
        'python-whois==0.7.3',
        'favicon',
        'selenium',
        'scikit-learn==0.23.2',
        'numpy==1.18.5',
        'scipy==1.5.4'
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
    include_package_data=True
)