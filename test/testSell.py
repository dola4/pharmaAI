from models.sell import Sell
from bson.objectid import ObjectId
import datetime

client_id = ObjectId("652fe2d3ea08c4a353f239f9")

def test_create():
    
    prescrip_id1 = ObjectId("652fe5d934b29db8a8c2a3c5")
    prescrip_id2 = ObjectId("652fe5d934b29db8a8c2a3c6")
    sell1 = Sell(
        datetime.datetime.today().strftime('%Y-%m-%d'),
        client_id,
        [prescrip_id1, prescrip_id2]
    )
    sell1.create()

def test_get_all_sells():
    print("Getting all sells")
    sells = Sell.get_all_sells()
    for sell in sells:
        print(sell.to_dict())


def get_sells_by_client_id():
    client_id = ObjectId("652fe2d3ea08c4a353f239f9")
    sells = Sell.get_sells_by_client_id(client_id)
    for sell in sells:
        print(sell.to_dict())

def test_get_sell_by_id():
    sell_id = ObjectId("652feaf4c1657afef25fb6b0")    
    sell = Sell.get_sell_by_id(sell_id)
    print(sell.to_dict())

    

#test_create()
test_get_all_sells()
#get_sells_by_client_id()
#test_get_sell_by_id()
