import pandas as pd


class DfManager:
    """
    Class used to hold the dataframes used by the app in a single object.

    The object can be created in dashapp.__init__ and imported in modules when needed. A doc file outlining each loaded
    df's general properties is also generated (useful as a quick reference for column names, shapes, etc).

    Relies on a {'DF_NAME': df_path} str:pathlike mapping defined in config.py
    Alternatively, the format can be {'DF_NAME': (df_path, 'doc')}, where values are tuples consisting of a path and a
    str documenting or describing the df.

    Each DF_NAME key will be added to the DfManager object as an instance variable pointing to the corresponding df
    loaded from disk.

    For example, assuming DM is a DfManager object initiated with df_config_dict={'TEST_DF': 'test_df.p'},
    DM.TEST_DF will point to the loaded df.
    """

    def __init__(self, df_config_dict, update_doc=True):

        self.df_data = {}

        for var_name, info in df_config_dict.items():
            if type(info) == tuple:
                path = info[0]
                doc = info[1]
            else:
                path = info
                doc = ''

            setattr(self, var_name, DfManager.load_df_from_pickle(path))
            self.df_data[var_name] = doc

        print(f'Successfully loaded {len(self.df_names)} dfs: {", ".join(n for n in self.df_names)}')
        self.doc_md = self.make_df_doc_file()
        if update_doc:
            self.save_doc_file()

    def make_df_doc_file(self, max_len=30):
        title = 'Dataframe Doc\n======\n\n'
        subtitle = f'Loaded {len(self.df_names)} dataframes:\n\n'

        names_list = f'\n'.join(f'* {n} {"-" * (len(d) > 0)} {d}' for n, d in self.df_data.items()) + '\n\n'

        details = []

        for df_name, df_doc in self.df_data.items():
            df = getattr(self, df_name)

            s = f'{df_name}\n---\n\n'
            s += f'##### **Description:** {df_doc}\n\n' * (len(df_doc) > 0)
            s += f'Rows: {len(df)}, Columns: {len(df.columns)}, Total values: {df.size}\n\n'

            s += f'Index ({max_len} first): ' + ', '.join(str(i) for i in df.index[:max_len]) + '\n\n'
            s += f'Columns ({max_len} first): ' + ', '.join(str(c) for c in df.columns[:max_len]) + '\n\n'

            details.append(s)

        return title + subtitle + names_list + '\n\n'.join(d for d in details)

    def save_doc_file(self, path='df_doc.md'):
        with open(path, 'w') as f:
            f.write(self.doc_md)

    @property
    def df_names(self):
        return self.df_data.keys()

    @classmethod
    def load_df_from_pickle(cls, path):
        return pd.read_pickle(path)

