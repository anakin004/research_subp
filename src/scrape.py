from bs4 import BeautifulSoup as bs
import requests as re





def get_web_content(url, headers=None):

    """ gets html content from a website using BeautifulSoup """
    """ also, has optional headers incase there is some bot detection on websites """

    try:

        response = re.get(url, headers=headers)
        
        
        # if successful
        if response.status_code == 200:    
            web_content = bs(response.content, 'html.parser')
            return web_content

        else:
            print(f"Failed to retrieve web content, status code {response.status_code}")
            return None
        
    except Exception as e:
        print(f"Error: {e}")
        return None


# a wrapper for now, might add more to it
def get_tables_from_bs4(web_content):

    """ Excepts web_content to be a beatifulsoup object """
    """ returns the tables from the web content return from get_web_content or a bs html object """

    tables = web_content.find_all('table')
    return tables   

def get_formatted_for_syzkaller(table_data):
    """returns the table data formatted for syzkaller, with a new line every 4 cells"""
    """on syzkaller db, the meaningful data seems to be in seperate rows, but is treated as one row"""

    content = ""

    # for syzkaller db, only the last row parsed from bs4 matters
    row = table_data[-1]
    

    # note ...
    # <td> defines data in a cell in a row, <tr> defines a row of a table, <table> for entire table

    cells = row.find_all('td') 
    

    if cells:
        # collecting the cell text, strip extra spaces, and put them in a list
        cell_texts = []
        for cell in cells:
            cell_texts.append(cell.text.strip())
            
        # print the cells in chunks of 4, separated by ' | ', then add a newline
        for i in range(0, len(cell_texts), 4):
            row_str = ' | '.join(cell_texts[i:i+4]) + '\n'
            content += row_str
    
    return content 


