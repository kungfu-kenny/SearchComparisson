import re
import random
from pprint import pprint
from parse_files import ProduceSearches


class LabFirst:
    """
    class which is dedicated to return all results from the labs
    """
    def __init__(self, value_list:list) -> None:
        self.inserted_list = value_list
        self.x_1, self.x_2, self.outer_mark = 0.44, 0.56, 0.64
        self.objective_mark, self.self_mark = 0.5, 0.75
        self.search = ProduceSearches(self.inserted_list)
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
        Output: we created values of the modified board values which were further parsed
        """
        value_lists = list(zip(*self.search_list))
        value_len = [[len(f.get('links', [])) for f in k] for k in value_lists]
        value_len_max = [max(i) for i in value_len]
        value_result = []
        for value_list, link_list in zip(value_lists[:], self.search_links[:]):
            value_list_presence = []
            for value_links_dict in value_list:
                value_links = value_links_dict.get('links', [])
                value_link_presence = []
                for value_link in link_list:
                    if value_link in value_links:
                        value_link_presence.append(value_links.index(value_link))
                    else:
                        value_link_presence.append(-1)
                value_list_presence.append(value_link_presence) 
            value_result.append(value_list_presence)
        value_presence = []
        for value_searched_list, value_max in zip(value_result, value_len_max):
            value_presence_artist = []
            for value_artist_list in value_searched_list:
                value_presence_link = []
                for value_index in value_artist_list:
                    if value_index >= 0:
                        value_presence_link.append(value_max-value_index)
                    else:
                        value_presence_link.append(0)
                value_presence_artist.append(value_presence_link)
            value_presence.append(value_presence_artist)
        value_results = []
        for value_links, values_sums in zip(self.search_links, value_presence):
            value_dict_sums = {i:0 for i in value_links}
            for values_sum in values_sums:
                for i, s in zip(value_links, values_sum):
                    value_dict_sums[i] = value_dict_sums[i] + s
            value_results.append([f for f, _ in sorted(value_dict_sums.items(), 
                            reverse=True, key=lambda item: item[1])])
        return value_results
        
    def make_aggregation_condorse(self) -> list:
        """
        Method which is dedicated to produce condorce aggregation of the values
        Input:  None
        Output: we created values of the condorse values which were further parsed
        """
        value_lists = list(zip(*self.search_list))
        value_len = [[len(f.get('links', [])) for f in k] for k in value_lists]
        value_len_max = [max(i) for i in value_len]
        value_result = []
        for value_list, link_list in zip(value_lists[:], self.search_links[:]):
            value_list_presence = []
            for value_links_dict in value_list:
                value_links = value_links_dict.get('links', [])
                value_link_presence = []
                for value_link in link_list:
                    if value_link in value_links:
                        value_link_presence.append(value_links.index(value_link))
                    else:
                        value_link_presence.append(-1)
                value_list_presence.append(value_link_presence) 
            value_result.append(value_list_presence)
        value_presence = []
        for value_searched_list, value_max in zip(value_result, value_len_max):
            value_presence_artist = []
            for value_artist_list in value_searched_list:
                value_presence_link = []
                for value_index in value_artist_list:
                    if value_index >= 0:
                        value_presence_link.append(value_max-value_index)
                    else:
                        value_presence_link.append(0)
                value_presence_artist.append(value_presence_link)
            value_presence.append(value_presence_artist)
        value_order = []
        for value_searched_types, value_searched in zip(value_presence, self.search_links):
            value_max, value_max_link = 0, 0
            value_list = []
            value_searched_type = value_searched.copy()
            while len(value_searched_type) > 1:
                for i, _ in enumerate(value_searched_type):
                    for j, _ in enumerate(value_searched_type):
                        if i != j:
                            value_a = sum([k[i] for k in value_searched_types])
                            value_b = sum([k[j] for k in value_searched_types])
                            value_max_el, value_max_v = (i, value_a) if value_a > value_b else (j, value_b)
                            if value_max_v > value_max:
                                value_max = value_max_v
                                value_max_link = value_max_el
                max_link = value_searched_type.pop(value_max_link)  
                value_max = 0
                value_list.append(max_link)
            value_list.append(value_searched_type[0])
            value_order.append(value_list)
        return value_order

    def produce_weights_statistic(self, value_list:list=[]) -> list:
        """
        Method which is dedicated to produce relevant values
        Input:  value_list = list values which were developed of the aggregation
        Output: we developed answer of relevant weights
        """
        if not value_list:
            value_list = self.make_aggregation_board()
        value_relevancy = [
            [
                1 if name_inserted.lower() in search.lower() else random.random() for search in value_search
            ] for value_search, name_inserted in zip(value_list, self.inserted_list)]
        v_list = [[f/sum(search) for f in search] for search in value_relevancy]
        o_list = [[f/sum([f for f in search if f > 0.5]) for f in search] for search in value_relevancy]
        subjective_marks = self.produce_subjective_marks(value_relevancy, value_list)
        v_list_mean = [sum(f)/len(f) for f in v_list]
        x_list = [sum((f-mean)**2/(len(v_list)- 1) for f in v) 
                                        if len(v_list) > 1 else 0 for v, mean in zip(v_list, v_list_mean)]
        list_weights_unnormed = [[rel*(x_1*o + (1-x_1)*v) for v, o, rel in zip(search_v, search_o, search_rel)] 
                for search_v, search_o, search_rel, x_1 in zip(v_list, o_list, subjective_marks, x_list)]
        list_weights = [[weight/sum(weights) for weight in weights] for weights in list_weights_unnormed]
        return list_weights

    def produce_relevancy(self) -> list:
        """
        Method which is dedicated to produce the exspert relevancy of the selected values
        Input:  all calculated values from the search
        Outpyt: we developed values of the 
        """
        value_list = list(zip(*self.search_list))
        list_relevancy = []
        for value_searches, value_inserted in zip(value_list, self.inserted_list):
            list_record = []
            for value_search in value_searches:
                value_created_rel = []
                for value_link in value_search.get('names', []):
                    if value_inserted.lower() in value_link.lower():
                        value_created_rel.append(1)
                    else:
                        value_created_rel.append(random.random())
                list_record.append(value_created_rel)
            list_relevancy.append(list_record)
        return list_relevancy
    
    def produce_subjective_marks(self, value_relevancy:list, value_links:list) -> list:
        """
        Method which is dedicated to produce values of the subjective mark, based on
        Input:  value_relevancy = relevant values of calculation
                value_links = list of the links
        Output: we developed values of the subjective marks
        """
        def get_rand_int(inserted:float) -> float:
            if inserted <= 0.04:
                return inserted*12.5
            if 0.04 < inserted <= 0.06:
                return 0.65
            return 0.7
        list_marks_prev = [[get_rand_int(i) for i in rel] for rel in value_relevancy] 
        list_marks = []
        for value_searches, links, searched in zip(list_marks_prev, value_links, self.inserted_list):
            list_mark = []
            for prev_mark, prev_link  in zip(value_searches, links):
                if 'youtube' not in prev_link:
                        prev_mark += 0.1
                if ''.join(e for e in searched if e.isalnum()).lower() \
                        in ''.join(e for e in prev_link if e.isalnum()).lower():
                    prev_mark += 0.1
                list_mark.append(prev_mark)
            list_marks.append(list_mark)
        return list_marks

    def produce_weights(self, value_list:list=[]) -> float:
        """
        Method which is dedicated to develop weights of the experts
        Input:  value_list = calculated values of it
        Output: we developed the formula of the kompetency of the experts
        """
        if not value_list:
            value_list = self.make_aggregation_board()
        value_relevancy = [
            [
                1 if name_inserted.lower() in search.lower() else random.random() for search in value_search
            ] for value_search, name_inserted in zip(value_list, self.inserted_list)]
        v_list = [[f/sum(search) for f in search] for search in value_relevancy]
        o_list = [[f/sum([f for f in search if f > 0.5]) for f in search] for search in value_relevancy]
        subjective_marks = self.produce_subjective_marks(value_relevancy, value_list)
        list_weights_unnormed = [[rel*(self.x_1*o + self.x_2*v) for v, o, rel in zip(search_v, search_o, search_rel)] 
                for search_v, search_o, search_rel in zip(v_list, o_list, subjective_marks)]
        list_weights = [[weight/sum(weights) for weight in weights] for weights in list_weights_unnormed]
        return list_weights
        
    def produce_main(self) -> None:
        """
        Method which is dedicated to produce main values of the results
        Input:  All used values
        Output: selected values which was previously neccessary
        """
        value_order_board = self.make_aggregation_board()
        value_order_condorse = self.make_aggregation_condorse()
        weights_board = self.produce_weights(value_order_board)
        weights_condorse = self.produce_weights(value_order_condorse)
        weights_board_mod = self.produce_weights_statistic(value_order_board)
        weights_condorse_mod = self.produce_weights_statistic(value_order_condorse)
        return self.search_list, weights_board, weights_condorse, weights_board_mod, weights_condorse_mod
        

if __name__ == '__main__':
    a = LabFirst(['a$ap rocky', 'rihanna', 'tyler the creator', 'kendrick lamar', 'killer mike'])
    a.produce_main()