# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['metagenompy']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3.3,<4.0.0',
 'networkx>=2.5,<3.0',
 'numpy>=1.19.5,<2.0.0',
 'pandas>=1.2.0,<2.0.0',
 'tqdm>=4.55.1,<5.0.0']

setup_kwargs = {
    'name': 'metagenompy',
    'version': '0.4.1',
    'description': 'Your all-inclusive package for aggregating and visualizing metagenomic BLAST results.',
    'long_description': '# metagenompy\n\n[![PyPI](https://img.shields.io/pypi/v/metagenompy.svg?style=flat)](https://pypi.python.org/pypi/metagenompy)\n[![Tests](https://github.com/kpj/metagenompy/workflows/Tests/badge.svg)](https://github.com/kpj/metagenompy/actions)\n\nYour all-inclusive package for aggregating and visualizing metagenomic BLAST results.\n\n\n## Installation\n\n```bash\n$ pip install metagenompy\n```\n\n\n## Usage\n\n### Summary statistics for BLAST results\n\nAfter blasting your reads against a [sequence database](ftp://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/), generating summary reports using `metagenompy` is a blast.\n\n```python\nimport metagenompy\n\n\n# read BLAST results file with columns \'qseqid\' and \'staxids\'\ndf = (pd.read_csv(\'blast_result.csv\')\n        .set_index(\'qseqid\')[\'staxids\']\n        .str.split(\';\')\n        .explode()\n        .dropna()\n        .reset_index()\n        .rename(columns={\'staxids\': \'taxid\'})\n)\n\ndf.head()\n##    qseqid    taxid\n## 0   read1   648716\n## 1   read1  1797690\n## 2   read1  1817827\n## 3   read1  2580422\n## 4   read1     1451\n\n# classify taxons at multiple ranks\nrank_list = [\'species\', \'genus\', \'class\', \'superkingdom\']\ndf = metagenompy.classify_dataframe(\n    graph, df,\n    rank_list=rank_list\n)\n\n# aggregate read matches\nagg_rank = \'genus\'\ndf_agg = metagenompy.aggregate_classifications(df, agg_rank)\n\ndf_agg.head()\n##         taxid                   species            genus            class superkingdom\n## qseqid\n## read1    <NA>                      <NA>             <NA>             <NA>         <NA>\n## read2   36035  Saccharomycodes ludwigii  Saccharomycodes  Saccharomycetes    Eukaryota\n## read3    1352      Enterococcus faecium     Enterococcus          Bacilli     Bacteria\n## read4    1352      Enterococcus faecium     Enterococcus          Bacilli     Bacteria\n## read5    1352      Enterococcus faecium     Enterococcus          Bacilli     Bacteria\n\n# visualize outcome\nmetagenompy.plot_piechart(df_agg)\n```\n\n<img src="gallery/piechart.png" width="50%">\n\n### NCBI taxonomy as NetworkX object\n\nThe core of `metagenompy` is a taxonomy as a networkX object.\nThis means that all your favorite algorithms work right out of the box.\n\n```python\nimport metagenompy\nimport networkx as nx\n\n\n# load taxonomy\ngraph = metagenompy.generate_taxonomy_network()\n\n# print path from human to pineapple\nfor node in nx.shortest_path(graph.to_undirected(as_view=True), \'9606\', \'4615\'):\n    print(node, graph.nodes[node])\n## 9606 {\'rank\': \'species\', \'authority\': \'Homo sapiens Linnaeus, 1758\', \'scientific_name\': \'Homo sapiens\', \'genbank_common_name\': \'human\', \'common_name\': \'man\'}\n## 9605 {\'rank\': \'genus\', \'authority\': \'Homo Linnaeus, 1758\', \'scientific_name\': \'Homo\', \'common_name\': \'humans\'}\n## [..]\n## 4614 {\'rank\': \'genus\', \'authority\': \'Ananas Mill., 1754\', \'scientific_name\': \'Ananas\'}\n## 4615 {\'rank\': \'species\', \'authority\': [\'Ananas comosus (L.) Merr., 1917\', \'Ananas lucidus Mill., 1754\'], \'scientific_name\': \'Ananas comosus\', \'synonym\': [\'Ananas comosus var. comosus\', \'Ananas lucidus\'], \'genbank_common_name\': \'pineapple\'}\n```\n\n### Easy transformation and visualization of taxonomic tree\n\nExtract taxonomic entities of interest and visualize their relations:\n\n```python\nimport metagenompy\nimport matplotlib.pyplot as plt\n\n\n# load and condense taxonomy to relevant ranks\ngraph = metagenompy.generate_taxonomy_network()\nmetagenompy.condense_taxonomy(graph)\n\n# highlight interesting nodes\ngraph_zoom = metagenompy.highlight_nodes(graph, [\n    \'9606\',  # human\n    \'9685\',  # cat\n    \'9615\',  # dog\n    \'4615\',  # pineapple\n    \'3747\',  # strawberry\n    \'4113\',  # potato\n])\n\n# visualize result\nfig, ax = plt.subplots(figsize=(10, 10))\nmetagenompy.plot_network(graph_zoom, ax=ax, labels_kws=dict(font_size=10))\nfig.tight_layout()\nfig.savefig(\'taxonomy.pdf\')\n```\n\n<img src="gallery/network.png" width="50%">\n',
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
