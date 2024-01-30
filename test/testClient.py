from models.client import Client
from bson.objectid import ObjectId



def test_create():
    client1 = Client(
        'Dummy',
        'retarded',
        63,
        'Male',
        'dumretard@example.com',
        15142148292,
    )
    client2 = Client(
        'F', 
        'Word',
        32,
        'female',
        'fuck@example.com',
        15142148292,
    )
    client2.create()
    client1.create()

def test_find_all_client():
    clients = Client.get_all_client()
    for client in clients:
        print(client.to_dict())

def test_get_client_by_email():
    email =  'fuck@example.com'
    client = Client.get_client_by_email(email)
    print(f'nom du client : {client.first_name} {client.last_name}')

def test_update_client():
    client_id = "652d5464d0cceeff17fbb2d3"
    client_id = ObjectId(client_id)
    updated_client = Client(
        "fuck",
        "Uall",
        34,
        "female",
        "fUa@example.com",
        15142148292,
    )
    updated_client.update_client(client_id)
    print(updated_client)

def test_delete_client():
    client_id = "652d5464d0cceeff17fbb2d3"
    client_id = ObjectId(client_id)
    Client.delete_client(client_id)




#test_create()
#test_find_all_client()
#test_get_client_by_email()
#test_update_client()
#test_delete_client()