from scrape import get_web_content, get_tables_from_bs4, get_formatted_for_syzkaller
from save_content import save_to_file

url = "https://syzkaller.appspot.com/upstream/subsystems"
web_content = get_web_content(url)

if web_content:
    table_data = get_tables_from_bs4(web_content)
    content = get_formatted_for_syzkaller(table_data)
    save_to_file(content, "scraped_data/syzkaller_db.txt")
