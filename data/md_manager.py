import codecs


class MdManager:
    def __init__(self, md_config_dict, load_readme=True):

        if load_readme:
            try:
                self.readme = MdManager.load_markdown_file('README.md')
            except Exception:
                self.readme = 'Error loading readme file.'
                print(self.readme)

        for var_name, path in md_config_dict.items():
            setattr(self, var_name, MdManager.load_markdown_file(path))


    @classmethod
    def load_markdown_file(cls, path):
        with codecs.open(path, 'r', 'utf-8') as f:
            return f.read()

