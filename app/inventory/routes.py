from email import message
from app.inventory import blueprint
from flask_restful import Resource, Api
from flask import jsonify, render_template, redirect, request, url_for
import json
import datetime


from flask_mail import Message
from app.helpers.connection import make_database_connection

# function to return the data for screen1 
# need to add check if newly added line item number already exist.

@blueprint.route('/inventory_data',methods=['GET','POST'])
def inventory_data():
    try:
        data = data = request.args
        material_code = data["material_code"]
        # database connection
        cnxn = make_database_connection()
        cursor = cnxn.cursor()
        default_query = """
                            select i.Cast_Number,
                            i.Stack_Number,
                            i.Coil_No,
                            i.Diameter,
                            i.Grade,
                            i.UTS,
                            i.Elongation
                            from QN_Tbl_Inventory as i
                            where Material_Code = '{0}'
                        """.format(material_code)
        print(default_query)
        cursor.execute(default_query)
        columns = [column[0] for column in cursor.description]
        results = []
        main_results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        print(results)
        for temp in results:
            temp_obj  = {}
            temp_obj['cast_number'] = temp['Cast_Number']
            temp_obj['stack_number'] = temp['Stack_Number']
            temp_obj['coil_number'] = temp['Coil_No']
            temp_obj['diameter'] = temp['Diameter']
            temp_obj['grade'] = temp['Grade']
            temp_obj['uts'] = temp['UTS']
            temp_obj['elongation'] = temp['Elongation']
            main_results.append(temp_obj)
        return jsonify(status=200,data=main_results,message="It worked!")
    except Exception as e:
        # print(e.message)
        print(e)
        return jsonify(status=500,message="Internal server error!")
    # return jsonify(status=200,message="It worked!")




