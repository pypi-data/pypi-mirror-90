# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['persine', 'persine.bridges']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=7.0.0',
 'beautifulsoup4>=4.6.3',
 'pandas>=1.1.5,<2.0.0',
 'selenium>=3.141.0,<4.0.0']

extras_require = \
{'docs': ['sphinx>=3,<4']}

setup_kwargs = {
    'name': 'persine',
    'version': '0.1.3',
    'description': 'Persine is an automated tool to study and reverse-engineer algorithmic recommendation systems. It has a simple interface and encourages reproducible results.',
    'long_description': '[![Documentation Status](https://readthedocs.org/projects/persine/badge/?version=latest)](https://persine.readthedocs.io/en/latest/?badge=latest)\n\n# Persine, the Persona Engine\n\nPersine is an **automated tool to study and reverse-engineer algorithmic recommendation systems**. It has a simple interface and encourages reproducible results. You tell Persine to drive around YouTube and it gives back a spreadsheet of what else YouTube suggests you watch!\n\n> Persine => **Pers**[ona Eng]**ine**\n\n### For example!\n\nPeople have suggested that if you watch a few lightly political videos, YouTube starts suggesting more and more extreme content – _but does it really?_\n\nThe theory is difficult to test since it involves a lot of boring clicking and YouTube already knows what you usually watch. **Persine to the rescue!**\n\n1. Persine starts a new fresh-as-snow Chrome\n2. You provide a list of videos to watch and buttons to click (like, dislike, "next up" etc)\n3. As it watches and clicks more and more, YouTube customizes and customizes\n4. When you\'re all done, Persine will save your winding path and the video/playlist/channel recommendations to nice neat CSV files.\n\nBeyond analysis, these files can be used to repeat the experiment again later, seeing if recommendations change by time, location, user history, etc.\n\nIf you didn\'t quite get enough data, don\'t worry – you can resume your exploration later, picking up right where you left off. Since each "persona" is based on Chrome profiles, all your cookies and history will be safely stored until your next run.\n\n### An actual example\n\nSee Persine in action [on Google Colab](https://colab.research.google.com/drive/1eAbfwV9mL34LVVIzW4AgwZt5NZJ21LwT?usp=sharing).\n\nIncludes a few examples for analysis, too.\n\n## Installation\n\n```\npip install persine\n```\n\nPersine will automatically install Selenium and BeautifulSoup for browsing/scraping, pandas for data analysis, and pillow for processing screenshots.\n\nYou will need to manually install chromedriver to allow Selenium to control Chrome. [See details here](https://persine.readthedocs.io/en/latest/user/install.html)\n\n## Quickstart\n\nIn this example, we start a new session by visiting a YouTube video and clicking the "next up" video three times to see where it leads us. We then save the results for later analysis.\n\n```python\nfrom persine import PersonaEngine\n\nengine = PersonaEngine(headless=False)\n\nwith engine.persona() as persona:\n    persona.run("https://www.youtube.com/watch?v=hZw23sWlyG0")\n    persona.run("youtube:next_up#3")\n    persona.history.to_csv("history.csv")\n    persona.recommendations.to_csv("recs.csv")\n```\n\nWe turn off headless mode because it\'s fun to watch!\n\n## More examples, more features, more everything\n\n[Find the complete documentation here](https://persine.readthedocs.io/)',
    'author': 'Jonathan Soma',
    'author_email': 'jonathan.soma@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jsoma/persine',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.3',
}


setup(**setup_kwargs)
