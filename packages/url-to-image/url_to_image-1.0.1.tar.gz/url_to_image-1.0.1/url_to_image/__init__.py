from urllib.request import urlopen
from PIL import Image, ImageTk
import io

def convert(url,which):
	image_url = urlopen(url)
	image_bytes = io.BytesIO(image_url.read())
	image = Image.open(image_bytes)
	return specific_type(image,which)

def specific_type(image,which):
	if which == "pil":
		return image
	elif which == "tk":
		tk_img = ImageTk.PhotoImage(image)
		image.close()
		return tk_img