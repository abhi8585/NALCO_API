from email import message


# from sympy import residue
#from app import transporter
#from tabulate import tabulate
from app.loadplanning import blueprint
from flask_restful import Resource, Api
from flask import jsonify, render_template, redirect, request, url_for
import json
#from app.base.util import verify_pass
#from app.models import audit, bag, depotomaster, depovendor, sku, auditsku, bagtosku, audittobag, disttobag, pickup, picktobag, deviatedbag, userinfo
#from app import db
#from app.models import depoinventory, deviateddepobag, depopickup
import datetime

#from app import mail

from flask_mail import Message


def make_database_connection():
    import pyodbc
    cnxn = pyodbc.connect(driver='{FreeTDS}', host='115.124.119.236', database='NALCO_DISPATCH',
                        trusted_connection='no', user='Aipalatte2', password='guest2@Nalco2022',
                        TrustServerCertificate='yes')
    return cnxn


# function to return the data for screen1 

@blueprint.route('/get_virtual_truck_details',methods=['GET','POST'])
def get_virtual_truck_details():
    try:
        data = request.get_json(force=True)
        cnxn = make_database_connection()
        cursor = cnxn.cursor()
        try:
            if data["dispatch_date"] == "" or data["dispatch_date"] == None:
                return jsonify(status=400, message = "No Dispatch date provided")
            else:
                dispatch_date = data["dispatch_date"]
        except Exception as e:
            return jsonify(status=400, message = "No Dispatch date provided")
        
        try:
            if data["customer_code"] == "" or data["customer_code"] == None:
                return jsonify(status=400, message = "No Customer code provided")
            else:
                customer_code = data["customer_code"]
        except Exception as e:
            print(e)
            return jsonify(status=400, message = "No Dispatch date provided")

        # getting data for virtual truck numbers
        # order number from Order Header Table with dispatch date and vendor code
        # Order number join PreVehicleLoading Table
        # Join Order details table on basis of line item to get item details
        # Join Virtual Truck Mapping on basis PreloadID

        sql_query = """
                    select * from 
                    QN_Tbl_Sales_Order_HDR
                    INNER JOIN QN_Tbl_Vehicle_Load_Planning
                    ON QN_Tbl_Vehicle_Load_Planning.Sales_Order_Number = QN_Tbl_Sales_Order_HDR.Sales_Order_Number
                    INNER JOIN QN_Tbl_Sales_Order_Detail
                    ON QN_Tbl_Sales_Order_Detail.Line_item_Number = QN_Tbl_Vehicle_Load_Planning.Line_item_Number
                    INNER JOIN QN_Tbl_Virtual_Truck_Pre_Load_Mapping
                    On QN_Tbl_Virtual_Truck_Pre_Load_Mapping.VehiclePlanningID = QN_Tbl_Vehicle_Load_Planning.PreLoadID
                    where QN_Tbl_Sales_Order_HDR.Plan_Delivery_Date = '{0}' and QN_Tbl_Sales_Order_HDR.Customer_Code = '{1}'
                    """.format(dispatch_date, customer_code)
        cursor.execute(sql_query)
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        virtual_truck_data = []
        for temp in results:
            temp_obj = dict()
            temp_obj["virtual_truck_number"] = temp["Virtual_Truck_Number"]
            temp_obj["dispatch_order_number"] = temp["Sales_Order_Number"]
            temp_obj["line_item_number"] = temp["Line_item_Number"]
            # need to add sku code column after discussion with IDRIS JI
            temp_obj["transportation_by"] = temp["Vehicle_Type"]
            temp_obj["transporter_code"] = temp["Transporter_Code"]
            temp_obj["truck_capacity"] = temp["Capacity_Of_Vehicle"]
            temp_obj["diameter"] = temp["Diameter"]
            # need to add code for grade after discussion with IDRIS JI
            temp_obj["uts"] = temp["UTS_From"]
            temp_obj["elongation"] = temp["Elongation_From"]
            virtual_truck_data.append(temp_obj)
        return jsonify(status=200, data=virtual_truck_data)
    except Exception as e:
        print(e)
        return jsonify(status=500)