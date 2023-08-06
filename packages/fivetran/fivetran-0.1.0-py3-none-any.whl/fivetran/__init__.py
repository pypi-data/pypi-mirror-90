__version__ = '0.1.0'

class Table:
    def __init__(self, name, primary_key=['id']):
        self.name         = name
        self.insert       = []
        self.delete       = []
        self._primary_key = primary_key
        
    def insert_record(self, record):
        self.insert.append(record)

    def delete_record(self, record):
        self.delete.append(record)

    def primary_key(self):
        return { "primary_key": self._primary_key }

class BaseConnector:
    def __init__(self, name, state, tables):
        self.name    = name
        self._state  = state or self._default_state()
        self._tables = tables

    def state(self):
        return self._state

    def insert(self):
        insert = {}
        for table in self._tables:
            insert[table.name] = table.insert
        return insert

    def delete(self):
        delete = {}
        for table in self._tables:
            delete[table.name] = table.delete
        return delete

    def schema(self):
        schema = {}
        for table in self._tables:
            schema[table.name] = table.primary_key()
        return schema

    def has_more(self):
        try:
            return self._state['has_more']
        except:
            raise KeyError(f'has_more missing from the state of {self.name}')

    def reset_state(self):
        raise NotImplementedError(f'Reset state not implemented for {self.name}')

    def _default_state(self):
        raise NotImplementedError(f'Default state not implemented for {self.name}')

    def _get_table(self, table_name):
        for table in self._tables:
            if table.name == table_name: return table
        return None

    def _insert_record(self, table, record):
        table.insert_record(record)

    def _delete_record(self, table, record):
        table.delete_record(record)