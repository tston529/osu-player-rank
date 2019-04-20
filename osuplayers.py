from urllib.request import urlopen
import urllib.parse
from bs4 import BeautifulSoup
import sys

def get_player_count(url):
    """
    @brief      Parses the total active player counts for a given page
    
    @param      url   string; the url of the page of player counts to scrape
    
    @return     int; The player count.
    """
    page = urlopen(url)

    soup = BeautifulSoup(page, features="html.parser")

    table_divs = soup.findAll('td', attrs={'class': 'ranking-page-table__column ranking-page-table__column--dimmed'})

    sum = 0
    for i in range(len(table_divs)//5):
        sum += int((table_divs[i*5].text).strip().replace(',', ''))
    return sum


def calc_rank(id=13197473):
    """
    @brief      Scrapes and parses the rank of the given player

    @param      id   int; the unique id of the desired player [default: my id :-) ]
    
    @return     The player's rank.
    """
    player_url = urllib.parse.urlparse("http://osu.ppy.sh/pages/include/profile-general.php?u=player_id&m=0".replace('player_id', str(id)))
    page = urlopen(player_url.geturl())
    soup = BeautifulSoup(page, features="html.parser")
    table_divs = soup.findAll('div', attrs={'class': 'profileStatLine'})

    import re
    pattern = '\(#\d*,*\d+\)'
    for div in table_divs:
        for childdiv in div.find_all('b'):
            result = re.search(pattern, str(childdiv.text))
            my_ranking = int(result.group(0).replace(',', '').replace("(#", '').replace(")", ''))
            break
        break
    return my_ranking


def main():
    
    player_id = 13197473
    if len(sys.argv) == 2:
        player_id = int(sys.argv[1])

    my_ranking = -1
    total_players = 0
    urls = ['https://osu.ppy.sh/rankings/osu/country', \
            'https://osu.ppy.sh/rankings/osu/country?page=2#scores', \
            'https://osu.ppy.sh/rankings/osu/country?page=3#scores', \
            'https://osu.ppy.sh/rankings/osu/country?page=4#scores']

    my_ranking = calc_rank(player_id)

    for url in urls:
        total_players += get_player_count(url)

    print("You are ranked " + "{:,}".format(my_ranking) + " out of " \
        + "{:,}".format(total_players) + " active players," \
        + "\nputting you in the top " + str(round(my_ranking/total_players*100, 2)) + "%.")

if __name__=="__main__":
    main()