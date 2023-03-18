import PIL.Image
import PIL.ExifTags
from geopy.geocoders import Nominatim
import gmplot.gmplot



print("Example: Sample_image.png")
print("                      ^^^")
print("An format of the image MUST be included")
get_image = input("Enter the directory of the image -> ")
out_name = input("Enter name of the output -> ")

try:
    img = PIL.Image.open(f"{get_image}")
except:
    raise Exception("An exception occurred when trying to open the image. Please check if the image exists or the "
                    "right format. Program terminated")

exif = {
    PIL.ExifTags.TAGS[f]: b
    for f, b in img._getexif().items()
    if f in PIL.ExifTags.TAGS
}
try:
    location = exif["GPSInfo"]
except:
    raise Exception("An image with no geotag was found. Program terminated")

north = exif["GPSInfo"][2]
east = exif["GPSInfo"][4]

lat = (north[0] * 60) + (north[1] * 60) * north[2] / 60 / 60
long = (east[0] * 60) + (east[1] * 60) * east[2] / 60 / 60
lat, long = float(lat), float(long)

print(lat, long)

map = gmplot.GoogleMapPlotter(lat, long, 8)
map.marker(lat, long, "red")
map.draw(f"{out_name}.html")

geoloc = Nominatim(user_agent="GetLoc")
locnm = geoloc.reverse(f"{lat}, {long}")
print(locnm.address)
