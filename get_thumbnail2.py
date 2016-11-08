thumbalizr_config={
	'api_key':"", #put your api key here
	'service_url':"http://api.thumbalizr.com/", #  # don't change, if you didn't have a special service contract
	'use_local_cache':True, # TRUE or FALSE for local image cache
	'local_cache_dir':"cache", #relative cache directory must exists in install directory and rwx permissions to all (777)
	'local_cache_expire':12 # local chache expiration time in hours
  }
thumbalizr_defaults={
	'width':"250", # image width
	'delay':"8", # caputre delay useful for flash content 5 - 10 is a good value
	'encoding':"png", # jpg or png
	'quality':"90", #image quality 10-90
	'bwidth':"1280", # browser width
	'mode':"screen", # screen or page
	'bheight':"1024" # browser height only for mode=screen
}

class thumbalizrRequest():
	
  def __init__(self):
    global thumbalizr_config,thumbalizr_defaults
    self.api_key=thumbalizr_config['api_key']
    self.service_url=thumbalizr_config['service_url']
    self.use_local_cache=thumbalizr_config['use_local_cache']
    self.local_cache_dir=thumbalizr_config['local_cache_dir']
    self.local_cache_expire=thumbalizr_config['local_cache_expire']
    self.encoding=thumbalizr_defaults['encoding']
    self.quality=thumbalizr_defaults['quality']
    self.delay=thumbalizr_defaults['delay']
    self.bwidth=thumbalizr_defaults['bwidth']
    self.mode=thumbalizr_defaults['mode']
    self.bheight=thumbalizr_defaults['bheight']
    self.width=thumbalizr_defaults['width']


  def build_request(self,url) :
    self.request_url= 
    (self.service_url+"?"+
    "api_key="+self.api_key+"&"+
    "quality="+self.quality+"&"+
    "width="+self.width+"&"+
    "encoding="+self.encoding+"&"+
    "delay="+self.delay+"&"+
    "mode="+self.mode+"&"+
    "bwidth="+self.bwidth+"&"+
    "bheight="+self.bheight+"&"+
    "url="+url)
   #################ここまで書き換えた################
  self.local_cache_file=md5(url)."_".self.bwidth."_".self.bheight."_".self.delay."_".self.quality."_".self.width.".".self.encoding;
		self.local_cache_subdir=self.local_cache_dir."/".substr(md5(url),0,2);		
	}
	
	
	function request(url) { 
		self.build_request(url);
		if (file_exists(self.local_cache_subdir."/".self.local_cache_file)) { 
			filetime=filemtime(self.local_cache_subdir."/".self.local_cache_file);
			cachetime=time()-filetime-(self.local_cache_expire*60*60);
		} else {
			cachetime=-1;
		}
		if (!file_exists(self.local_cache_subdir."/".self.local_cache_file) || cachetime>=0) {
			self.img= file_get_contents(self.request_url);
			headers="";
			foreach(http_response_header as tmp) {
		 		if (strpos(tmp,'X-Thumbalizr-')!==false) { 
		 			tmp1=explode('X-Thumbalizr-',tmp); tmp2=explode(': ',tmp1[1]); headers[tmp2[0]]=tmp2[1]; 
		 		}
			}	
			self.headers= headers;		
			self.save();
		} else {
			self.img= file_get_contents(self.local_cache_subdir."/".self.local_cache_file);
			self.headers['URL']= url;
			self.headers['Status']= 'LOCAL';		
		}
	}
	
	private function save() { 
		if (self.img && self.use_local_cache===TRUE && self.headers['Status']=="OK") {
			if (!file_exists(self.local_cache_subdir)) { mkdir(self.local_cache_subdir); }
	 		fp=fopen(self.local_cache_subdir."/".self.local_cache_file,'w');
	 		fwrite(fp,self.img);
	 		fclose(fp);
		}
	}
	
	function output(sendHeader = true,destroy = true) {  
		if (self.img) {
			if (sendHeader) {
				if (self.encoding=="jpg") {
					header("Content-type: image/jpeg");
				} else {
					header("Content-type: image/png");
				}
				foreach(self.headers as k=>v) {
					header("X-Thumbalizr-".k.": ".v);
				}
			}
			echo self.img;				
			if (destroy) {
				self.img= false;
			}
		} else {
			return false;
		}
	}

}
