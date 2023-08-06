from setuptools import setup, find_packages 
  
with open('requirements.txt') as f: 
    requirements = f.readlines() 
  
long_description = """Version 1.1.0
Fixed socket connection problem"""
  
setup( 
        name ='bulkmail', 
        version ='1.1.0', 
        author ='Rafeed M. Bhuiyan', 
        author_email ='rafeedm.bhuiyan@gmail.com', 
        url ='https://github.com/roughweed/csv-bulk-email', 
        description ='Python package for sending bulk emails.', 
        long_description = long_description, 
        long_description_content_type ="text/markdown", 
        license ='MIT', 
        packages = find_packages(), 
        entry_points ={ 
            'console_scripts': [ 
                'bulkmail = bulkmail.commandline:main'
            ] 
        },
        classifiers =( 
            "Programming Language :: Python :: 3", 
            "License :: OSI Approved :: MIT License", 
            "Operating System :: OS Independent", 
        ), 
        python_requires='>=3.6',
        keywords ='email bulk cli mail', 
        install_requires = requirements, 
        zip_safe = False
) 