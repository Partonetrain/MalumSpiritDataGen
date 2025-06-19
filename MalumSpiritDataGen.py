import os
import json
import time
import csv
from dataclasses import dataclass

ENTRIES_FILE_NAME = "entries.csv"
TEMPLATE_FILE_NAME = "template.json"
SPIRIT_DIR = "malum/spirit_data/entity"
entries = [] 
start_time = 0

@dataclass
#constructor generated automatically
class Entry:
    modid: str
    mobname: str
    primaryType: str
    sacredSpirits: int
    wickedSpirits: int
    arcaneSpirits: int
    eldritchSpirits: int
    aerialSpirits: int
    aqueousSpirits: int
    earthenSpirits: int
    infernalSpirits: int

def main():
  print('MalumSpiritDataGen by Partonetrain')
  start_time = time.perf_counter()
  checkFilesExist()
  ParseEntries()
  recipes_generated = FillTemplate()
  end_time = time.perf_counter()
  execution_time = end_time - start_time
  
  print(f"Generated {recipes_generated} spirit data files in {execution_time:.4f} seconds")

def checkFilesExist():
    if(not (os.path.exists(ENTRIES_FILE_NAME) and os.path.exists(TEMPLATE_FILE_NAME)) ):
        print("Necessary files do not exist, exiting...")
        time.sleep(3)
        quit()

def ParseEntries():
  with open(ENTRIES_FILE_NAME, 'r') as csv_file:
    reader = csv.DictReader(csv_file, skipinitialspace=True)
    #dictreader allows addressing with str

    item_count = 0
    line = 1 #ignore header
    for row in reader:
        if(not "#" in row["mobId"]):
          split = row["mobId"].split(":")
          entry = Entry(
                    modid=split[0],
                    mobname=split[1],
                    primaryType=row["primaryType"],
                    sacredSpirits=int(row["sacredSpirits"]),
                    wickedSpirits=int(row["wickedSpirits"]),
                    arcaneSpirits=int(row["arcaneSpirits"]),
                    eldritchSpirits=int(row["eldritchSpirits"]),
                    aerialSpirits=int(row["aerialSpirits"]),
                    aqueousSpirits=int(row["aqueousSpirits"]),
                    earthenSpirits=int(row["earthenSpirits"]),
                    infernalSpirits=int(row["infernalSpirits"]),
                )
          entries.append(entry)
          line = line + 1
          item_count = item_count + 1
          #print(entry)
          
    print(f"parsed {item_count} entries")
    csv_file.close()

def FillTemplate():
  recipes_generated = 0
  tier = 0
  
  template_data = ""
  with open(TEMPLATE_FILE_NAME, 'r') as json_file:
    template_data = json.load(json_file)

  tryMakeDir(SPIRIT_DIR)
  for entry in entries:
    recipe_data = ""
    #print("filling template for " + str(entry))
    path = SPIRIT_DIR + "\\" + entry.modid
    tryMakeDir(path)
    recipe_data = template_data

    recipe_data["registry_name"] = entry.modid + ":" + entry.mobname

    recipe_data["primary_type"] = entry.primaryType
    recipe_data["spirits"].clear()
    #I don't know why but without the clear it retains the
    #spirits of the previous entry

    if(entry.sacredSpirits > 0):
        print(f"{entry.modid}:{entry.mobname} has {entry.sacredSpirits} sacred")
        recipe_data["spirits"].append({"sacred": entry.sacredSpirits})
    if(entry.wickedSpirits > 0):
        print(f"{entry.modid}:{entry.mobname} has {entry.wickedSpirits} wicked")
        recipe_data["spirits"].append({"wicked": entry.wickedSpirits})
    if(entry.arcaneSpirits > 0):
        print(f"{entry.modid}:{entry.mobname} has {entry.arcaneSpirits} arcane")
        recipe_data["spirits"].append({"arcane": entry.arcaneSpirits})
    if(entry.eldritchSpirits > 0):
        print(f"{entry.modid}:{entry.mobname} has {entry.eldritchSpirits} eldritch")
        recipe_data["spirits"].append({"eldritch": entry.eldritchSpirits})
    if(entry.aerialSpirits > 0):
        print(f"{entry.modid}:{entry.mobname} has {entry.aerialSpirits} aerial")
        recipe_data["spirits"].append({"aerial": entry.aerialSpirits})
    if(entry.aqueousSpirits > 0):
        print(f"{entry.modid}:{entry.mobname} has {entry.aqueousSpirits} aqueous")
        recipe_data["spirits"].append({"aqueous": entry.aqueousSpirits})
    if(entry.earthenSpirits > 0):
        print(f"{entry.modid}:{entry.mobname} has {entry.earthenSpirits} earthen")      
        recipe_data["spirits"].append({"earthen": entry.earthenSpirits})
    if(entry.infernalSpirits > 0):
        print(f"{entry.modid}:{entry.mobname} has {entry.infernalSpirits} infernal")      
        recipe_data["spirits"].append({"infernal": entry.infernalSpirits})

                                      
    recipe_path = path + "\\" + entry.mobname + ".json"
    with open(recipe_path, "w") as output_file:
        json.dump(recipe_data, output_file)
        print("Generated spirit data for " + entry.modid + ":" + entry.mobname)
        recipes_generated = recipes_generated + 1
    output_file.close()
  return recipes_generated

def getTimeFromTier(tier):
    if(tier == 0): # Wood
        return 250
    if(tier == 1): # Gold
        return 300
    if(tier == 2): # Stone
        return 500
    if(tier == 3): # Iron
        return 750
    if(tier == 4): # Diamond
        return 1500
    if(tier == 5): # Netherite
        return 2000
    if(tier > 5): # Anything higher
        return 3000

def tryMakeDir(path):
    os.makedirs(path, exist_ok=True) #mkdirs can create subdirs

if __name__ == '__main__':
  main()
