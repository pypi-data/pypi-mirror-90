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

setup_kwargs = {
    'name': 'persine',
    'version': '0.1.2',
    'description': 'Persine is an automated tool to study and reverse-engineer algorithmic recommendation systems. It has a simple interface and encourages reproducible results.',
    'long_description': '# Persine, the Persona Engine\n\nPersine is an **automated tool to study and reverse-engineer algorithmic recommendation systems**. It has a simple interface and encourages reproducible results. You tell Persine to drive around YouTube and it gives back a spreadsheet of what else YouTube suggests you watch!\n\n> Persine => **Pers**[ona Eng]**ine**\n\n### For example!\n\nPeople have suggested that if you watch a few lightly political videos, YouTube starts suggesting more and more extreme content – _but does it really?_\n\nThe theory is difficult to test since it involves a lot of boring clicking and YouTube already knows what you usually watch. **Persine to the rescue!**\n\n1. Persine starts a new fresh-as-snow Chrome\n2. You provide a list of videos to watch and buttons to click (like, dislike, "next up" etc)\n3. As it watches and clicks more and more, YouTube customizes and customizes\n4. When you\'re all done, Persine will save your winding path and the video/playlist/channel recommendations to nice neat CSV files.\n\nBeyond analysis, these files can be used to repeat the experiment again later, seeing if recommendations change by time, location, user history, etc.\n\nIf you didn\'t quite get enough data, don\'t worry – you can resume your exploration later, picking up right where you left off. Since each "persona" is based on Chrome profiles, all your cookies and history will be safely stored until your next run.\n\n### An actual example\n\nSee Persine in action [on Google Colab](https://colab.research.google.com/drive/1eAbfwV9mL34LVVIzW4AgwZt5NZJ21LwT?usp=sharing). Includes a few examples for analysis, too.\n\n## Installation\n\n```\npip install persine\n```\n\nPersine will automatically install Selenium and BeautifulSoup for browsing/scraping, pandas for data analysis, and pillow for processing screenshots.\n\nYou will need to install [chromedriver](https://chromedriver.chromium.org/) to allow Selenium to control Chrome. **Persine won\'t work without it!**\n\n* **Installing chromedriver on OS X:** I hear you can install it [using homebrew](https://formulae.brew.sh/cask/chromedriver), but I\'ve never done it! You can also follow the link above and click the "latest stable release" link, then download `chromedriver_mac64.zip`. Unzip it, then move the `chromedriver` file into your `PATH`. I typically put it in `/usr/local/bin`.\n* **Installing chromedriver on Windows:** Follow the link above, click the "latest stable release" link. Download `chromedriver_win32.zip`, unzip it, and move `chromedriver.exe` into your `PATH` (in the spirit of anarchy I just put it in `C:\\Windows`).\n* **Installing chromedriver on Debian/Ubuntu:** Just run `apt install chromium-chromedriver` and it\'ll work.\n\n## Quickstart\n\nIn this example, we start a new session by visiting a YouTube video and clicking the "next up" video three times to see where it leads us. We then save the results for later analysis.\n\n```python\nfrom persine import PersonaEngine\n\nengine = PersonaEngine(headless=False)\n\nwith engine.persona() as persona:\n    persona.run("https://www.youtube.com/watch?v=hZw23sWlyG0")\n    persona.run("youtube:next_up#3")\n    persona.history.to_csv("history.csv")\n    persona.recommendations.to_csv("recs.csv")\n```\n\nWe turn off headless mode because it\'s fun to watch!\n',
    'author': 'Jonathan Soma',
    'author_email': 'jonathan.soma@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jsoma/persine',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.3',
}


setup(**setup_kwargs)
