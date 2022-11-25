from email import message
from app.delivery import blueprint
from flask_restful import Resource, Api
from flask import jsonify, render_template, redirect, request, url_for
import json
import datetime
# from helpers.connection import make_database_connection
# from app.helpers.connection import make_database_connection
from app.modify.routes import material_description

#from app import mail

from flask_mail import Message


def make_database_connection():
    import pyodbc
    cnxn = pyodbc.connect(driver='{FreeTDS}', host='115.124.119.236', database='NALCO_DISPATCH',
                        trusted_connection='no', user='Aipalatte2', password='guest2@Nalco2022',
                        TrustServerCertificate='yes')
    return cnxn

# function for getting material description with material code




# function to return the data for screen1 

@blueprint.route('/get_delivery_order',methods=['GET','POST'])
def get_delivery_order():
    # data = request.get_json(force=True)
    data = request.args
    # exception handling for reading input parameters
    try:
        dispatch_date = data["dispatch_date"]
        if dispatch_date == "" or dispatch_date == None:
            return jsonify(status=400,message="Please Select Dispatch Date!")
    except:
        return jsonify(status=400,message="Please Select Dispatch Date!")
    default_query = """
                select *
                from QN_Tbl_Sales_Order_HDR
                INNER JOIN QN_Tbl_Sales_Order_Transporter_Detail
                ON ( QN_Tbl_Sales_Order_Transporter_Detail.Sales_Order_Number = QN_Tbl_Sales_Order_HDR.Sales_Order_Number)
                WHERE QN_Tbl_Sales_Order_HDR.Plan_Delivery_Date = '{0}' 
            """.format(dispatch_date)
    for key, value in data.items():
        if key == "customer_code":
            if value == "" or value == None:
                pass
            else:
                temp_query = "AND QN_Tbl_Sales_Order_HDR.Customer_Code =  '{0}' ".format(value)
                default_query = default_query + temp_query
        if key == "order_number":
            if value == "" or value == None:
                pass
            else:
                temp_query = "AND QN_Tbl_Sales_Order_HDR.Sales_Order_Number = '{0}' ".format(value)
                default_query = default_query + temp_query
        if key == "transporter":
            if value == "" or value == None:
                pass
            else:
                temp_query = "AND QN_Tbl_Sales_Order_Transporter_Detail.Transporter_code = '{0}' ".format(value)
                default_query = default_query + temp_query
    print(default_query)
    cnxn = make_database_connection()
    cursor = cnxn.cursor()
    cursor.execute(default_query) 
    columns = [column[0] for column in cursor.description]
    results = []
    main_results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    for temp in results:
        temp_obj  = {}
        temp_obj['delivery_date'] = temp['Plan_Delivery_Date'].strftime("%d-%m-%Y")
        temp_obj['order_number'] = temp['Sales_Order_Number']
        temp_obj['customer_code'] = temp['Customer_Code']
        temp_obj['customer_name'] = temp['Customer_Name']
        temp_obj['destination'] = temp['Destination']
        temp_obj['transporter_name'] = temp['Transporter_Name']
        temp_obj['transporter_code'] = temp['Transporter_Code']
        temp_obj['delivery_quantity'] = float(temp['Plan_Del_Qty'])
        temp_obj["status"] = temp["Status"]
        main_results.append(temp_obj)
    # print(main_results)
    return jsonify(status=200,data=main_results)


# function to return the data for screen2

@blueprint.route('/get_delivery_order_details',methods=['GET','POST'])
def get_delivery_order_details():
    # data = request.get_json(force=True)
    data = request.args
    # exception handling for reading input parameters
    try:
        order_number = data["order_number"]
        if order_number == "" or order_number == None:
            return jsonify(status=400,message="Please Select Order Number!")
    except:
        return jsonify(status=400,message="Please Select Order Number!")
    import pyodbc
    cnxn = pyodbc.connect(driver='{FreeTDS}', host='115.124.119.236', database='NALCO_DISPATCH',
                      trusted_connection='no', user='Aipalatte2', password='guest2@Nalco2022',
                      TrustServerCertificate='yes')
    cursor = cnxn.cursor()
    sql_query = """ 
        select * from 
            QN_Tbl_Sales_Order_Detail where Sales_Order_Number = '{0}'
            """.format(order_number)
    cursor.execute(sql_query) 
    columns = [column[0] for column in cursor.description]
    results = []
    main_results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    for temp in results:
        temp_obj = {}
        temp_obj['order_number'] = temp['Sales_Order_Number']
        temp_obj['line_item_number'] = temp['Line_item_Number']
        temp_obj['material_code'] = temp['Material_Code']
        # need to add code for material description
        temp_description = material_description(dict(material_code=temp['Material_Code']),cursor)
        temp_obj['material_description'] = temp_description['material_description']
        temp_obj['quantity'] = float(temp['Quantity']) if temp['Quantity'] else float(0.00)
        temp_obj['status'] = temp['Status']
        main_results.append(temp_obj)
    # print(main_results)
    return jsonify(status=200,data=main_results)


#function to get the data for screen truck planning screen1

@blueprint.route('/get_truck_planning_orders',methods=['GET','POST'])
def get_truck_planning_orders():
    data = request.args
    # exception handling for reading input parameters
    try:
        dispatch_date = data["dispatch_date"]
        if dispatch_date == "" or dispatch_date == None:
            return jsonify(status=400,message="Please Select Dispatch Date!")
    except:
        return jsonify(status=400,message="Please Select Dispatch Date!")
    default_query = """
                             select *
                    from QN_Tbl_Sales_Order_HDR
                    INNER JOIN QN_Tbl_Sales_Order_Detail
                    ON ( QN_Tbl_Sales_Order_Detail.Sales_Order_Number = QN_Tbl_Sales_Order_HDR.Sales_Order_Number)
                    WHERE QN_Tbl_Sales_Order_HDR.Plan_Delivery_Date = '{0}'
                    """.format(dispatch_date)
    for key, value in data.items():
        if key == "customer_code":
            if value == None or value == "":
                pass
            else:
                temp_query = "AND Customer_Code = '{0}' ".format(value)
                default_query = default_query + temp_query
    import pyodbc
    cnxn = pyodbc.connect(driver='{FreeTDS}', host='115.124.119.236', database='NALCO_DISPATCH',
                      trusted_connection='no', user='Aipalatte2', password='guest2@Nalco2022',
                      TrustServerCertificate='yes')
    cursor = cnxn.cursor()
    # sql_query = """ 
    #     AND Customer_Code = '{1}'
    #         """.format(dispatch_date, customer_code)
    cursor.execute(default_query) 
    columns = [column[0] for column in cursor.description]
    results = []
    main_results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    for temp in results:
        temp_obj = dict()
        temp_obj["order_number"] = temp["Sales_Order_Number"]
        temp_obj["line_item_number"] = temp["Line_item_Number"]
        temp_obj["material_code"] = temp["Material_Code"]
        # add code for material description
        temp_description = material_description(dict(material_code=temp['Material_Code']),cursor)['material_description']
        temp_obj["material_description"] = temp_description
        temp_obj["weight"] = temp["Net_Weight"]
        temp_obj["uom"] = temp["UOM"]
        temp_obj["quantity"] = float(temp["Quantity"]) if temp["Quantity"] else float(0.00)
        temp_obj["status"] = temp["Status"]
        main_results.append(temp_obj)
    print(main_results)
    return jsonify(status=200,data=main_results)


# api to return transporter code as per Order and Line Item Number

@blueprint.route('/get_transporter_and_truck_details',methods=['GET','POST'])
def get_transporter_and_truck_details():
    data = request.args
    try:
        order_number = data["order_number"]
        if order_number == "" or order_number == None:
            return jsonify(status=400,message="Please Select Order Number!")
    except:
        return jsonify(status=400,message="Please Select Order Number!")
    try:
        line_item_number = data["line_item_number"]
        if line_item_number == "" or line_item_number == None:
            return jsonify(status=400,message="Please Select Line Item Number!")
    except:
        return jsonify(status=400,message="Please Select Line Item Number!")
    # sql execution to get the transporter code details
    # make connection

    import pyodbc
    cnxn = pyodbc.connect(driver='{FreeTDS}', host='115.124.119.236', database='NALCO_DISPATCH',
                        trusted_connection='no', user='Aipalatte2', password='guest2@Nalco2022',
                        TrustServerCertificate='yes')
    cursor = cnxn.cursor()
    sql_query = """ 

            select Transporter_Code from QN_Tbl_Sales_Order_Transporter_Detail
            where Sales_Order_Number = '{0}' and Sales_order_item_Number = '{1}'
            """.format(order_number, line_item_number)
    cursor.execute(sql_query) 
    columns = [column[0] for column in cursor.description]
    results = []
    main_results = []
    final_results = []
    for row in cursor.fetchall():
        results.append(dict(zip(columns, row)))
    for temp in results:
        temp_obj = {}
        transporter_code = temp["Transporter_Code"]
        temp_obj[transporter_code] = []
        # print(temp_obj)
        sql_query = """ 
                select Capacity from QN_Tbl_Truck_Master
                where Transporter_Code = '{0}'
            """.format(transporter_code)
        cursor.execute(sql_query) 
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            temp_obj[transporter_code].append(dict(zip(columns, row))['Capacity'])
        final_results.append(temp_obj)
    return jsonify(status=200, data = final_results)


# api to save the truck planning data for screen 3.1
# need to add line item number in the values after discussion with Idris ji
@blueprint.route('/insert_vehicle_planning_details',methods=['GET','POST'])
def insert_vehicle_planning_details():
        data = request.get_json(force=True)
        load_vehicle_mapping = list()
        try:
            vehicle_planning_data = data["vehicle_planning_data"]
            # print(vehicle_planning_data)
        except:
            return jsonify(status=400,message="No Vehicle Planning Data")
        # making connection
        import pyodbc
        cnxn = pyodbc.connect(driver='{FreeTDS}', host='115.124.119.236', database='NALCO_DISPATCH',
                        trusted_connection='no', user='Aipalatte2', password='guest2@Nalco2022',
                        TrustServerCertificate='yes')
        for temp in vehicle_planning_data:
            values = []
            try:
                if temp["order_number"] == "" or temp["order_number"] == None:
                    return jsonify(status=400, message="No order number selected")
                else:
                    values.append(temp["order_number"])
            except:
                return jsonify(status=400, message="No order number selected")
            # reading line item number

            try:
                if temp["line_item_number"] == "" or temp["line_item_number"] == None:
                    return jsonify(status=400, message="No Line Number selected")
                else:
                    values.append(temp["line_item_number"])
            except:
                return jsonify(status=400, message="No Line number selected")
            
            try:
                if temp["transporter_code"] == "" or temp["transporter_code"] == None:
                    return jsonify(status=400, message="No Transporter Code selected")
                else:
                    values.append(temp["transporter_code"])
            except:
                return jsonify(status=400, message="No Transporter Code selected")

            try:
                if temp["no_of_vehicle"] == "" or temp["no_of_vehicle"] == None:
                    return jsonify(status=400, message="No Total Vehicle selected")
                else:
                    values.append(temp["no_of_vehicle"])
            except:
                return jsonify(status=400, message="No Total Vehicle selected")

            try:
                if temp["vehicle_capacity"] == "" or temp["vehicle_capacity"] == None:
                    return jsonify(status=400, message="No Vehicle Capacity selected")
                else:
                    values.append(temp["vehicle_capacity"])
            except:
                return jsonify(status=400, message="No Vehicle Capacity selected")

            try:
                if temp["vehicle_type"] == "" or temp["vehicle_type"] == None:
                    return jsonify(status=400, message="No Vehicle Type selected")
                else:
                    values.append(temp["vehicle_type"])
            except:
                return jsonify(status=400, message="No Vehicle Type selected")
            try:
                if temp["virtual_truck_numbers"] == "" or temp["virtual_truck_numbers"] == None:
                    return jsonify(status = 400, message = "No Virtual Truck Number selected")
                else:
                    virtual_truck_numbers = temp["virtual_truck_numbers"]
               
            except:
                return jsonify(status = 400, message = "No Virtual Truck Number selected")
            values = tuple(values)
            sql_query = """
                INSERT INTO QN_Tbl_Vehicle_Load_Planning (Sales_Order_Number, Line_item_Number, Transporter_Code, No_Of_Truck_Wagons, Capacity_Of_Vehicle, Vehicle_Type)
            VALUES {0};
            """.format(values)
            try:
                cursor = cnxn.cursor()
                cursor.execute(sql_query)
                cnxn.commit()
                cursor.execute("SELECT @@IDENTITY AS ID;")
                pre_load_id = int(cursor.fetchone()[0])
                load_vehicle_mapping.append(dict(pre_load_id=pre_load_id,
                                            virtual_truck_numbers=virtual_truck_numbers))
            except Exception as e:
                print(e)
                cnxn.rollback()
                return jsonify(status=500, message="Server Error while inserting Data!")
        
        # # mapping virtual truck numbers with the PreLoad ID in the newly constructed table as discussed.
        # print(load_vehicle_mapping)
        try:
            for val in load_vehicle_mapping:
                for temp in val["virtual_truck_numbers"]:
                    sql_query = """
                            INSERT INTO QN_Tbl_Virtual_Truck_Planning (PreLoadID, Virtual_Truck_Number)
                            VALUES ({0},'{1}')
                    """.format(val["pre_load_id"], temp)
                    try:
                        cursor = cnxn.cursor()
                        cursor.execute(sql_query)
                        cnxn.commit()  
                    except Exception as e:
                        cnxn.rollback()
                        print(e.message)
                        return jsonify(status=500, message="Server Error while inserting Mapping Data!")     
        except Exception as e:
            print(e.message)
            cnxn.rollback()
            return jsonify(status=500, message="Server Error while inserting Mapping Data!")
        return jsonify(status=200,message="Data Successfully Inserted!")


# api to return the last generated virtual Truck Number
# need to add suffix after discussion with Idris ji
@blueprint.route('/get_last_virtual_truck_number',methods=['GET','POST'])
def get_last_virtual_truck_number():
    try:
        cnxn = make_database_connection()
        cursor = cnxn.cursor()
        sql_query = """
                        select Virtual_Truck_Number from QN_Tbl_Virtual_Truck_Planning
                    """
        cursor.execute(sql_query)
        # First case if there is no V.T.No in database
        # Creating First V.T.No
        if len(cursor.fetchall()) == 0:
            # print(first_virtual_truck_number)
            from datetime import datetime
            currentDay = datetime.now().day
            currentMonth = datetime.now().month
            currentYear = datetime.now().year
            first_virtual_truck_number = "VT" + str(currentDay) + str(currentMonth) + str(currentYear)[0:]
            first_virtual_truck_number = first_virtual_truck_number + "0000"
            # print(currentDay, currentMonth, currentYear)
            print(first_virtual_truck_number)

            return jsonify(status=200,last_virtual_truck_number=first_virtual_truck_number)
        else:
            sql_query = """
                select MAX(Virtual_Truck_Number) as LAST_TRUCK_NUMBER from QN_Tbl_Virtual_Truck_Planning 
                        """

            cursor.execute(sql_query)
            columns = [column[0] for column in cursor.description]
            results = []
            order_numbers = []
            last_virtual_truck_number=cursor.fetchone()[0]
            last_date = last_virtual_truck_number[2:4]
            from datetime import datetime
            currentDay = datetime.now().day
            currentMonth = datetime.now().month
            currentYear = datetime.now().year
            if str(currentDay) == str(last_date):
                return jsonify(status=200, last_virtual_truck_number = last_virtual_truck_number)
            else:
                first_virtual_truck_number = "VT" + str(currentDay) + str(currentMonth) + str(currentYear)[0:]
                first_virtual_truck_number = first_virtual_truck_number + "0000"
                print(first_virtual_truck_number)
                return jsonify(status=200, last_virtual_truck_number=first_virtual_truck_number)
    except Exception as e:
        print(e)
        return jsonify(status=500,message="Internal Server Error")