import requests
import pandas as pd
import json
# from Free_Proxy_List import * # Effectiveness
from time import sleep
from random import randint
from stem import Signal
from stem.control import Controller
from bs4 import BeautifulSoup as bs

class wall_street_crawler:
    def __init__(self):
        """
        To initialize the basic settings.
        """
        self.url_day = 'https://www.wsj.com/news/archive/{}' # URL for 1 day data
        self.url_day_above = 'https://www.wsj.com/search/term.html?min-date={}&max-date={}&isAdvanced={}&daysback={}&andor={}&sort={}&source={}' # URL for more than 1 days data
        self.links_each_news = {} # Draftly data print
        self.df = '' # Final data print

        # Fixed Setting
        self.page = '1'
        self.isAdvanced = 'true'
        self.andor = 'AND'
        self.sort = 'date-desc'
        self.source = 'wsjarticle'

        self.headers = {
            'accept-encoding' : 'gzip, deflate, br',
            'accept-language' : 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control' : 'max-age=0',
            'cookie' : "MicrosoftApplicationsTelemetryDeviceId=cd5ea44c-1b3b-0cdd-dca3-e6e26312f244; MicrosoftApplicationsTelemetryFirstLaunchTime=1588001380771; ResponsiveConditional_initialBreakpoint=lg; _fbp=fb.1.1588001385475.457600159; _parsely_session={" + "%22sid%22:1%2C%22surl%22:%22{}&page={}".format(self.url_day_above,self.page) +"%22%2C%22sref%22:%22%22%2C%22sts%22:1588001385523%2C%22slts%22:0}; _parsely_visitor={%22id%22:%22fdac8037-f48d-4d20-bb34-c240dcedf688%22%2C%22session_count%22:1%2C%22last_session_ts%22:1588001385523}; wsjregion=na%2Cus; gdprApplies=false; ccpaApplies=false; ab_uuid=dbd993a8-2b5d-4ff9-988b-22c7453b853e; usr_bkt=1p6sdUNJWD; test_key=0.8938667562079046; AMCVS_CB68E4BA55144CAA0A4C98A5%40AdobeOrg=1; kuid=u4mo1iaxv; ksg=ue57wz7wy,ue5q336cz,sgho4iyqy,ue5uid965; AMCV_CB68E4BA55144CAA0A4C98A5%40AdobeOrg=1585540135%7CMCIDTS%7C18380%7CMCMID%7C18737543708374052700206986505413105341%7CMCAAMLH-1588606188%7C11%7CMCAAMB-1588606188%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1588008588s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.4.0; s_cc=true; _ncg_g_id_=64227cdf-0f9b-4561-9a8d-7dc3b9248709; _ncg_id_=171148328e1-64971cd1-ae7a-4c0a-b913-f2413cdb9bbd; _ncg_sp_ses.5378=*; rdt_uuid=7151c733-0a93-4b3c-b3d8-dd2cc4f88c1a; _mibhv=anon-1585113403007-9784984535_4171; _micpn=esp:-1::1587989012188; _scid=85cf00f3-3f27-483a-87c2-36990120777f; OB-USER-TOKEN=0af581a4-df4d-4663-8ffa-0f37034a0203; cX_P=k86vleid5ozh3fza; cX_S=k9in0zlsijt1q8jh; __qca=P0-822237915-1588001391298; __gads=ID=3c68b0f8bf180bab:T=1588001391:S=ALNI_MYoIk1ppy5N9ClhQwedb19n9cWxnQ; _sctr=1|1587916800000; usr_prof_v2=eyJpYyI6NH0%3D; utag_main=v_id:0171bc4235300036725d0c86ff7203073009406b00bd0$_sn:1$_se:2$_ss:0$_st:1588003285776$ses_id:1588001387826%3Bexp-session$_pn:2%3Bexp-session$_prevpage:WSJ_ResearchTools_Search%20Results%20%7C%20Wall%20Street%20Journal%3Bexp-1588005085785$vapi_domain:wsj.com; _tq_id.TV-63639009-1.1fc3=39dac461496b5de7.1588001390.0.1588001488..; _ncg_sp_id.5378=30a2b02b-33c9-42a4-92b4-d9f5153b9295.1585113403.1.1588001491.1585113403.fb3298b0-fc60-46c2-9dbc-1f0758cf8e52; hok_seg=none; s_tp=5168; s_ppv=WSJ_ResearchTools_Search%2520Results%2520%257C%2520Wall%2520Street%2520Journal%2C18%2C18%2C93",
            'referer' : self.url_day_above,
            'sec-fetch-dest' : 'document',
            'sec-fetch-mode' : 'navigate',
            'sec-fetch-site' : 'same-origin',
            'upgrade-insecure-requests' : '1',
            'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }
        self.proxies = { 'http' : '' } # Avoid IP blocking

    def request(self,day,date_start,date_end='',label_block=[]):
        """
        To request data from Wall Street Journal.
        
        ############ FORMAT VARIABLE ###############
        # day -> 1d / 2d / 7d / 30d / 90d / 1y / 4y
        # date_start -> YYYY/MM/DD
        # date_end -> YYYY/MM/DD
        # label_block -> ['Opinion']
        #############################################
        """
        self.date_start = date_start
        self.date_end = date_end
        self.day = day

        # Start to request
        if self.day == '1d':
            self.date_start = date_start.replace('/','')
            res = requests.get(self.url_day.format(self.date_start),headers = self.headers)
        else:
            res = requests.get(self.url_day_above.format(
                self.date_start,self.date_end,self.isAdvanced,   # Dynamic input variable
                self.day,self.andor,self.sort,self.source        # Dynamic input variable
            ) + '&page={}'.format(self.page),headers = self.headers)
        self.get_each_news_data(res,label_block)

    def get_each_news_data(self,res,label_block):
        """
        To get link from the main website for collecting data.
        """
        if self.day == '1d':
            raw_data = bs(res.content.decode(),'html.parser') # Initialize bs4 to clear data
            for no,ele in enumerate(raw_data.ol.find_all('article')): # Get the link from every news
                self.links_each_news[str(no)] = {'type' : ele.span.string,'link' : ele.a['href']}
                print('Getting links from each page! Link : {}'.format(no + 1))
        else:
            raw_data = bs(res.content.decode(),'lxml')
            total_page = int(raw_data.find_all('li',class_ = 'results-count')[1].string.split(' ')[1])
            total_download = raw_data.find('li',class_ = 'results-count').string.split(' ')[2]
            count = 0
            for page_num in range(total_page):     
                res = requests.get(self.url_day_above.format(
                    self.date_start,self.date_end,self.isAdvanced,   # Dynamic input variable
                    self.day,self.andor,self.sort,self.source        # Dynamic input variable
                ) + '&page={}'.format(page_num+1),headers = self.headers)
                raw_data = bs(res.content.decode(),'lxml')
                raw_data = raw_data.find('ul',class_ = 'items hedSumm').find_all('div',class_ = 'item-container headline-item')
                for ele in raw_data:
                    count+=1
                    self.links_each_news[str(count)] = {
                        'type' : ele.a.string,
                        'link' : 'https://www.wsj.com' + ele.h3.a['href']
                    }
                print('Getting links from each page! Page : {} / {}'.format(page_num + 1,total_page))
                # print('Type: {} ,\n Link: {}'.format(self.links_each_news[str(count)]['type'],self.links_each_news[str(count)]['link']))
            self.to_JSON('Links_Each_News',self.links_each_news,total_download)
        print('Get links complete !')
        self.process_data(label_block,total_download)

    def process_data(self,label_block:list,total_download):
        """
        To process the raw data.
        """
        data_to_df = [] # Save clean data in the regular format
        count = 0 # Count download data

        for each_no in self.links_each_news:
            try:
                if self.links_each_news[each_no]['type'] not in label_block: # Classify data by label condition 
                    res_each = requests.get(self.links_each_news[each_no]['link'],headers = self.headers,proxies = self.proxies)
                    raw_data_each = bs(res_each.content.decode(),'html.parser')
                    title = self.is_empty(raw_data_each.find('h1',class_ = 'wsj-article-headline')) # Get title
                    sub_title = self.is_empty(raw_data_each.find('h2',class_ = 'sub-head')) # Get sub-title
                    content = ''
                    # Get article content with different way
                    try:
                        for each_para in raw_data_each.find('div',class_ = 'wsj-snippet-body').find_all('p'):
                            content = content + format(each_para.string) # Get content(might be partial content)
                    except:
                        for each_para in raw_data_each.find('div',class_ = 'article-content').find_all('p'):
                            content = content + format(each_para.string) # Get content(might be partial content)
                    # Get article date with different way
                    try:
                        d_date = raw_data_each.time.string.split('Updated')[1].split('ET')[0].split(' ')
                        date =  d_date[2].split(',')[0] + '-' + self.convert_month(d_date[1]) + '-' + d_date[3]
                    except:
                        d_date = [d for d in raw_data_each.time.string.split(' ') if d != '']
                        date = d_date[2].split(',')[0] + '-' + self.convert_month(d_date[1]) + '-' + d_date[3]
                    # Push scrapped data to list
                    data_to_df.append([date,title,sub_title,content])
                    # sleep(randint(1,3)) # Pause 1 sec to avoid IP block
                    count+=1 # Counting number of downloaded article
                    print('Downloading.... {} / {}'.format(count,total_download))
                    # Renew IP if get 10 data
                    if count % 5 == 0:
                        self.renew_connection()
                        session = self.get_tor_session()
                        temp_IP = session.get("http://httpbin.org/ip").json()['origin']
                        self.proxies['http'] = temp_IP
                        print('Switch IP to: {}'.format(temp_IP))

            except Exception as e: # Print out error news
                    self.print_err(self.links_each_news[each_no]['type'],self.links_each_news[each_no]['link'],each_no,e)
        print('Number of download data: {}'.format(len(data_to_df)))
        self.to_dataframe(data_to_df)
    
    def to_dataframe(self,data_to_df):
        """
        To change clean data to dataframe.
        """
        columns = ['date','title','sub_title','content'] # Columns' name
        self.df = pd.DataFrame(data_to_df,columns = columns)

        # Clean "ENTER" symbol
        self.df['title'] = self.df['title'].apply(self.replace_sym)
        self.df['sub_title'] = self.df['sub_title'].apply(self.replace_sym)
        self.df['content'] = self.df['content'].apply(self.replace_sym)

    def to_csv(self):
        """
        To save as csv file.
        """
        self.df.to_csv('WSJ_{}_data.csv'.format(self.day),index = False,header = True,encoding='utf-8')
    
    def to_JSON(self,file_name,dict_file,indent):
        """
        To save as JSON file.
        """
        out_file = open("{}.json".format(file_name), "w")  
        json.dump(dict_file, out_file, indent = indent)  
        out_file.close()  

############################## OPTIONAL FUNCTION ##############################
    def is_empty(self,content):
        """
        To check content is empty or is existing.
        """
        if content == None:
            return ''
        else:
            return content.string

    def replace_sym(self,content):
        """
        To replace "ENTER" symbol.
        """
        return content.replace('\n','')

    def convert_month(self,month):
        """
        To convert month in number format or word format.
        """
        month_dict = {
            'January' : 1,
            'February' : 2,
            'March' : 3,
            'April' : 4,
            'May' : 5,
            'June' : 6,
            'July' : 7,
            'August' : 8,
            'September' : 9,
            'October' : 10,
            'November' : 11,
            'December' : 12
        }
        
        try:
            if isinstance(month,str):
                return str(month_dict[month])
            elif isinstance(month,int):
                if month in month_dict.values():
                    key_list = list(month_dict.keys())
                    val_list = list(month_dict.values())
                    return key_list[val_list.index(month)]
                else:
                    print("Error: {}, Month input doesn't match the format!".format(month))
        except:
            print("Error: {}, Month input doesn't match the format!".format(month))

    def print_err(self,type_,link,num,err):
        """
        To print out exception error.
        """
        print('Error: Failed to download! \n' ,
        'Failed Detail: \n' ,
        '-> type: {} \n '.format(type_) ,
        '-> link: {} \n '.format(link) ,
        '-> number: {} \n '.format(num) ,
        '-> error: {} \n '.format(err)
        )

    def get_tor_session(self):
        """
        To get a current session's IP address.
        """
        session = requests.session()
        # Tor uses the 9050 port as the default socks port
        session.proxies = {'http':  'socks5://127.0.0.1:9050',
                        'https': 'socks5://127.0.0.1:9050'}
        return session

    def renew_connection(self):
        """
        To renew IP for avoiding band IP address.
        """
        with Controller.from_port(port = 9051) as controller:
            controller.authenticate(password="weijie12")
            controller.signal(Signal.NEWNYM)
############################## OPTIONAL FUNCTION ##############################

####### 1d FORMAT #######
# DAY = '1d'
# START_DATE = '2020/04/22' 
# END_DATE = ''
# LABEL_BLOCK = ['Opinion']

# wsj_crawler = wall_street_crawler()
# wsj_crawler.request(DAY,START_DATE,END_DATE,LABEL_BLOCK)
# wsj_crawler.to_csv()
# print(wsj_crawler.df)

####### 1d ABOVE FORMAT #######
if __name__ == "__main__":
    DAY = '90d'
    START_DATE = '2020/01/01' 
    END_DATE = '2020/04/01'
    LABEL_BLOCK = ['Opinion']

    wsj_crawler = wall_street_crawler()
    wsj_crawler.request(DAY,START_DATE,END_DATE,LABEL_BLOCK)
    wsj_crawler.to_csv()
    print(wsj_crawler.df)