from setuptools import setup, find_packages

setup(
    name='lc_nl2sql',
    version='0.1.2',
    description='Long Context NL2SQL',
    author='Yeounoh Chung',
    author_email='yeounoh@google.com',
    packages=find_packages(),
    install_requires=[
        'google-cloud-aiplatform>=1.38', 'google-generativeai>=0.5.3',
        'google-ai-generativelanguage>=0.6.3', 'transformers==4.39.1',
        'evaluate==0.4.0', 'func-timeout==4.3.5', 'datasets>=2.14.6',
        'pydantic==1.10.11', 'pylint==3.0.2',
        'scipy ==1.11.3',
    ],
    entry_points={
        'console_scripts': [
            'lc_nl2sql = lc_nl2sql.process_and_predict:main',
        ],
    },
)
