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
        
        # put the cells in chunks of 4, separated by ' | ', then add a newline
        cell_texts = []
        

        for i in range(0, len(cells), 4):

            for j in range(4):
                cell_texts.append(cells[i+j].text.strip())
            
            # Join the 4 cell texts with ' | ' and add a newline
            row_str = ' | '.join(cell_texts) + '\n'
            content += row_str
            cell_texts = []  
    
    return content

def get_formatted_for_cve_db(table_data):
        
    content = ""

    # cve db treats all cve bugs in table as one row, the row being the third row on the webpage html
    row = table_data[2]
    cells = row.find_all('td')

    # group cells by two
    for i in range(0, len(cells), 2):
        
        formatted_cell1_text = cells[i].text.strip()
        formatted_cell2_text = cells[i+1].text.strip()

        # the delimeter matters here since the description of cve bug can have characters like | that was used for syzkaller scrape
        # substrings like "||", "->" and "::" exist in some of the text so one needs to found in order to efficiently parse data
        # I ran a script to find the substring ":::" in any of the cells and there wasnt any so ::: is the designated delimeter
        content += f"{formatted_cell1_text} ::: {formatted_cell2_text}\n"

    return content



