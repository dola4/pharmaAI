from models.prescription import Prescription
from bson.objectid import ObjectId
import datetime

def test_create():
    print("Creating")
    client_id = ObjectId("652fe2d3ea08c4a353f239f9")
    prescription1 = Prescription(
        client_id,
        datetime.datetime.today(),
        datetime.datetime.today() + datetime.timedelta(days=30),
        "acid",
        "CHUM",
        "Dr. House",
        30
    )
    prescription2 = Prescription(
        client_id,
        datetime.datetime.today(),
        datetime.datetime.today() + datetime.timedelta(days=30),
        "psylocibine",
        "CHUM",
        "Dr. House",
        30
    )

    prescription1.create()
    prescription2.create()

def test_get_all_prescriptions():
    print("Getting all prescriptions")
    prescriptions = Prescription.get_all_prescriptions()
    for prescription in prescriptions:
        print(prescription.to_dict())

def test_get_prescription_by_client_id():
    print("Getting prescription by client id")
    client_id = ObjectId("652d5464d0cceeff17fbb2d4")
    prescriptions = Prescription.get_prescription_by_client_id(client_id)
    for prescription in prescriptions:
        print(prescription.to_dict())

def test_get_prescription_by_id():
    print("Getting prescription by id")
    prescription_id = ObjectId("652e9bd6f646f34919dd2936")
    prescription = Prescription.get_prescription_by_id(prescription_id)
    print(prescription.to_dict())


test_create()
#test_get_all_prescriptions()
#test_get_prescription_by_client_id()
#test_get_prescription_by_id()
