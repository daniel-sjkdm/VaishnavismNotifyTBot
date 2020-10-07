from helpers.vaishnadb import VaishnaDBPG()

vdb = VaishnaDBPG()

events = vdb.get_iskcon_events("2020", fetch_by="year")
print(events)

print("----------------------------------------------")
events = vdb.get_iskcon_events("2020", fetch_by="year")
print(events)


print("--------------------------------------------------")
events = vdb.get_iskcon_events("January", fetch_by="month")
print(events)