import pymongo
from PIL import Image
import io

# MongoDB setup
mongo_url = ""
client = pymongo.MongoClient(mongo_url)
db = client['YourDatabaseName']  # Replace with your database name
collection = db['YourCollectionName']  # Replace with your collection name

# Retrieve the document with the image
document = collection.find_one({'filename': 'test1.png'})  # Adjust if you have other identifiers

# Check if the document is found
if document and 'image_data' in document:
    img_data = document['image_data']
   
    # Convert binary data back to an image
    img = Image.open(io.BytesIO(img_data))
   
    # Display the image
    img.show()
   
    # Optionally, save the image locally
    img.save('/home/jimit/Pictures/Screenshots/retrieved_test1.png')
    print("Image retrieved and saved as 'retrieved_test1.png'.")
else:
    print("Image not found in MongoDB.")