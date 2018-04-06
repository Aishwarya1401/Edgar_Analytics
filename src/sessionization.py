from collections import OrderedDict
import csv
from datetime import datetime
import sys

class Edgar:
    def __init__(self,inputfile,outputfile,inactivityfile):
        self.inputfile = inputfile
        self.outputfile = outputfile
        self.inactivityfile = inactivityfile
        self.inactivityperiod = 0
        self.dict_records = OrderedDict()
        self.time_format = '%Y-%m-%d %H:%M:%S'
        
    def get_inactivity_period(self):
        with open(self.inactivityfile) as f:
            line = f.read()
            self.inactivityperiod = int(line)
        
        
    def process_logs(self):
        
        with open(self.outputfile,'w') as fw:
            with open(self.inputfile) as csvfile:
                reader = csv.DictReader(csvfile)
                current_time =" "
                current_date =" "
                for row in reader:
                    if row['ip'] not in self.dict_records:
                        self.dict_records[row['ip']] = {}
                        self.dict_records[row['ip']]['session_start_time'] =  row['time']
                        self.dict_records[row['ip']]['start_date'] = row['date']
                        self.dict_records[row['ip']]['end_date'] = row['date']
                        self.dict_records[row['ip']]['docs'] = 1
                        self.dict_records[row['ip']]['session_end_time'] = row['time']
                    else:
                        self.dict_records[row['ip']]['session_end_time'] = row['time']
                        self.dict_records[row['ip']]['end_date'] = row['date']
                        self.dict_records[row['ip']]['docs'] = self.dict_records[row['ip']]['docs'] +1

                    current_time = self.dict_records[row['ip']]['session_end_time']
                    current_date = self.dict_records[row['ip']]['end_date']

                    for key in self.dict_records:
                        current_date_time = current_date +" "+ current_time
                        key_date_time = self.dict_records[key]['end_date'] + " " + self.dict_records[key]['session_end_time']

                        time_elapsed =  datetime.strptime(current_date_time, self.time_format) - datetime.strptime(key_date_time, self.time_format)

                        if(time_elapsed.total_seconds() > self.inactivityperiod ):
                                key_end_date_time = self.dict_records[key]['end_date']+ " "+ self.dict_records[key]['session_end_time']
                                key_start_date_time = self.dict_records[key]['start_date']+ " "+ self.dict_records[key]['session_start_time']
                                duration = datetime.strptime(key_end_date_time, self.time_format) - datetime.strptime(key_start_date_time, self.time_format) 
                                total_duration = int(duration.total_seconds() +1)
                                
                                fw.write(key+","+key_start_date_time+","+key_end_date_time +","+str(total_duration) +","+str(self.dict_records[key]['docs']))
                                fw.write("\n")
                                self.dict_records.pop(key,None)


            for key in self.dict_records:
                key_end_date_time = self.dict_records[key]['end_date']+ " "+ self.dict_records[key]['session_end_time']
                key_start_date_time = self.dict_records[key]['start_date']+ " "+ self.dict_records[key]['session_start_time']
                duration = datetime.strptime(key_end_date_time, self.time_format) - datetime.strptime(key_start_date_time, self.time_format) 
                total_duration = int(duration.total_seconds() +1)

                fw.write(key+","+key_start_date_time+","+key_end_date_time +","+str(total_duration) +","+str(self.dict_records[key]['docs']))
                fw.write("\n")
                




if __name__ == "__main__":
    
    inputfile = sys.argv[1]
    inactivityfile = sys.argv[2]
    outputfile =  sys.argv[3]
    
    o = Edgar(inputfile,outputfile,inactivityfile)
    o.get_inactivity_period()
    o.process_logs()
    

