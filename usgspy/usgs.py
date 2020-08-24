import requests
import datetime
import time     
import pandas as pd 
from io import StringIO
from .mapping import has_gpd,pd_to_gpd
    
class earthquakes(object):
    
    def __init__(self,debug_level = 0, apptype = 'json', init_calls = True , use_gpd = True):
        
        self.base = 'https://earthquake.usgs.gov/fdsnws/event/1/'
        self.sleep_time_s = 1. # throttle calls    
        self.last_call_time = None 
        self.last_request = {
            'payload':{},
            'url':None,
            'endpoint':None,
        }
    
        if has_gpd:
            self.use_gpd = use_gpd
        else:
            self.use_gpd = False 
            
        self.debug_level = debug_level 
        
        apptypes = ['json','wadl']
        if apptype not in apptypes:
            raise ValueError(f"apptype must be {' '.join(apptype)}")
        self.apptype = apptype
        
        if init_calls:
            self.version = self.get_version()
            self.parameters = self.get_application() 
        else:
            self.version=''
            self.parameters={}
        
    def fetch(self,endpoint,payload={}):
        # https://earthquake.usgs.gov/fdsnws/event/1/[METHOD[?PARAMETERS]] 
        url = self.base + endpoint
        
        if self.debug_level > 0:
            print(f"calling api at {url}")
            if payload:
                print("with parameters:")
                print(payload)            
        
        if self.last_call_time is None:
            wait_time = 0 
        else:
            now_time = datetime.datetime.now() 
            dt = now_time - self.last_call_time
            if dt.seconds < self.sleep_time_s:
                wait_time = self.sleep_time_s
            else:
                wait_time = 0.
                
        time.sleep(wait_time)
                        
        if payload:
            r = requests.get(url, params=payload)
        else:
            r = requests.get(url)
            
        self.last_call_time = datetime.datetime.now()   
        
        self.last_request = {
            'url' : url,
            'endpoint': endpoint,
            'payload': payload,
        }
        
        return r 
    
    def _sanitize_startend(self,setime,strformat='%Y-%m-%d'):
        
        if isintance(setime,str):
            date_t = datetime.datetime.strptime(settime,strformat)
        
        date_str = date_t.strftime('%Y-%m-%d')        
        
    def get_application(self):                       
        r = self.fetch('application.'+self.apptype)
        return r.json()
                
    def catalogs(self):
        raise NotImplementedError("catalogs not implemented, use fetch() to reach a generic endpoint")
        return 
    
    def contributors(self):
        raise NotImplementedError("contributors not implemented, use fetch() to reach a generic endpoint")
        return 
    
    def _count_query(self,count_or_query,startime=None,endtime=None,**kwargs):
        
        payload = {'format':'geojson'}
        
        if startime is not None:
            payload['starttime'] = self._sanitize_startend(starttime)
        
        if endtime is not None:
            payload['endtime'] = self._sanitize_startend(endtime)
            
        for key,val in kwargs.items():
            payload[key] = val
                        
        if count_or_query in ['count','query']:            
            return self.fetch(count_or_query,payload)
        else:
            raise ValueError("_count_query requires 'count' or 'query'")
                
    def count(self,startime=None,endtime=None,**kwargs):        
        r = self._count_query('count',startime,endtime,**kwargs)         
        try: 
            c = r.json()
        except:
            c = r.text
        return c
        
    def query(self,startime=None,endtime=None,**kwargs):
        r = self._count_query('query',startime,endtime,**kwargs)
        
        fmt = self.last_request['payload']['format']
        if fmt == 'csv' :
            df = pd.read_csv(StringIO(r.text),sep=",")
            if self.use_gpd:
                df = pd_to_gpd(df,'latitude','longitude')
            return df 
            
        elif fmt == 'geojson':
            return r.json() 
        else:
            return r.text
    
    def get_version(self):
        r = self.fetch('version')
        return r.text
