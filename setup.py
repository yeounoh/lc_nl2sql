from setuptools import setup, find_packages

setup(
    name='lc_nl2sql',
    version='0.1.5',
    description='Long Context NL2SQL',
    author='Yeounoh Chung',
    author_email='yeounoh@google.com',
    packages=find_packages(),
    install_requires=[
        'google-cloud-aiplatform==1.66.0', 'google-generativeai>=0.7.2',
        'google-cloud-storage==2.18.2', 'google-cloud==0.32.0',
        'google-api-core==2.19.2',
        'google-ai-generativelanguage==0.6.6', 'transformers==4.39.1',
        'evaluate==0.4.0', 'func-timeout==4.3.5', 'datasets==2.21.0',
        'pydantic==1.10.11', 'pylint==3.0.2',
        'scipy ==1.11.3', 'protobuf==4.25.4',
        'langchain-google-genai==1.0.9', 'langchain-google-vertexai==1.0.8'
    ],
    entry_points={
        'console_scripts': [
            'lc_nl2sql = lc_nl2sql.process_and_predict:main',
        ],
    },
)
