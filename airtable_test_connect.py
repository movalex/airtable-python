import os
from pyairtable import Api


token = os.environ["AIRTABLE_TOKEN"]
api = Api(token)



def get_base_by_name(name=None):
    if not name:
        return
    for base in api.bases():
        # print(base.name)
        if base.name == name:
            return base
        


base = get_base_by_name("Lemonade Stand Inventory")

for table in base.tables():
    print(table.name)
    for records in table.iterate():
        print(records[0].get("fields").keys())



