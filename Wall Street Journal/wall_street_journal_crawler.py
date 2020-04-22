import requests
import pandas as pd
# import datetime as dt
from time import sleep
from bs4 import BeautifulSoup as bs

class wall_street_crawler:
    def __init__(self):
        """
        To initialize the basic settings.
        """
        self.headers = {
            'accept-encoding' : 'gzip, deflate, br',
            'accept-language' : 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control' : 'max-age=0',
            'cookie' : 'MicrosoftApplicationsTelemetryDeviceId=2e60f7c3-7fde-c5f7-259f-fcfde1e2d33c; MicrosoftApplicationsTelemetryFirstLaunchTime=1587214359886; DJSESSION=country%3Dtw%7C%7Ccontinent%3Das%7C%7Cregion%3D%7C%7Ccity%3Dtaipei%7C%7Clatitude%3D25.02%7C%7Clongitude%3D121.45%7C%7Ctimezone%3Dgmt%2B8; gdprApplies=false; ccpaApplies=false; ab_uuid=6594e524-20fd-4293-ab22-284c99a52be4; usr_bkt=63L1D4y2F9; __gads=ID=68c1d53f31c0b600:T=1587214329:S=ALNI_MbzPovsiqCCINO9cmaiYJjI7Rm0iA; AMCVS_CB68E4BA55144CAA0A4C98A5%40AdobeOrg=1; s_cc=true; _mibhv=anon-1585113403007-9784984535_4171; _micpn=esp:-1::1587214334860; _scid=30146b1f-a532-40d7-a98a-ae0d3f4b4bc3; cX_P=k86vleid5ozh3fza; cX_S=k95mfnb6lozeywsx; _fbp=fb.1.1587214335751.1743228894; OB-USER-TOKEN=0af581a4-df4d-4663-8ffa-0f37034a0203; bkuuid=XA0QnxR999OJpooK; _ncg_g_id_=64227cdf-0f9b-4561-9a8d-7dc3b9248709; cX_G=cx%3A178ygmx2pqwx9n46tvapcofhv%3A2cw8rxy6pqz01; __qca=P0-389897079-1587214336959; _sctr=1|1587139200000; __adroll_fpc=abed96594d298a87326c355f85fe083e-1587214366004; _ntv_uid=0cf20779-fd58-4970-b553-12feff3bb3a0; kuid=u3l8xn21p; ksg=sgho4iyqy; usr_prof_v2=eyJpYyI6NX0%3D; hok_seg=none; djvideovol=1; MicrosoftApplicationsTelemetryFirstLaunchTime=1587493052071; MicrosoftApplicationsTelemetryDeviceId=c09bd020-b0eb-ce58-98ce-c1a29fdba114; test_key=0.02129019173271307; vidoraUserId=gb78j5m2tc95ulrb8lhq1tpobe6l37; _ncg_id_=171148328e1-64971cd1-ae7a-4c0a-b913-f2413cdb9bbd; __ar_v4=BLKVHZP6SRDZ3E5KVJS2CU%3A20200418%3A18%7CVVQU6E37EJBTDLQXFNU22G%3A20200418%3A18%7CUBK2BTYVYBEGTHKRZO6NVW%3A20200418%3A18; wsjregion=na%2Cus; AMCV_CB68E4BA55144CAA0A4C98A5%40AdobeOrg=1585540135%7CMCIDTS%7C18375%7CMCMID%7C18737543708374052700206986505413105341%7CMCAAMLH-1588146456%7C11%7CMCAAMB-1588146456%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1587548856s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.4.0; _ncg_sp_ses.5378=*; _parsely_session={%22sid%22:9%2C%22surl%22:%22https://www.wsj.com/news/economy%22%2C%22sref%22:%22https://www.wsj.com/%22%2C%22sts%22:1587541750687%2C%22slts%22:1587498083394}; _parsely_visitor={%22id%22:%22fdac8037-f48d-4d20-bb34-c240dcedf688%22%2C%22session_count%22:9%2C%22last_session_ts%22:1587541750687}; GED_PLAYLIST_ACTIVITY=W3sidSI6IlVlV28iLCJ0c2wiOjE1ODc1NDYxNTAsIm52IjowLCJ1cHQiOjE1ODc0OTI5NTQsImx0IjoxNTg3NDkzMTExfV0.; ResponsiveConditional_initialBreakpoint=lg; s_sq=%5B%5BB%5D%5D; utag_main=v_id:01718d58b5870096b6fded4e4d0003073001a06b00bd0$_sn:8$_se:20$_ss:0$_st:1587548578260$vapi_domain:wsj.com$ses_id:1587541656618%3Bexp-session$_pn:20%3Bexp-session$_prevpage:WSJ_Summaries_Archive_NewsArchive%3Bexp-1587550378276; s_tp=4077; s_ppv=WSJ_Summaries_Archive_NewsArchive%2C23%2C23%2C937; _ncg_sp_id.5378=30a2b02b-33c9-42a4-92b4-d9f5153b9295.1585113403.1.1587546779.1585113403.fb3298b0-fc60-46c2-9dbc-1f0758cf8e52; _tq_id.TV-63639009-1.1fc3=74200c6d03e7a60b.1587214364.0.1587546779..',
            'sec-fetch-dest' : 'document',
            'sec-fetch-mode' : 'navigate',
            'sec-fetch-site' : 'none',
            'upgrade-insecure-requests' : '1',
            'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }
        self.url_day = 'https://www.wsj.com/news/archive/{}' # URL for 1 day data
        self.url_day_above = '' # URL for more than 1 days data
        self.links_each_news = {} # Draftly data print
        self.df = '' # Final data print

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
        self.day = day

        # Start to request
        if day == '1d':
            date_start = date_start.replace('/','')
            res = requests.get(self.url_day.format(date_start),headers = self.headers)
        else:
            res = requests.get(self.url_day_above,headers = self.headers)
        self.get_each_news_data(res,label_block)

    def get_each_news_data(self,res,label_block):
        """
        To get link from the main website for collecting data.
        """
        raw_data = bs(res.content.decode(),'html.parser') # Initialize bs4 to clear data
        for no,ele in enumerate(raw_data.ol.find_all('article')): # Get the link from every news
            self.links_each_news[str(no)] = {'type' : ele.span.string,'link' : ele.a['href']}
        self.process_data(label_block)

    def process_data(self,label_block:list):
        """
        To process the raw data.
        """
        data_to_df = [] # Save clean data in the regular format
        count = 0 # Count download data

        try:
            for each_no in self.links_each_news:
                if self.links_each_news[each_no]['type'] not in label_block: # Classify data by label condition 
                    res_each = requests.get(self.links_each_news[each_no]['link'],headers = self.headers)
                    raw_data_each = bs(res_each.content.decode(),'html.parser')
                    title = self.is_empty(raw_data_each.find('h1',class_ = 'wsj-article-headline')) # Get title
                    sub_title = self.is_empty(raw_data_each.find('h2',class_ = 'sub-head')) # Get sub-title
                    content = ''
                    try:
                        for each_para in raw_data_each.find('div',class_ = 'wsj-snippet-body').find_all('p'):
                            content = content + format(each_para.string) # Get content(might be partial content)
                    except:
                        for each_para in raw_data_each.find('div',class_ = 'article-content').find_all('p'):
                            content = content + format(each_para.string) # Get content(might be partial content)
                    data_to_df.append([title,sub_title,content])
                    sleep(1) # Pause 1 sec for avoiding IP block
                    count+=1
                    print('Downloading.... {}'.format(count))
            print('Number of download data: {}'.format(len(data_to_df)))
        except Exception as e: # Print out error news
            print('Error: Failed to download! \n' ,
                'Failed Detail: \n' ,
                '-> type: {} \n '.format(self.links_each_news[each_no]['type']) ,
                '-> link: {} \n '.format(self.links_each_news[each_no]['link']) ,
                '-> number: {} \n '.format(each_no) ,
                '-> error: {} \n '.format(e))
        self.to_dataframe(data_to_df)
    
    def to_dataframe(self,data_to_df):
        """
        To change clean data to dataframe.
        """
        columns = ['title','sub_title','content'] # Columns' name
        self.df = pd.DataFrame(data_to_df,columns = columns)

        # Clean "ENTER" symbol
        self.df['title'] = self.df['title'].apply(self.replace_sym)
        self.df['sub_title'] = self.df['sub_title'].apply(self.replace_sym)
        self.df['content'] = self.df['content'].apply(self.replace_sym)

    def to_csv(self):
        """
        To save as csv file.
        """
        self.df.to_csv('WSJ_{}_{}_data.csv'.format(self.date_start,self.day),encoding='utf8')

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


DAY = '1d'
START_DATE = '2020/04/22' 
END_DATE = ''
LABEL_BLOCK = ['Opinion']

wsj_crawler = wall_street_crawler()
wsj_crawler.request(DAY,START_DATE,END_DATE,LABEL_BLOCK)
print(wsj_crawler.df)