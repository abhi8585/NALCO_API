from email import message
from app.modify import blueprint
from flask_restful import Resource, Api
from flask import jsonify, render_template, redirect, request, url_for
import json
import datetime


from flask_mail import Message
from app.helpers.connection import make_database_connection

# function to return the data for screen1 
# need to add check if newly added line item number already exist.

@blueprint.route('/modify_order',methods=['GET','POST'])
def modify_order():
    data = request.get_json(force=True)
    cnxn = make_database_connection()
    cursor = cnxn.cursor()
    #handle cases for newly added items
    try:
        newly_added_items = data["newly_added_items"]
        if len(newly_added_items) == 0:
            print("No new line item added")
            pass
        else:
            # print("Line Item added")
            for temp in newly_added_items:
                values = []
                try:
                    if temp["order_number"] == "" or temp["order_number"] == None:
                        return jsonify(status=400,message="Please provide order number")
                    else:
                        values.append(temp["order_number"])
                except Exception as e:
                    return jsonify(status=500,message="Error while reading order number")

                try:
                    if temp["line_item_number"] == "" or temp["line_item_number"] == None:
                        return jsonify(status=400,message="Please provide Line Item number")
                    else:
                        values.append(temp["line_item_number"])
                except Exception as e:
                    return jsonify(status=500,message="Error while reading Line Item number")

                try:
                    if temp["material_code"] == "" or temp["material_code"] == None:
                        return jsonify(status=400,message="Please provide Material code")
                    else:
                        values.append(temp["material_code"])
                except Exception as e:
                    print(e.message)
                    return jsonify(status=500,message="Error while reading Material Code")

                # try:
                #     if temp["material_description"] == "" or temp["material_description"] == None:
                #         return jsonify(status=400,message="Please provide Material description")
                #     else:
                #         values.append(temp["material_description"])
                # except Exception as e:
                #     return jsonify(status=500,message="Error while reading Material Description")

                try:
                    if temp["quantity"] == "" or temp["quantity"] == None:
                        return jsonify(status=400,message="Please provide Material quantity")
                    else:
                        values.append(temp["quantity"])
                except Exception as e:
                    return jsonify(status=500,message="Error while reading Material Description")

                try:
                    if temp["status"] == "" or temp["status"] == None:
                        return jsonify(status=400,message="Please provide Material Status")
                    else:
                        values.append(temp["status"])
                except Exception as e:
                    return jsonify(status=500,message="Error while reading Material Status")
                values = tuple(values)
                sql_query = """
                    INSERT INTO QN_Tbl_Sales_Order_Detail (Sales_Order_Number,Line_item_Number, Material_Code, Quantity, Status)
                    VALUES {0};
                """.format(values)
                print(sql_query)
                try:
                    cursor.execute(sql_query)
                    cnxn.commit()
                    print("Data successfully inserted!")
                except Exception as e:
                    print(e.message)
                    cnxn.rollback()
                    return jsonify(status=500, message="Server Error while inserting Data!")     
    except Exception as e:
        # print(e.message)
        return jsonify(status=500,message="Error while adding New Line items")

    # handle the case for recently deleted items

    try:
        removed_items = data["removed_items"]
        if len(removed_items) == 0:
            pass
        else:
            for temp in removed_items:
                values = []
                # print(temp["order_number"])
                # print(temp)
                try:
                    if temp["order_number"] == "" or temp["order_number"] == None:
                        return jsonify(status=400,message="Please provide order number")
                    else:
                        values.append(temp["order_number"])
                except Exception as e:
                    return jsonify(status=500,message="Error while reading order number")
                try:
                    if temp["line_item_number"] == "" or temp["line_item_number"] == None:
                        return jsonify(status=400,message="Please provide Line Item number")
                    else:
                        values.append(temp["line_item_number"])
                except Exception as e:
                    return jsonify(status=500,message="Error while reading Line Item number")
                sql_query = """
                    DELETE FROM QN_Tbl_Sales_Order_Detail WHERE Sales_Order_Number='{0}'
                     and Line_item_Number = '{1}';
                """.format(values[0],values[1])
                print(sql_query)
                try:
                    cursor.execute(sql_query)
                    cnxn.commit()
                    print("Data successfully inserted!")
                except Exception as e:
                    print(e.message)
                    cnxn.rollback()
                    return jsonify(status=500, message="Server Error while Removing Line Item Data!")  
    except Exception as e:
        return jsonify(status=500,message="Error while removing new items")

    # handle cases for modified items
    try:
        try:
            modified_items = data["modified_items"]
            if len(modified_items) == 0:
                pass
            else:
                for temp in modified_items:
                    temp_order_number = temp["order_number"]
                    temp_line_item_number = temp["line_item_number"]
                    # print(temp_line_item_number,temp_order_number)
                    for key, value in temp.items():
                        if isinstance(value, dict):
                            if key == "material_code":
                                column_name = "Material_Code"
                                temp_value = value["new_value"]
                            if key == "quantity":
                                column_name = "Quantity"
                                temp_value = int(value["new_value"])
                            sql_query = """ 
                                    UPDATE QN_Tbl_Sales_Order_Detail
                                    SET {0} = '{1}', Is_Modified = 1
                                    WHERE Sales_Order_Number='{2}' and Line_item_Number = '{3}';
                                        """.format(column_name, value["new_value"],temp_order_number,temp_line_item_number)
                            try:
                                cursor.execute(sql_query)
                                cnxn.commit()
                                print("Data successfully Updated!")
                            except Exception as e:
                                print(e.message)
                                cnxn.rollback()
                                return jsonify(status=500, message="Server Error while Modifying Line Item Data!")  
                print("Items modified successfully!")
        except Exception as e:
            pass
    except:
        return jsonify(status=500,message="Error while Modifying Line items")
    return jsonify(status=200,message="Order successfully Modified")



def material_description(data,cursor):
    # print(data["material_code"])
    if data["material_code"] == "" or data["material_code"] == None:
        return dict(status=400,message="Material code is NULL!")
    else:
        sql_query = """
                        select Description from QN_Tbl_Material_Master where Material_Code = '{0}'
                    """.format(data["material_code"])
        try:
            cursor.execute(sql_query)
            columns = [column[0] for column in cursor.description]
            # print(columns)
            results = []
            temp_data = cursor.fetchone()
            if temp_data == None:
                return dict(status=400,material_description="")
            else:
                # print(cursor.fetchone()[0])
                return dict(status=200,material_description=temp_data[0])
            # print(cursor.fetchone())
            # print(cursor.fetchall())
            # # print(len(cursor.fetchall()))
            # if len(cursor.fetchall()) == 0:
            #     return dict(status=400,message="Wrong Material Code")
            # for row in cursor.fetchall():
            #     # print(row[0])
            #     results.append(dict(zip(columns, row)))
            # print(results)
            return dict(status=200) 
        except Exception as e:
            print(e)
            # cnxn.rollback()
            return dict(status=500,message="Internal Server Error!") 


@blueprint.route('/get_material_description',methods=['GET','POST'])
def get_material_description():
    # data = request.get_json(force=True)
    material_code = request.args.get('material_code')
    # print(material_code)
    try:
        cnxn = make_database_connection()
        cursor = cnxn.cursor()
    except:
        return jsonify(status=500, message="Error while connecting to Database")
    try:
        data = dict(material_code=material_code)
        data = material_description(data,cursor)
        # print(data)
        return jsonify(data)
    except Exception as e:
        print(e)
        return jsonify(status=500,message="No Material code provided!")




