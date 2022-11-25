# -*- encoding: utf-8 -*-
"""
Copyright (c) 2021
"""
from crypt import methods
from datetime import date, datetime
from email import message
from app.master import blueprint
from decouple import config
import json, requests
from flask_cors import CORS, cross_origin
from flask import jsonify, render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response
# import pdfkit
import os

# NALCO APIS

def make_database_connection():
    import pyodbc
    cnxn = pyodbc.connect(driver='{FreeTDS}', host='115.124.119.236', database='NALCO_DISPATCH',
                        trusted_connection='no', user='Aipalatte2', password='guest2@Nalco2022',
                        TrustServerCertificate='yes')
    return cnxn


# api to return the customer codes for dropdown.

@blueprint.route('/get_customer_codes', methods=["GET","POST"])
def get_customer_codes():
    try:
        sql_query = """
                        select Customer_Code from QN_Tbl_Customer_Master
                    """
        cnxn = make_database_connection()
        cursor = cnxn.cursor()
        cursor.execute(sql_query)
        columns = [column[0] for column in cursor.description]
        results = []
        customer_codes = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        for temp in results:   
            customer_codes.append(temp["Customer_Code"])    
        return jsonify(status=200,data=customer_codes)
    except Exception as e:
        print(e)
        return jsonify(status=500,message="Internal Server Error")


# api to return the transporter codes for dropdown.
@blueprint.route('/get_transporter_codes', methods=["GET","POST"])
@cross_origin()
def get_transporter_codes():
    try:
        sql_query = """
                        select Transporter_Code from QN_Tbl_Transporter_Master
                    """
        cnxn = make_database_connection()
        cursor = cnxn.cursor()
        cursor.execute(sql_query)
        columns = [column[0] for column in cursor.description]
        results = []
        transporter_codes = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        for temp in results:   
            transporter_codes.append(temp["Transporter_Code"])    
        return jsonify(status=200,data=transporter_codes)
    except Exception as e:
        return jsonify(status=500,message="Internal Server Error")

# api to get order numbers for dropdown

@blueprint.route('/get_order_numbers', methods=["GET","POST"])
@cross_origin()
def get_order_numbers():
    try:
        sql_query = """
                        select Sales_Order_Number from QN_Tbl_Sales_Order_HDR
                    """
        cnxn = make_database_connection()
        cursor = cnxn.cursor()
        cursor.execute(sql_query)
        columns = [column[0] for column in cursor.description]
        results = []
        order_numbers = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        for temp in results:   
            order_numbers.append(temp["Sales_Order_Number"])    
        return jsonify(status=200,data=order_numbers)
    except Exception as e:
        print(e)
        result = jsonify(status=500,message="Internal Server Error")
        return result.headers.add('Access-Control-Allow-Origin', '*')






