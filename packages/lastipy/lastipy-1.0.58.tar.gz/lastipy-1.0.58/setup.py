from setuptools import setup, find_packages

setup(name='lastipy',
      version='1.0.58',
      description='Python library that combines Last.fm and Spotify',
      url='http://github.com/evanjamesjackson/lastipy',
      author='Evan Jackson',
      author_email='evanjamesjackson@gmail.com',
      packages=find_packages(),
      entry_points={'console_scripts': [
          'recommendations_playlist = scripts.recommendations_playlist:build_recommendations_playlist',
          'save_new_releases = scripts.save_new_releases:save_new_releases',
          'organize_favorites = scripts.organize_favorites:organize_favorites'
      ]},
      install_requires=['numpy', 'requests', 'spotipy', 'pytest', 'iso8601', 'python-dateutil'])
