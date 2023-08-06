from utils import *
from evaluate_category import *
from evaluate_output import *
import matplotlib.pyplot as plt
import collections
import json


class zanon(object):

    def __init__(self, deltat, pk, k): 
        super(zanon, self).__init__()
        self.deltat = deltat
        self.rate = 1800
        self.z = 10
        self.H = {}
        self.c = {}
        self.pk = pk
        self.k = k
        self.t_start = 0
        self.t_stop = 0
        self.last_update = 0
        self.test = []
        self.time = []
        self.kanon = []
        self.queue = collections.deque()
        self.all_tuple = collections.deque()
        self.f_out = open('output.txt', 'w+')
        self.f_count = open('counters.txt', 'w+')
        self.tot_data = []
        self.details = [0]*20
        self.all_details = [[] for i in range(20)]
        self.anonymized  = collections.deque()
        self.tot_anon = []
        self.from_ll_to_mt = Transformer.from_crs('epsg:4326', 'epsg:3857')
        self.stepsize = np.array([3000, 5000, 10000, 30000, 500000])
        self.numeric_category = False

	
    def anonymize(self, tupla):
        
        t = float(tupla[0])
        u = tupla[1]  
       
        if(len(tupla) == 4):
            lat = tupla[2]
            lon = tupla[3]
            a = "*".join(str(x) for x in reversed(get_cell(self,lat,lon)))
            self.numeric_category = True
        elif(len(tupla)==3):
            a = tupla[2].strip() 
        else: raise ValueError("Arguments can be either 3 or 4, not " + str(len(tupla)))
            
              
        if self.t_start == 0:
            self.t_start = t
            output = {}
            output['all_details']=[[] for i in range(20)]
            output['tot_anon']=[]
            output['time'] = []
            output['z']=[]
            output['kanon']=[]
            with open("output.json","w+") as f:
                json.dump(output,f)
             
        sep = '*'
        cat = a.split(sep)
        for level in range(len(cat)):    
            att = '*'.join(cat[:level + 1])
            if att in self.H:
                evict(self, t, att)
                  
        clean_queue(self,t)        
        z_change(self, t)          
        self.t_stop = t                
        manage_data_structure(self, t, u, a)       
        check_and_output(self, t, u, a)
               
    def duration(self):
        print('End of simulation (simulated time: {})'.format(str(timedelta(seconds = int(self.t_stop - self.t_start)))))

    def evaluate_output(self):
        evaluate_output()
        
    def evaluate_category(self,z):
        evaluate_cat(z)
        
    def final_kanon(self):
        final_kanon()

    def plot_z(self):
        plot_z(self)
        
    def endFiles(self):
        self.f_out.close()
        self.f_count.close()
		