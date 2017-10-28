import unittest
from TsqlParser import Parser


class TestTsqlParser(unittest.TestCase):

    def test_status(self):
        p = Parser(input_data='SELECT c1,c2 FROM tab1', type=2)
        self.assertTrue(p.status)

    def test_to_string(self):
        p = Parser(input_data='SELECT c1,c2 FROM tab1', type=2)
        self.assertEqual(p.to_string(), '(tsql_file (batch (sql_clauses '
                                        '(sql_clause (dml_clause (select_statement '
                                        '(query_expression (query_specification SELECT '
                                        '(select_list (select_list_elem (expression (full_column_name '
                                        '(id (simple_id c1))))) , (select_list_elem (expression (full_column_name '
                                        '(id (simple_id c2)))))) FROM (table_sources (table_source '
                                        '(table_source_item_joined (table_source_item (table_name_with_hint '
                                        '(table_name (id (simple_id tab1))))))))))))))) <EOF>)')
if __name__ == '__main__':
    unittest.main()

