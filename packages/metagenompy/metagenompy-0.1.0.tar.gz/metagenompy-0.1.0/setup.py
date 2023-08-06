# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['metagenompy']

package_data = \
{'': ['*']}

install_requires = \
['ipython>=7.19.0,<8.0.0',
 'matplotlib>=3.3.3,<4.0.0',
 'networkx>=2.5,<3.0',
 'pandas>=1.2.0,<2.0.0',
 'tqdm>=4.55.1,<5.0.0']

setup_kwargs = {
    'name': 'metagenompy',
    'version': '0.1.0',
    'description': 'Your all-inclusive package for aggregating and visualizing metagenomic BLAST results.',
    'long_description': "# metagenompy\n\nYour all-inclusive package for aggregating and visualizing metagenomic BLAST results.\n\n\n## Installation\n\n```bash\n$ pip install metagenompy\n```\n\n\n## Usage\n\n### NCBI taxonomy as NetworkX object\n\nThe core of `metagenompy` is a taxonomy as a networkX object.\nThis means that all your favorite algorithms work right out of the box.\n\n```python\nimport metagenompy\nimport networkx as nx\n\n\n# load taxonomy\ngraph = metagenompy.generate_taxonomy_network()\n\n# print path from human to pineapple\nfor node in nx.shortest_path(graph.to_undirected(as_view=True), '9606', '4615'):\n    print(node, graph.nodes[node])\n## 9606 {'rank': 'species', 'scientific_name': 'Homo sapiens', 'common_name': 'human'}\n## 9605 {'rank': 'genus', 'scientific_name': 'Homo'}\n## [..]\n## 4614 {'rank': 'genus', 'scientific_name': 'Ananas'}\n## 4615 {'rank': 'species', 'scientific_name': 'Ananas comosus', 'common_name': 'pineapple'}\n```\n\n### Easy transformation and visualization of taxonomy\n\n`metagenompy`, e.g., allows you to quickly extract taxonomic entities of interest and visualize their relations.\n\n```python\nimport metagenompy\nimport matplotlib.pyplot as plt\n\n\n# load and condense taxonomy to relevant ranks\ngraph = metagenompy.generate_taxonomy_network()\nmetagenompy.condense_taxonomy(graph)\n\n# highlight interesting nodes\ngraph_zoom = metagenompy.highlight_nodes(graph, [\n    '9606',  # human\n    '9685',  # cat\n    '9615',  # dog\n    '4615',  # pineapple\n    '3747',  # strawberry\n    '4113',  # potato\n])\n\n# visualize result\nfig, ax = plt.subplots(figsize=(10, 10))\nmetagenompy.plot_taxonomy(graph_zoom, ax=ax, labels_kws=dict(font_size=10))\nfig.tight_layout()\nfig.savefig('taxonomy.pdf')\n```\n\n![Exemplary taxonomy](gallery/taxonomy.png)\n",
    'author': 'kpj',
    'author_email': 'kim.philipp.jablonski@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kpj/metagenompy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
