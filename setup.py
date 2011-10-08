from setuptools import setup, find_packages
import os

version = open(os.path.join("younglives", "research", "types", "version.txt")).read().strip()

setup(name='younglives.research.types',
      version=version,
      description="",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['younglives', 'younglives.research'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.wfform',
          'collective.portlet.workflowsteps',
      ],
      extras_require = {
          'test': [
              'plone.app.testing',
          ]
      },
      entry_points="""
      # -*- Entry points: -*-
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
