from setuptools import setup, find_packages

setup(name='jira-wiki-md',
      version='0.5.0',
      author='Jean Giard',
      license='LGPL',
      classifier=[
          'Programming Language :: Python :: 3'
      ],
      packages=find_packages(where='src'),
      package_dir={'': 'src'},
      entry_points={
          'markdown.extensions': ['jirawiki = jiramd.extension:JiraWikiExtension']
      },
      include_package_data=True,
      install_requires=[
          'markdown'
      ],
      )
