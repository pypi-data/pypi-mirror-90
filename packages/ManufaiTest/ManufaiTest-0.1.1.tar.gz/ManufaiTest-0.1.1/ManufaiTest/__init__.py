

import sys
import tkinter, sys, json
from tkinter import messagebox
from random import randint
from pathlib import Path
import pickle
import os
import subprocess, platform
import string
import re

class Calculator:
    def add_numbers(num1, num2):
    	return num1 + num2

    def subtract_numbers(num1, num2):
        return num1 - num2

    def multiply_numbers(num1, num2):
        return num1 * num2

    def divide_numbers(num1, num2):
        return num1 / num2


class GenerateCode:
    def construct_user_code(user_name, user_lastname):

        var_name = str(user_name)
        var_lastname = str(user_lastname)
        var_code = ""

        if not var_name or not var_lastname:
            var_code = "Debes introducir Nombre y Apellido"
        else:
            random = randint(10000,99999)
            var_code = str(var_name[0] + var_lastname[0] + str(random))
            print("Tu codigo es: " + var_code)
        return var_code

    def save_user_code(user_name, user_lastname, user_code, path_view):
        #Convert Parameters as Strings
        var_name = str(user_name)
        var_lastname = str(user_lastname)
        var_code = str(user_code)
        path = str(path_view)

        message = ""

        filename = "Users.txt"
        my_file = Path(path + filename)

        if not var_name or not var_lastname or not var_code:
            message = "Debes introducir Nombre y Apellido"
            return message
        else:
            try:
                my_abs_path = my_file.resolve(strict=True)
            except FileNotFoundError:  # doesn't exist
                file = open("Users.txt", "a") 
                file.write(var_name + " " + var_lastname + " " + var_code + "\n") 
                file.close()
                message = "Usuario guardado con exito"
                return message 
            else:  # exists
                file = open("Users.txt", "w") 
                file.write(var_name + " " + var_lastname + " " + var_code + "\n") 
                file.close() 
                message = "Usuario guardado con exito"
                return message 


    def view_all_users(path_view):
        path = str(path_view)
        filename = "Users.txt"
        my_file = Path(path + '/' + filename)

        try:
            my_abs_path = my_file.resolve(strict=True)
        except FileNotFoundError:  # doesn't exist
            file_users = "No hay usuarios registrados"
            return file_users 
        else:  # exists
            file = open(my_file, "r")
            print([line.rstrip() for line in open(my_file)])
            file_users = file.readlines()
            file.close()
            return file_users 


class DongleConection:

    def ping(host):
        #Returns True if host responds to a ping request  
        try:
            output = subprocess.check_output("ping -{} 1 {}".format('n' if platform.system().lower()=="windows" else 'c', host), shell=True)
            return True
    
        except Exception:
            return False
    
    
    #print(ping("192.168.0.36"))
    def ValidateRequest():
        i = 1
        while True:
            i = i + 1
            import time
            timeout = time.time() + 1   # 5 minutes from now
            while True:
                test = 0
                if test == 5 or time.time() > timeout:
                    #print(ping("google.com"))
                    if ping("www.google.com") == False:
                        print("Error de conexion en la Red")
                    else:
                        print("Conexion de Red Exitosa")
                    break
                test = test - 1
            if(i > 3):
                break
            
    def ValidateDongleConection(STATUS_NUMBER):
        if(STATUS_NUMBER == 401):
            #print("Problema de conexion con Dongle")
            return "No se ha detectado Dongle"
    
        else:
            return "Conexion con Dongle exitosa"
            
    def ShowExecutionNumber(EXECUTION_NUMBER):
        total_executions = str(EXECUTION_NUMBER)
        return "Tienes: " + total_executions + " Ejecuciones restantes"
    
    
    