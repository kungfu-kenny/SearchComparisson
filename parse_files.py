import urllib
import requests
from pprint import pprint
from bs4 import BeautifulSoup
from multiprocessing import Pool
from fake_useragent import UserAgent

class ProduceSearches:
    """
    class which is dedicated to develop values for searching from browser
    """
    def __init__(self, value_list_search:list) -> None:
        self.value_list_search = value_list_search
        self.links_search = self.produce_links_search(value_list_search)

    def produce_links_search(self, value_list:list) -> list:
        """
        Method which is dedicated to produce links of the search
        Input:  value_list = 
        Output: list of lists which is dedicated to work with
        """
        return [
            [self.produce_link_google(f) for f in value_list],
            [self.produce_link_qwant(f) for f in value_list],
            [self.produce_link_bing(f) for f in value_list],
            [self.produce_link_duckduckgo(f) for f in value_list],
            [self.produce_link_yahoo(f) for f in value_list]
        ]
    
    def produce_link_google(self, value_search:str) -> str:
        """
        Method which is dedicated to produce search link of the Google
        Input:  value_search = link input which would be developed
        Output: link value for the request search
        """
        # https://www.google.com/search?channel=fs&client=ubuntu&q=a%24ap+rocky+testing
        for replace, replaced in [(' ', '+'), 
                                ('$', '%24')]:
            value_search = value_search.replace(replace, replaced)
        return ''.join(['https://www.google.com/search?',
                        'channel=fs&client=ubuntu&',
                        f'q={value_search}'])

    def produce_link_qwant(self, value_search:str) -> str:
        """
        Method which is dedicated to produce search link for the Qwant
        Input:  value_search = link input which would be developed
        Output: link value for the request search
        """
        # https://www.qwant.com/?q=a%24ap+rocky&t=web
        for replace, replaced in [(' ', '+'), 
                                ('$', '%24')]:
            value_search = value_search.replace(replace, replaced)
        return f'https://www.qwant.com/?q={value_search}&t=web'

    def produce_link_yahoo(self, value_search:str) -> str:
        """
        Method which is dedicated to develop values of the Yahoo search
        Input:  value_search = search words for it
        Output: we developed search link
        """
        for replace, replaced in [(' ', '+'), 
                                ('$', '%24')]:
            value_search = value_search.replace(replace, replaced)
        return ''.join(['https://search.yahoo.com/search;',
                        '_ylt=A2KLfSAI0V5h7z0AOIxXNyoA;',
                        '_ylc=X1MDMjc2NjY3OQRfcgMyBGZyA',
                        '3lmcC10BGZyMgNzYi10b3AEZ3ByaWQ',
                        'DcFkyVEFrN3VTZy5adHlqMGZuUmhKQ',
                        'QRuX3JzbHQDMARuX3N1Z2cDMTAEb3J',
                        'pZ2luA3NlYXJjaC55YWhvby5jb20Ec',
                        'G9zAzIEcHFzdHIDBHBxc3RybAMwBHF',
                        'zdHJsAzIwBHF1ZXJ5A2ElMjRhcCUyM',
                        'HJvY2t5JTIwbmV0JTIwd29ydGgEdF9',
                        'zdG1wAzE2MzM2MDM4NjQ-',
                        f'?p={value_search}&fr2=sb-top&fr=yfp-t'])

    def produce_link_bing(self, value_search:str) -> str:
        """
        Method which is dedicated to produce search link for the Bing
        Input:  value_search = link input which would be developed
        Output: link value for the request search
        """
        # https://www.bing.com/search?form=MOZLBR&pc=MOZI&q=a%24ap+rocky
        for replace, replaced in [(' ', '+'), 
                                ('$', '%24')]:
            value_search = value_search.replace(replace, replaced)
        return ''.join(['https://www.bing.com/',
                        'search?form=MOZLBR&pc=MOZI&',
                        f"q={value_search}"])

    def produce_link_duckduckgo(self, value_search:str) -> str:
        """
        Method which is dedicated to produce search link for the Duckduckgo
        Input:  value_search = search for the link which would be developed
        Output: link value for the request search
        """
        # https://duckduckgo.com/?t=ffab&q=a%24ap+rocky&ia=web
        for replace, replaced in [(' ', '+'), 
                                ('$', '%24')]:
            value_search = value_search.replace(replace, replaced)
        return ''.join(['https://duckduckgo.com/html?'
                        f"q={value_search}&pretty=1&no_html=1&skip_disambig=1"])
        
    @staticmethod
    def produce_html_text(value_list:set) -> str:
        """
        Static Method which is dedicated to make the html 
        Input:  value_link = link to search
                headers = value of the random headers
        Output: we returned text of the html
        """
        value_link, headers = value_list
        try:
            value_get = requests.get(value_link, headers=headers)
            if value_get.status_code == 200:
                return value_get.text
            return ''
        except Exception as e:
            print(e)
            print('#############################################')
            return ''

    def produce_parse_qwant(self, value_list:list) -> dict:
        """
        Methow which is dedicated to develop values of the 
        Input:  value_html = html value for the parsing values
                value_link = link which was previously parsed
        Output: we developed values for the search
        """
        value_html, value_link = value_list
        value_dict = {'search': value_link, 'names': [], 'links': []}
        if len(value_html) < 1000:
            return value_dict
        soup = BeautifulSoup(value_html, 'html.parser')
        value_article = soup.find_all('article', class_="web result")
        value_addon = [f.find('span', class_='ad') for f in value_article]
        value_addon = [True if f else False for f in value_addon]
        value_article = [article for article, check in zip(value_article, value_addon) if not check]
        value_names = [f.find('a').text.strip() for f in value_article]
        value_links = [f.find('p', class_='url').text.strip() for f in value_article]
        value_dict['names'] = value_names
        value_dict['links'] = value_links
        return value_dict

    def produce_parse_google(self, value_list:list) -> dict:
        """
        Method which is dedicated to parse values of the Google search
        Input:  value_html = html values of the parse
                value_link = link of the search which was created
        Output: we developed dictionary of the values
        """
        value_html, value_link = value_list
        value_dict = {'search': value_link, 'names': [], 'links': []}
        if len(value_html) < 1000:
            return value_dict
        soup = BeautifulSoup(value_html, 'html.parser')
        soup = soup.find_all('a')
        if not soup:
            try:
                value_html = self.produce_html_text([value_link, self.headers_random])
                return self.produce_parse_google([value_html, value_link])
            except Exception as e:
                print(e)
                print('===========================================================')
                return value_dict
        value_links = [f.get('href') for f in soup]
        value_names = [f.find('h3') for f in soup]
        value_links = [f for f, n in zip(value_links, value_names) if n]
        value_names = [f for f in value_names if f]
        value_names = [f.text for f in value_names if f]
        value_links = [f.split('=') for f in value_links]
        value_search = []
        for link in value_links:
            for i, search in enumerate(link[::-1]):
                if 'url' in search:
                    value_search.append(len(link) - i)
        value_links = [f[index] for f, index in zip(value_links, value_search)]
        value_links = [''.join(f.split('&')[:-1]) for f in value_links]
        value_links = [f.replace("%3Fv%3D", '?v=') if 'https://www.youtube.com/watch' 
                                    in f else f for f in value_links]
        value_dict['names'] = value_names
        value_dict['links'] = value_links
        return value_dict

    def produce_parse_duckduckgo(self, value_list:list) -> dict:
        """
        Method which is dedicated to create values of the parsed links from duckduckgo
        Input:  value_html = html value of the parsed link
                value_link = link which was previously used
        Output: dictionary of used links
        """
        value_html, value_link = value_list
        value_dict = {'search': value_link, 'names': [], 'links': []}
        if len(value_html) < 1000:
            return value_dict
        soup = BeautifulSoup(value_html, 'html.parser')
        soup = soup.find('div', id='links')
        soup = soup.find_all('h2')
        value_name = [f.text.strip() for f in soup]
        value_link = [f.find('a').get('href', '') for f in soup]
        value_dict['names'] = value_name
        value_dict['links'] = value_link
        return value_dict

    def produce_parse_yahoo(self, value_list:list) -> dict:
        """
        Method which is dedicated to parse Yahoo values for it
        Input:  value_html = html values for the parsing
                value_link = link value of the parsed value
        Output: dictionary with the previously parsed values
        """
        value_html, value_link = value_list
        value_dict = {'search': value_link, 'names': [], 'links': []}
        if len(value_html) < 1000:
            return value_dict
        soup = BeautifulSoup(value_html, 'html.parser')
        soup = soup.find('div', id='results')
        soup = soup.find('div', id='left')
        soup = soup.find('ol')
        if not soup:
            try:
                value_html = self.produce_html_text([value_link, self.headers_random])
                return self.produce_parse_yahoo([value_html, value_link])
            except Exception as e:
                print(e)
                print('===========================================================')
                return value_dict
        soup = soup.find_all('h3', class_='title tc')
        value_name = [f.find('a').text for f in soup]
        value_link_span = [f.find('span') for f in soup]
        value_between_link = [f.find('span') for f in value_link_span]
        value_between_link = [f.text if f else '' for f in value_between_link]
        value_links = [f.text.split(b)[0] if f and b else f.text 
                        for f, b in zip(value_link_span, value_between_link)]
        value_names = [f.split(b)[-1] if f and b else f 
                        for f, b in zip(value_name, value_links)]
        value_names = [f.split(b)[-1] if f and b else f 
                        for f, b in zip(value_names, value_between_link)]
        value_links = [f.get('href') for f in [f.find('a') for f in soup]]
        value_links = [f.split('/') for f in value_links]
        value_links = [f[7].split('=')[1] for f in value_links]
        value_links = [urllib.parse.unquote(f) for f in value_links]
        value_dict['names'] = value_names
        value_dict['links'] = value_links
        return value_dict
        
    def produce_parse_bing(self, value_list:list) -> dict:
        """
        Method which is dedicated to parse Bing values
        Input:  value_html = html values
                value_link = link for the parsing
        Output: dictionaries with names and links
        """
        value_html, value_link = value_list
        value_dict = {'search': value_link, 'names': [], 'links': []}
        if len(value_html) < 1000:
            return value_dict
        soup = BeautifulSoup(value_html, 'html.parser')
        soup = soup.find('div', id='b_content')
        soup = soup.find('ol', id='b_results')
        value_search = soup.find_all('li', class_='b_algo')
        if not value_search:
            try:
                value_html = self.produce_html_text([value_link, self.headers_random])
                return self.produce_parse_bing([value_html, value_link])
            except Exception as e:
                print(e)
                print('===========================================================')
                return value_dict
        value_title = [f.find('h2') for f in value_search]
        value_names = [f.text for f in value_title]
        value_links = [f.find('a').get('href', '') for f in value_title]
        value_dict['names'] = value_names
        value_dict['links'] = value_links
        return value_dict

    def produce_main(self) -> list:
        """
        Method which is dedicated to create values of the 
        Input:  None
        Output: list with values of the parsed search engines
        """
        self.headers_random = {'user-agent': UserAgent().random,}
        links_google, links_qwant, links_bing, \
            links_duckduckgo, links_yahoo = self.links_search
        value_google = [[rand, self.headers_random] for rand in links_google]
        value_qwant = [[rand, self.headers_random] for rand in links_qwant]
        value_bing = [[rand, self.headers_random] for rand in links_bing]
        value_duckduckgo = [[rand, self.headers_random] for rand in links_duckduckgo]
        value_yahoo = [[rand, self.headers_random] for rand in links_yahoo]
        
        with Pool(5) as pool:
            value_html_google = pool.map(self.produce_html_text, value_google)
            value_html_qwant = pool.map(self.produce_html_text, value_qwant)
            value_html_bing = pool.map(self.produce_html_text, value_bing)
            value_html_duckduckgo = pool.map(self.produce_html_text, value_duckduckgo)
            value_html_yahoo = pool.map(self.produce_html_text, value_yahoo)

        value_google = [[html, link] for html, link in zip(value_html_google, links_google)]
        value_qwant = [[html, link] for html, link in zip(value_html_qwant, links_qwant)]
        value_bing = [[html, link] for html, link in zip(value_html_bing, links_bing)]
        value_duckduckgo = [[html, link] for html, link in zip(value_html_duckduckgo, links_duckduckgo)]
        value_yahoo = [[html, link] for html, link in zip(value_html_yahoo, links_yahoo)]
        
        with Pool(5) as pool:
            value_dict_google = pool.map(self.produce_parse_google, value_google)
            value_dict_qwant = pool.map(self.produce_parse_qwant, value_qwant)
            value_dict_bing = pool.map(self.produce_parse_bing, value_bing)
            value_dict_duckduckgo = pool.map(self.produce_parse_duckduckgo, value_duckduckgo)
            value_dict_yahoo = pool.map(self.produce_parse_yahoo, value_yahoo)
        
        return value_dict_google, value_dict_qwant, value_dict_bing, \
                value_dict_duckduckgo, value_dict_yahoo
        
if __name__ == '__main__':
    a = ProduceSearches(['a$ap rocky', 'rihanna'])
    a.produce_main()