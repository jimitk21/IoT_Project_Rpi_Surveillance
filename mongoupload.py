import pymongo

# MongoDB Setup
mongo_url = "MONGO_URL"
client = pymongo.MongoClient(mongo_url)
db = client['YourDatabaseName']  # Replace with your database name
collection = db['YourCollectionName']  # Replace with your collection name

# Load image and convert to binary
with open('/home/jimit/Pictures/Screenshots/test1.png', 'rb') as img_file:
    img_data = img_file.read()

# Insert the image binary data into MongoDB
document = {
    'filename': 'test1.png',
    'image_data': img_data
}
collection.insert_one(document)

print("Image uploaded to MongoDB successfully.")