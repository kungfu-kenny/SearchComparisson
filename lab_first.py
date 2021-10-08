from pprint import pprint
from parse_files import ProduceSearches


class LabFirst:
    """
    class which is dedicated to return all results from the labs
    """
    def __init__(self, value_list:list) -> None:
        self.search = ProduceSearches(value_list)
        self.search_list = self.search.produce_main()

    def make_aggregation_board(self) -> list:
        """
        Method which is dedicated to return values of the aggregation
        Input:  value_list
        Output: we created values of the 
        """
        pass

    def produce_main(self) -> None:
        """
        Method which is dedicated to produce main values of the results
        Input:  All used values
        Output:
        """
        pprint(self.search_list)


if __name__ == '__main__':
    a = LabFirst(['тестування'])#, 'rihanna', 'tyler the creator', 'kendrick lamar', 'killer mike'])
    a.produce_main()