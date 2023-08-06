# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pelican', 'pelican.plugins.bibliography']

package_data = \
{'': ['*'], 'pelican.plugins.bibliography': ['data/templates/*']}

install_requires = \
['citeproc-py>=0.5.1,<0.6.0',
 'pelican>=4.5,<5.0',
 'pybtex>=0.23.0,<0.24.0',
 'pyyaml>=5.3,<6.0']

setup_kwargs = {
    'name': 'pelican-bibliography',
    'version': '0.4.0',
    'description': 'Generated bibliography in Pelican that can be rendered in references and citations',
    'long_description': '# Bibliography: A Plugin for Pelican\n\n[![Build Status](https://img.shields.io/github/workflow/status/micahjsmith/pelican-bibliography/build)](https://github.com/micahjsmith/pelican-bibliography/actions)\n[![PyPI Version](https://img.shields.io/pypi/v/pelican-bibliography)](https://pypi.org/project/pelican-bibliography/)\n![License](https://img.shields.io/pypi/l/pelican-bibliography?color=blue)\n\nGenerated bibliography in Pelican that can be rendered in references and citations\n\nThis plugin provides a new generator, `BibliographyGenerator`. This generator adds `bibliography` to the Pelican context and can write an output file for each reference using a `citation.html` template. Additionally, the entire bibliography can be written using a `bibliography.html` template or otherwise.\n\n## Installation\n\nThis plugin can be installed via:\n\n```\npip install pelican-bibliography\n```\n\nNow, add it to your `pelicanconf.py`:\n\n```\nPLUGINS = [\'pelican.plugins.bibliography\']\n```\n\nThat\'s it, thanks to the [namespace plugins](https://docs.getpelican.com/en/latest/plugins.html#how-to-use-plugins) in Pelican 4.5+.\n\n## Usage\n\nWhen this generator is run, it first reads bibliography files from the `BIBLIOGRAPHY_PATHS` setting. For now, only BibTeX (`.bib`) files are supported, but more may be added in the future. Each reference contained in the bibliography is instantiated as a `Reference` object. The content of the reference is its citation in bibtex, while most of the useful information is in the metadata, such as the citation key, the title, the authors, the publication venue. Extra metadata key-value pairs can be read from YAML files in the same bibliography path. Now, you can use `bibliography` in your templates.\n\nNext, the citations can be written to separate files. If desired, for each reference, the citation will be rendered according to the `citation.html` template and written to a configured path. Ideally, your bibliography will link to the citation page so that interested readers can easily cite your work.\n\n### Configuration\n\nThe following variables can be configured in your `pelicanconf.py`:\n\n```\n# A directory that contains the bibliography-related templates\nBIBLIOGRAPHY_TEMPLATES: Union[str, os.PathLike]\n\n# A list of directories and files to look at for bibliographies, relative to PATH.\nBIBLIOGRAPHY_PATHS: List[str]\n\n# A list of directories to exclude when looking for pages\nBIBLIOGRAPHY_EXCLUDES: List[str]\n\n# list of file extensions (without leading period) that are bibliography files\nBIBLIOGRAPHY_EXTENSIONS: List[str]\n\n# list of file extensions (without leading period) that are metadata files\nBIBLIOGRAPHY_METADATA_EXTENSIONS: List[str]\n\n# attribute of the Reference object to order the bibliography by (in reverse order)\nBIBLIOGRAPHY_ORDER_BY: str\n\n# whether to write citations to files\nBIBLIOGRAPHY_WRITE_CITATIONS: bool\n\n# template to use for citations\nBIBLIOGRAPHY_CITATION_TEMPLATE_NAME: str\n\n# path prefix to save citations as in generated site\nBIBLIOGRAPHY_CITATIONS_PATH: Union[str, os.PathLike]\n```\n\n### Bibliography page\n\nA main application of this is to create a research page that displays some collection of published research. For example, you could create a new template in your theme, `bibliography.html` that renders your research:\n\n```\nHere are the titles of my papers:\n<ul>\n    {% for ref in bibliography %}\n    <li>{{ ref.title }}</li>\n    {% endfor %}\n</ul>\n```\n\nYou can\'t just create your bibliography in your site\'s `content/`, because the context that includes the articles, pages, bibliography, etc. is not available when your content is read. What you can do is create a new template that extends `page.html` or `article.html`, and use that template to render some text in your content tree.\n\nA basic bibliography template is included with the plugin that tries to extend your theme\'s page template. Thus you could render your bibliography by adding this page to your content:\n\n```markdown\nTitle: My Bibliography\nTemplate: bibliography\n\nHere is my bibliography\n```\n\n### Extra metadata\n\nYou can also provide additional metadata in a YAML file with the following structure:\n```yaml\n- key: someCitationKey2020\n  metadata:\n    key1: value1\n    key2: value2\n```\n\nNow the keys and values in the metadata hash associated with the citation key will be available in the corresponding `ref.metadata` dictionary in the `bibliography`.\n\n### Styling\n\nThe `bibliography.html` default template that is included with the package has its own styling for jump links and highlighting. You can customize additional elements. For example, to style specific authors:\n\n```css\n.ref-author[data-family="Micah J."][data-family="Smith"] {\n    text-weight: bold;\n}\n```\n\nYou can use multiple selectors to apply styles to the `ref-author` span with data attributes matching a certain name.\n\n## Contributing\n\nContributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues](https://github.com/micahjsmith/pelican-bibliography/issues).\n\nTo start contributing to this plugin, review the [Contributing to Pelican](https://docs.getpelican.com/en/latest/contribute.html) documentation, beginning with the **Contributing Code** section.\n\n## License\n\nThis project is licensed under the MIT license.\n',
    'author': 'Micah Smith',
    'author_email': 'micahjsmith@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/micahjsmith/pelican-bibliography',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
