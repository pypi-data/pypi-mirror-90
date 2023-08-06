# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dbxdeploy',
 'dbxdeploy.cluster',
 'dbxdeploy.dbc',
 'dbxdeploy.dbfs',
 'dbxdeploy.deploy',
 'dbxdeploy.git',
 'dbxdeploy.job',
 'dbxdeploy.notebook',
 'dbxdeploy.notebook.converter',
 'dbxdeploy.package',
 'dbxdeploy.s3',
 'dbxdeploy.string',
 'dbxdeploy.workspace']

package_data = \
{'': ['*'],
 'dbxdeploy': ['_config/.gitignore',
               '_config/.gitignore',
               '_config/.gitignore',
               '_config/config.yaml',
               '_config/config.yaml',
               '_config/config.yaml',
               '_config/config_test.yaml',
               '_config/config_test.yaml',
               '_config/config_test.yaml']}

install_requires = \
['boto3>=1.16.0,<2.0.0',
 'console-bundle==0.3.0a2',
 'databricks-api>=0.3.0,<0.4.0',
 'dbx-notebook-exporter>=0.4.0,<0.5.0',
 'injecta>=0.8.12,<0.9.0',
 'nbconvert>=5.6.0,<5.7.0',
 'pyfony-bundles==0.2.5a2',
 'pygit2>=1.3.0,<1.4.0',
 'python-box>=3.4.0,<3.5.0',
 'tomlkit>=0.5.0,<0.6.0']

entry_points = \
{'pyfony.bundle': ['autodetect = '
                   'dbxdeploy.DbxDeployBundle:DbxDeployBundle.autodetect']}

setup_kwargs = {
    'name': 'dbx-deploy',
    'version': '0.13.0a2',
    'description': 'Databricks Deployment Tool',
    'long_description': 'Databricks project deployment package\n',
    'author': 'Jiri Koutny',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bricksflow/dbx-deploy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.3,<3.8.0',
}


setup(**setup_kwargs)
