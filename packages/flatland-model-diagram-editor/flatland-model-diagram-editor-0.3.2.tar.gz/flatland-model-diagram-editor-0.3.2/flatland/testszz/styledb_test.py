"""
styledb_test.py – Ensure that we can build the drawingzz domain databasezz
"""
# We might move this test elsewhere, so let's use absolute paths from the package root
from flatland.databasezz.flatlanddb import FlatlandDB
from flatland.drawing_domainzz.styledb import StyleDB

fdb = FlatlandDB()
sdb = StyleDB(drawing_type='Starr class diagram', presentation='diagnostic')
print("Finished")
