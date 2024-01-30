from models.adresse import Adresse
from bson.objectid import ObjectId


def test_create():

    client_id = "652fe2d3ea08c4a353f239f9"

    adresse1 = Adresse(
        '1289',
        'rue de la paix',
        'Montreal',
        "H1A1R4",
        'Qc',
        'Canada',
        []
    )
    adresse2 = Adresse(
        '12',
        'rue de la guerre',
        'Montreal',
        "H3A1G4",
        'Qc',
        'Canada',
        []
    )
    
    adresse2.create(client_id)
    adresse1.create(client_id)

def test_get_adress_by_client_id():
    client_id = "652d5464d0cceeff17fbb2d4"
    client_adress = Adresse.get_adress_by_client_id(client_id)
    print(client_adress)

def test_update():
    adress_id = '652d64b711e237bbb2c24edb'
    adress_id = ObjectId(adress_id)
    updated_adress = Adresse(
        door='12061',
        street='Avenue Copernic',
        city='Montreal',
        postal_code="H1E1W1",
        state='Qc',
        country='Canada',
    )
    updated_adress.update(adress_id)


def test_delete():
    adress_id = "652d6a31885f1ffd6cf9983c"
    adress_id = ObjectId(adress_id)
    Adresse.delete(adress_id)

#test_create()
#test_get_adress_by_client_id()
#test_update()
#test_delete()

