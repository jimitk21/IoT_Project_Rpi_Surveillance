
from supabase import create_client, Client

url = "URL"
key = "APIKEY"

supabase: Client = create_client(url, key)

# Open the image file
with open("image.jpg", "rb") as file:
    try:
        # Upload the image to Supabase
        result = supabase.storage.from_("jimit-bucket").upload("image.jpg", file)
       
        # Get the public URL of the uploaded image
        public_url = supabase.storage.from_("jimit-bucket").get_public_url("image.jpg")
       
        print(f"Image uploaded successfully. Public URL: {public_url}")
    except Exception as e:
        print(f"Error uploading image: {e}")