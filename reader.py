"""
MetaReader
Author: Shaikh Aquib

Gets the html information from exiftool, processes it and returns it as dictionary or default html format.

Param: data_file (String) 
       (path of the file which is to be processed for metadata)

Functions: __read              - Reads the data from exif tool using subprocess.
           __convert_dms_to_dd - Converts the degree, minutes and second format to
                                 degree decimals format for GPS Co-ordinates.
           get_html            - Simply returns the output from __read().
           get_dict            - Returns a dictionary by refining the html data.
                                 Adds GPS Co-ordinates to dictionary by passing the latitude and longitude
                                 in dms format through __convert_dms_to_dd.
                    

"""

import subprocess
import re
import sys
import os


class MetaReader:

    # Constructor
    def __init__(self, data_file):
        self.data_file = data_file
        self.__core_path = "res\\exiftool"
        self.tries = 5

    # Trying to run the sub process if it fails
    # Max tries = 5
    def __read(self):
        try:
            tool_path = os.path.join(os.getcwd(), self.__core_path)
            process = subprocess.run(
                [tool_path, "-h", self.data_file], capture_output=True
            )
            return process.stdout.decode()
        except:
            while self.tries > 0:
                self.tries -= 1
                self.__read()
            # Exit if max tries has reached
            sys.exit(1)

    # Converts degree, minutes, seconds to decimal degrees
    # Decimals degrees can directly be used on map
    def __convert_dms_to_dd(self, text):
        pattern = r"(\d+) [a-z]* (\d+)&#39; (\d+)\.?[0]*&quot"
        res = re.search(pattern, text)

        degree, minutes, seconds = list(map(float, res[1:3]))

        half = minutes / 60 + seconds / 3600

        # Return degree decimal in string
        return degree + half

    # Returns the raw stdout of the subprocess, which is html
    def get_html(self):
        return self.__read()

    # Returns the converted stdout from html to dict
    def get_dict(self):
        raw = self.__read()
        meta_dict = {}
        li = []
        """ 
        raw[:raw.find("</table>")-7] gives us the required data
        1> We find the index of </table> which is at
           the end of the output string using .find()
        2> We do -7 to remove the </tr> at the very end as well.
        3> We get the string util we reach the combination of
           above indexes (combination of </table> index and -7).
        4> .split("</td>") removes the </td> at the end of every line and creates a list.
        5> Lastly, using for loop we iterate over each item and get element
           after <td>. hence, removing <td>.
    
        """
        for item in raw[: raw.find("</table>") - 7].split("</td>"):
            li.append(item[item.find("<td>") + len("<td>") :])
        # converting the above list to dict, with first the key then value

        latitude, longitude = None, None
        for i in range(0, len(li) - 1, 2):
            val = li[i + 1]

            # &#39 is used to represent minutes in HTML
            pattern1 = r"&#39"
            # &quot is used to represent seconds in HTML
            pattern2 = r"&quot"

            # Substitute the pattern with its appropriate sybmol(if it exists)
            if re.search(pattern1, val) != None:
                val = re.sub(pattern1, "'", val)
            if re.search(pattern2, val) != None:
                val = re.sub(pattern2, '"', val)
            meta_dict[li[i]] = val

            if li[i] == "GPS Latitude":
                latitude = self.__convert_dms_to_dd(li[i + 1])
            elif li[i] == "GPS Longitude":
                longitude = self.__convert_dms_to_dd(li[i + 1])

        if (latitude and longitude) != None:
            meta_dict["GPS Coordinates"] = str(latitude) + " " + str(longitude)
        return meta_dict
