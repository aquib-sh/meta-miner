import subprocess
import re
import sys

class MetaReader:

    """
    META READER CLASS
    
    Gets the html information from exiftool
    Processes it and returns it as dictionary
    or default html format

    Param: data-file (String)
           <path of the file which is to be processed
           for metadata>

    """
    
    def __init__(self,data_file):
        self.data_file = data_file

    # Trying to run the sub process if it fails
    # Max tries = 5 
    tries = 5

    def __read(self):
        try:
            process = subprocess.run(["exiftool","-h",self.data_file],capture_output=True)
            return process.stdout.decode()
        except:
            while(tries != 0):
                tries -= 1
                self.__read()
            # Exit if max tries has reached
            sys.exit(1)

    # Converts degree, minutes, seconds to decimal degrees
    # Decimals degrees can directly be used on map
    # Returns degree decimal in string
    def __convert_dms_to_dd(self,text):
        pattern = r"(\d+) [a-z]* (\d+)&#39; (\d+)\.?[0]*&quot"
        res = re.search(pattern,text)

        degree = float(res[1])
        minutes = float(res[2])
        seconds = float(res[3])

        half = minutes/60 + seconds/3600

        return degree + half


    # Returns the raw stdout of the subprocess, which is html
    def get_html(self):
        return self.__read()
    
    # Returns the converted stdout from html to dict
    def get_dict(self):
        raw = self.__read()

        """ 
            MEANING OF THE EXPRESSIONS IN BELOW.
            raw[:raw.find("</table>")-7] gives us the required dictonary 
        1> We find the index of </table> which is at
           the end of the output string using .find()
        2> We do -7 to remove the </tr> at the very end as well.
        3> We get the string util we reach the combination of
           above indexes (combination of </table> index and -7).
        4> .split("</td>") removes the </td> at the end of every line.
        5> Lastly, using for loop we iterate over each item and get element
           after <td>. hence, removing <td>.
    
        """
        meta_dict = {}
        li = []
        for item in raw[:raw.find("</table>")-7].split("</td>"):
            li.append(item[item.find("<td>")+len("<td>"):])
        #converting the above list to dict, with first the key then value
        latitude = None
        longitude = None
        for i in range(0,len(li)-1,2):
            val = li[i+1]

            pattern1 = r"&#39"
            pattern2 = r"&quot"

            if re.search(pattern1,val) != None:
                val = re.sub(pattern1,"'",val)
            if re.search(pattern2,val) != None:
                val = re.sub(pattern2,'"',val)
            meta_dict[li[i]]=val

            if(li[i] == "GPS Latitude"):
                latitude = self.__convert_dms_to_dd(li[i+1])
            if(li[i] == "GPS Longitude"):
                longitude = self.__convert_dms_to_dd(li[i+1])
        
        if(latitude != None and longitude != None):
            meta_dict["GPS Coordinates"] = str(latitude) +" "+str(longitude) 
        return meta_dict
    

#---------------------------------------------TESTING----------------------------------------------------------------
"""
obj = MetaReader("C:\\Users\\Aquib\\Downloads\\20200319_224342.jpg")
meta_dict=obj.get_dict()
for key, value in meta_dict.items():
   print("{} : {} ".format(key,value))
"""
