from PIL import Image
from PIL.ExifTags import TAGS
from PIL.ExifTags import GPSTAGS

class ImageMiner:
    def __init__(self,path):
        self.path = path
        self.img = Image.open(self.path)
        
    def show_image(self):
        self.img.show()

    def create_exif_dict(self):
        data = {}
        for tag, value in self.img._getexif().items():
            if isinstance(value,bytes):
                data[TAGS.get(tag,"Unknown")]=value.decode('utf-8',errors='ignore')
            else:
                data[TAGS.get(tag,"Unknown")]=value
        return data

    def improve_dict(self):
        data = self.create_exif_dict()
        for key, value in data.items():
            if key == "GPSInfo":
                gpsinfo = {}
                for key in data['GPSInfo'].keys():
                    decode = GPSTAGS.get(key,key)
                    gpsinfo[decode] = data['GPSInfo'][key]
                data["GPSInfo"] = gpsinfo
        return data

    def print_data(self):
        data = self.improve_dict()
        print(data)



#---------------------------TEST------------------------------------
path = r"C:\\Users\\Aquib\\Pictures\\pic.jpg"
obj = ImageMiner(path)
obj.show_image()
