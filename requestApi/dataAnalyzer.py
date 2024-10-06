from pymongo import MongoClient
import os
import google.generativeai as genai
import json
# Assign an envoriemant API key
os.environ['GOOGLE_API_KEY'] = 'AIzaSyC4iaf23A4TE1QDusMADUzG3GgC72u4eco'
# Hizmeti yapılandırın

class Planet:
    def __init__(self, pl_name, distance,pl_mass,rowupdate):
        self.pl_name = pl_name
        self.distance = distance
        self.pl_mass = pl_mass

        self.rowupdate = rowupdate
        

    def __str__(self) -> str:
        return f"Planet name {self.pl_name},Planet Distance from earth [pc]:{self.distance},Planet massive{self.distance}*Earth Massive; Planet Row Update {self.rowupdate}"

class PlanetsDatabase:
    def __init__(self, db_uri, db_adi):
        self.client = MongoClient(db_uri)
        self.db = self.client[db_adi]
        self.collection = self.db['planetCollection']

    def Planets(self):
        Planets_array = []  # A list add storage planets
        planets_description = []
        data = {}

        if "planets" not in data:
                data["planets"] = []  
                
        for document in self.collection.find():
            try:
                planet = Planet(document['pl_name'], document['sy_dist'],document['pl_bmasse'],document['rowupdate'])  # Dökümandan Planet objesi oluştur

            except:
                
                break
            
            
            genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
            generation_config = {"temperature":0.9,"top_p":1,"top_k":1,"max_output_tokens":2048}
            model = genai.GenerativeModel("gemini-pro",generation_config=generation_config)
            response = model.generate_content([f"Create a descriptive text for the following planets based on the data:{planet}"])

            t1 = response.text.split("\"text\"")[0]
            
            t2 = t1.split("\"")[0]
            planets_description.append(f"{t2}")

            # Append the new data
            js = {
                planet.pl_name:t2 
            }
            data["planets"].append(js)

            # Write the updated data back to the fil
            
            Planets_array.append(planet)  # Add planet object to the list

        with open('desc.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)
        


    def close(self):
        self.client.close()

def main():
    db = PlanetsDatabase('mongodb://localhost:27017/', 'planet_datas')
    db.Planets()
        
    
    db.close()
if __name__ == "__main__":
    main()
