from models.drug import Drug
from bson.objectid import ObjectId

def test_create():
    drug1 = Drug(
        'ghb',
        10,
        100,
        200,
    )
    drug2 = Drug(
        "psylocibine",
        10,
        100,
        200,
    )
    drug2.create()
    drug1.create()

def test_get_all_drugs():
    print (Drug.get_all_drugs())
    
def test_get_drug_by_id():
    drug_id = "652d72fadd4e11a00e9e82a4"
    drug_id = ObjectId(drug_id)
    print(Drug.get_drug_by_id(drug_id))

def test_update():
    drug_id = "652d72fadd4e11a00e9e82a5"
    drug = Drug(
        "MDMA",
        10, 
        60,
        120,
    )
    drug.update(drug_id)

def test_delete():
    drug_id = "652d72fadd4e11a00e9e82a5"
    drug_id = ObjectId(drug_id)
    Drug.delete(drug_id)

#test_create()
#test_get_all_drugs()
#test_get_drug_by_id()
#test_update()
test_delete()