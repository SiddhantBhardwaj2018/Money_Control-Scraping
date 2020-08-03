from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

html = urlopen("https://www.moneycontrol.com/stocksmarketsindia/")
bsObj = BeautifulSoup(html, 'lxml')


def scrape_easy(id):
    '''
    Scraping from MoneyControl.com to get data of top buyer,seller, top gainer,loser,52 week high ,low etc.
    '''
    arr = bsObj.find('div', {'id': id}).find(
        'table').find('tbody').findAll('tr')
    d = dict()
    for item in arr:
        for i, text1 in enumerate(item.findAll('td')):
            if i == 0:
                d[text1.text] = []
            else:
                d[item.findAll('td')[0].text].append(text1.text)
    return d

def scrape_indices():
    '''
    Scraping from MoneyControl.com to get info about domestic indices,global indices and most active stocks
    '''
    arr = bsObj.findAll('div',{'class':'marketatc_actcont'})
    active_arr = bsObj.find('div',{'id':'manse'}).find('table').find('tbody').findAll('tr')
    national,international,active_stocks = dict(),dict(),dict()
    for i,value in enumerate(arr):
        if(i == 0):
            for new in value.find('table').find('tbody').findAll('tr'):
                for k,td in enumerate(new.findAll('td')):
                    if k == 0:
                        national[td.text] = []
                    else:
                        national[new.findAll('td')[0].text].append(td.text)
        elif i == 1:
            for new in value.find('table').find('tbody').findAll('tr'):
                for k,td in enumerate(new.findAll('td')):
                    if k == 0:
                        international[td.text] = []
                    else:
                        international[new.findAll('td')[0].text].append(td.text)
    
    for item in active_arr:
        for i,text1 in enumerate(item.findAll('td')):
            if i == 0:
                active_stocks[text1.text] = []
            else:
                active_stocks[item.findAll('td')[0].text].append(text1.text)     

    return national,international,active_stocks

def main():
    '''
    This is the main function where I am scraping from unique ids at the relevant url, creating dataframes and outputting them to an html file. This code requires an internet connection to work.
    '''
    gainers,losers,buyers,sellers,week_high,week_low,price_shockers,volume_shockers = scrape_easy('msa_tgnse'), scrape_easy("msa_tlnse"), scrape_easy('msa_obnse'),scrape_easy("msa_osnse"),scrape_easy('msa_52hnse'),scrape_easy("msa_52lnse"),scrape_easy('msa_psnse'),scrape_easy("msa_vsnse")
    domestic_indices,international_indices,active_stocks = scrape_indices()
    gains_df = pd.DataFrame.from_dict(gainers,columns = ['Current_Price','Gain%'],orient = 'index')
    loss_df = pd.DataFrame.from_dict(losers,columns = ['Current_Price','Loss%'],orient = 'index')
    buy_df = pd.DataFrame.from_dict(buyers,columns = ['Current_Price','Change%'],orient='index')
    sell_df = pd.DataFrame.from_dict(sellers,columns = ['Current_Price','Change%'],orient='index')
    week52_high = pd.DataFrame.from_dict(week_high,columns = ['Days-High-Price','Current_Price'],orient = 'index')
    week52_low = pd.DataFrame.from_dict(week_low,columns = ['Days-High-Price','Current_Price'],orient = 'index')
    price_shock = pd.DataFrame.from_dict(price_shockers,columns = ['Current_Price','Change%'],orient = 'index')
    volume_shock = pd.DataFrame.from_dict(volume_shockers,columns = ['Current_Price','Change%'],orient = 'index')
    dome_indices = pd.DataFrame.from_dict(domestic_indices,columns = ['Price','Change','Change%'],orient = 'index')
    globe_indices = pd.DataFrame.from_dict(international_indices,columns = ['Price','Change','Change%'],orient = 'index')
    active_stocks_df = pd.DataFrame.from_dict(active_stocks,columns = ['Price','Change','Valuation'],orient = 'index') 

    output_string =  '<h1> Top Gainers </h1>' + '<br>' + gains_df.head().to_html() + '<br>'+ '<h1> Top Losers </h1>' + '<br>' + loss_df.head().to_html() + '<br>'  + '<h1> Top Buyers </h1>' + '<br>' + buy_df.head().to_html() + '<br>' + '<h1> Top Sellers </h1>' + '<br>' + sell_df.head().to_html() + '<br>' + '<h1> 52 Week High </h1>' + '<br>' + week52_high.head().to_html() + '<br>' + '<h1> 52 Week Low </h1>' + '<br>' + week52_low.head().to_html() + '<br>' + '<h1> Price Shockers </h1>' + '<br>' + price_shock.head().to_html() + '<br>' + '<h1> Volume Shockers </h1>' + '<br>' + volume_shock.head().to_html() + '<br>' + '<h1> National Indices </h1>' + '<br>' + dome_indices.head().to_html() + '<br>' + '<h1> International Indices </h1>' + '<br>' + globe_indices.head().to_html() + '<br>' + '<h1> Active Stocks </h1>' + '<br>' + active_stocks_df.head().to_html() + '<br>' 

    with open('output.html','w') as file:
      file.write(output_string)  
      file.close()

if __name__ == '__main__':
    main()
