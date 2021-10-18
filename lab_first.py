import re
import requests
from pprint import pprint
from parse_files import ProduceSearches


class LabFirst:
    """
    class which is dedicated to return all results from the labs
    """
    def __init__(self, value_list:list) -> None:
        self.search = ProduceSearches(value_list)
        self.search_list = self.produce_additional_sorting(
                                self.search.produce_main())
        self.search_links = self.produce_lists_every_values()

    def produce_lists_every_values(self) -> list:
        """
        Method which is dedicated to produce values of the 
        Input:  produced values of the lists
        Output: developed values for the search of it
        """
        value_lists = []
        for search_list in list(zip(*self.search_list)):
            value_list = []
            for search_links in search_list:
                value_list.extend(search_links.get('links', []))
            value_lists.append(value_list)
        value_lists = [list(set(f)) for f in value_lists]
        return value_lists

    @staticmethod
    def produce_additional_sorting(search_list:list) -> list:
        """
        Method which is dedicated to work with created values
        Input:  search_list = search list which was got from the parsing
        Output: we developed fully working links for it
        """
        regex = re.compile(r'^(?:http|ftp)s?://'
                    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
                    r'localhost|'
                    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
                    r'(?::\d+)?'
                    r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        for search_object in search_list:
            for search_browser in search_object:
                value_list_status = [re.match(regex, f) is not None for f in search_browser.get('links', [])]
                search_browser['links'] = [f for f, f_bool in zip(
                                    search_browser.get('links', []), value_list_status) if f_bool]
                search_browser['names'] = [f for f, f_bool in zip(
                                    search_browser.get('names', []), value_list_status) if f_bool]
        return search_list

    def make_aggregation_board(self) -> list:
        """
        Method which is dedicated to return values of the aggregation
        Input:  None
        Output: we created values of the 
        """
        value_lists = list(zip(*self.search_list))
        return 

    def produce_main(self) -> None:
        """
        Method which is dedicated to produce main values of the results
        Input:  All used values
        Output:
        """
        self.make_aggregation_board()


if __name__ == '__main__':
    a = LabFirst(['a$ap rocky', 'rihanna', 'tyler the creator', 'kendrick lamar', 'killer mike'])
    a.produce_main()