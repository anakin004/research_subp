from scrape import get_web_content, get_tables_from_bs4, get_formatted_for_syzkaller, get_formatted_for_cve_db
from save_content import save_to_file

syz_url = "https://syzkaller.appspot.com/upstream/subsystems"
cve_db_url = "https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=linux+kernel"

#change for website
web_content = get_web_content(cve_db_url)

if web_content:
    
    table_data = get_tables_from_bs4(web_content)

    # for syzkaller, already ran so commented out
    #content = get_formatted_for_syzkaller(table_data)
    #save_to_file(content, "scraped_data/syzkaller_db.txt")

    content = get_formatted_for_cve_db(table_data)
    save_to_file(content, "scraped_data/cve_db.txt")
