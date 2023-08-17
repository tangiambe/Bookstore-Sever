from pymongo import MongoClient

# mongodb+srv://<username>:<password>@books.ondwxvg.mongodb.net/
uri = "mongodb+srv://cody:team2password@books.ondwxvg.mongodb.net/"
client = MongoClient(uri)

try:
    print("Connected to MongoDB")
    # Perform database operations here
except Exception as e:
    print("Error connecting to MongoDB:", e)
finally:
    # Don't forget to close the connection when done
    client.close()