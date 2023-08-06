from setuptools import setup, find_packages

setup(

    name='SsyiWorking',

    version='0.2',

    description='This is a demo framework',

    author='Ssyi',

    author_email='shensongyi@sys-test.com.cn',

    zip_safe=False,

    include_package_data=True,

    packages=find_packages(),

    license='MIT',

    url='http://www.sys-test.com.cn',

    entry_points={

        'console_scripts': [

            'SsyiWorking = SsyiWorking.main:main'

        ]

    }

)
