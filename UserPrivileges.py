import datetime
import hashlib
import base64
import json

#this function is used to sign up a user and assign user roles and privileges

def signup() :
    print("Sign up")
    name = input("Enter your name: ")
    password = input('Enter a password including an upper-case letter, lower-case letter, a digit and length not less than 6: \n')

    while True:
            if not (any(x.isupper() for x in password) and any(x.islower() for x in password) and any(x.isdigit() for x in password) and len(password) >= 6):
                password = input("Password is too weak. Please re-enter: ")
            else:
                break

    hashed_password = hash_password(password)

    with open ("config.json", "r") as user_data:
        data = json.load(user_data)
        doctor_code = data['sec_codes'].get('doctor')
        staff_code = data['sec_codes'].get('staff')

        # for added security of preventing anyone from creating accounts with user roles
        # a code is added that will be known only by that particular user role.
        while True:
            role_number = input('Enter 1 for "doctor account" and 2 for "staff account: ')
            
            if role_number == "1":
                security_code = hash_password(input("Enter the security code given: "))
                if security_code == doctor_code:
                    user_type = "doctor"
                    privilege_level = "2"
                    break
                else:
                    print("Wrong security code. Please re-enter")
            
            elif role_number == "2":
                security_code = hash_password(input("Enter the security code given: "))
                if security_code == staff_code:
                    user_type = "staff"
                    privilege_level = "3"
                    break
                    break
                else:
                    print("Wrong security code. Please re-enter: ")   

            else:
                print("Invalid input. Please re-enter: ")
            
        
        
        # adding user data to thee config.json file
        user_id = len(data['users']) + 1
        data['users'].append({"id": user_id,
                              "name": name,
                              "password": hashed_password,
                              "user_type": user_type,
                              "privilege_level": privilege_level
                            })

        with open("config.json", "w") as user_data_out:
            json.dump(data, user_data_out)
            user_data.close()

        print("Account created successfully")

        # Collecting personal data of the user
        print("Please enter your personal data")

        name = input('Your Name: ')
        age = input('Age: ')
        nic_number = input('NIC Number: ')
        tel_number = input('Telephone Number: ')

        # write account details to data file
        with open("data.json", 'r') as json_data_file:
            data = json.load(json_data_file)
            data['personal_details'].append({
                'id': user_id,
                'name': name,
                'age': age,
                'nic_number': encode(nic_number),
                'tel_number': encode(tel_number)
            })
        with open("data.json", 'w') as outfile:
            json.dump(data, outfile)

        print("Account completed")



#this function is used to login a user based on the password and username

def login() :
    name = input("Enter username: ")
    hashed_password = hash_password(input("Enter password: "))
    result = "Login failed"
    with open("config.json", 'r') as user_data_file:
        data = json.load(user_data_file)
        for user in data['users']:
            if name == user['name'] and hashed_password == user['password']:
                current_user = user
                result = "Login successful"
        print(result)
    if result == "Login successful":
        return current_user
    else:
        return False 


#this function is used to hash the password

def hash_password(password) :
    hashed_password = hashlib.md5()
    hashed_password.update(password.encode("utf-8"))
    return hashed_password.hexdigest()

#this function is used to encode and decode the data

def encode(data) :
    encoded_bytes = base64.b64encode(data.encode("ascii"))
    encoded_string = encoded_bytes.decode("ascii")
    return encoded_string

def decode(data) :
    string_bytes = base64.b64decode(data.encode("ascii"))
    string_data = string_bytes.decode("ascii")
    return string_data


#############################################
###########  Common functions ###############
#############################################

def check_patient_id(patient_id):
    with open("data.json", 'r') as data_file:
        user_data = json.load(data_file)
        for patient in user_data['personal_details']:
            if patient_id == patient['id']:
                return True
        return False

def edit_account(user_id):

    with open("data.json", 'r') as data_file:
        data = json.load(data_file)
        for user in data['personal_details']:
            if user_id == user['id']:
                print("Enter new details. Enter old details to keep them unchanged")
                user['name'] = input("Name: ")
                user['age'] = input("Age: ")
                user['nic_number'] = encode(input("NIC number: "))
                user['tel_number'] = encode(input("Telephone number: "))
                break
        with open("data.json", 'w') as outfile:
            json.dump(data, outfile)

        print("Account edited successfully")



def renew_password(user_id):

    new_pwd = input('Enter a password including an upper-case letter, lower-case letter, a digit and length not less than 6: \n')
    while True:
        if not (any(x.isupper() for x in new_pwd) and any(x.islower() for x in new_pwd) and any(x.isdigit() for x in new_pwd) and len(new_pwd) >= 6):
            new_pwd = input("Password is too weak. Please re-enter: ")
        else:
            break
    new_password = hash_password(new_pwd)

    with open("config.json", 'r') as user_data_file:
        data = json.load(user_data_file)
        for user in data['users']:
            if user_id == user['id']:
                user['password'] = new_password
                break    

        with open("config.json", 'w') as data_outfile:
            json.dump(data, data_outfile)

    print("Password renewed successfully")





def view_account(user_id):

    with open("data.json", 'r') as data_file:
        data = json.load(data_file)
        for user in data['personal_details']:
            if user_id == user['id']:
                print("Name: ", user['name'])
                print("Age: ", user['age'])
                print("NIC number: ", decode(user['nic_number']))
                print("Telephone number: ", decode(user['tel_number']))
                break






#############################################
######## Admin Related functions ############
#############################################

#this function is used to set the security codes for the doctor and staff

def admin_options():
        
        print("Press 1 to create admin account\nPress 2 to edit doctor's security code\nPress 3 to edit staff's code\nPress -1 to exit\n")
        doctor, staff = '', ''

        while True:
            opt_number = input()
            if opt_number == '1':
                create_admin()
                print("Enter -1 to exit. Otherwise Enter the next option number: ")
                
            elif opt_number == '2':
                doctor_security_code = hash_password(input("Enter new doctor's security code: "))
                print("Enter -1 to exit. Otherwise Enter the next option number: ")

            elif opt_number == '3':
                staff_security_code = hash_password(input("Enter new staff's security code: "))
                print("Enter -1 to exit. Otherwise Enter the next option number: ")
            elif opt_number == '-1':
                print("Thank you admin")
                break
            else:
                print("Invalid input")

        with open("config.json", 'r') as user_data_file:
            data = json.load(user_data_file)
            doctor = data['sec_codes'].get('doctor')
            staff = data['sec_codes'].get('staff')
            if doctor:
                doctor = doctor_security_code
            if staff:
                 staff = staff_security_code
            data['sec_codes'] = {
                'doctor': doctor_security_code,
                'receptionist': staff_security_code,
            }

        with open("config.json", 'w') as data_outfile:
            json.dump(data, data_outfile)

    
def create_admin():
    name = input('Admin Username: ')
    temp_password = hash_password(input('Temporary password: '))

    # read and write user to config file
    with open("config.json", 'r') as json_data_file:
        data = json.load(json_data_file)
        admin_id = len(data['users'])+1
        data['users'].append({
            'id': admin_id,
            'name': name,
            'password': temp_password,
            'user_type': "admin",
            'privilege_level': '1'
        })
    with open("config.json", 'w') as outfile:
        json.dump(data, outfile)

    print("Account created successfully")
    print("Please enter personal details of admin")

    admin_name = input('Admin name: ')
    age = input('Age: ')
    nic_no = input('NIC number: ')
    tel = input('Telephone number: ')

    # read and write admin details to data file
    with open("data.json", 'r') as data_file:
        data = json.load(data_file)
        data['personal_details'].append({
            'id': admin_id,
            'name': admin_name,
            'age': age,
            'nic_number': encode(nic_no),
            'tel_number': encode(tel)
        })
    with open("data.json", 'w') as outfile:
        json.dump(data, outfile)



#############################################
######## Doctor Related functions ###########
#############################################

def doctor_options(curr_user_id):
    print("Press 1 to add sickness details \nPress 2 to add drug prescription \nPress 3 to add lab test prescription \nPress 4 to view sickness details \nPress 5 to view previous drug prescriptions \nPress 6 to view lab test prescription \nPress 7 to edit account \nPress 8 to renew password \nPress 9 to view account\nPress -1 to exit\n ")

    while True:
        opt_number = input()
        if opt_number in ['1', '2', '3', '4', '5', '6']:

            while True:
                patient_id = input("Enter patient id: ")
                if check_patient_id(patient_id):
                    break
                else:
                    print("Invalid patient id")

            if opt_number == '1':
                add_sickness_details(patient_id)
                print("Enter next option number: ")
            elif opt_number == '2':
                add_drug_presc(patient_id)
                print("Enter next option number: ")
            elif opt_number == '3':
                add_lab_presc(patient_id)
                print("Enter next option number: ")
            elif opt_number == '4':
                read_medical_details(patient_id)
                print("Enter next option number: ")
            elif opt_number == '5':
                read_drug_presc(patient_id)
                print("Enter next option number: ")
            elif opt_number == '6':
                read_lab_presc(patient_id)
                print("Enter next option number: ")
        elif opt_number == '7':
            edit_account(curr_user_id)
            print("Enter next option number: ")
        elif opt_number == '8':
            renew_password(curr_user_id)
            print("Enter next option number: ")
        elif opt_number == '9':
            view_account(curr_user_id)
            print("Enter next option number: ")
        elif opt_number == '-1':
            print("Thank you doctor")
            break
        else:
            print("Invalid input. Try again")



def add_sickness_details(patient_id):

    sickness = input("Enter sickness details: ")

    with open("data.json", 'r') as data_file:
        data = json.load(data_file)
        data['medical_details'].append({
            'id': patient_id,
            'sickness': sickness,
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    with open("data.json", 'w') as outfile:
        json.dump(data, outfile)

    print("Medical record added successfully")



def add_drug_presc(patient_id):

    drug_details = input("Enter drug prescription details: ")

    with open("data.json", 'r') as data_file:
        data = json.load(data_file)
        data['drug_presc'].append({
            'id': patient_id,
            'drug_details': drug_details,
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    with open("data.json", 'w') as outfile:
        json.dump(data, outfile)

    print("Drug prescription added successfully")




def add_lab_presc(patient_id):

    lab_presc = input("Enter lab test prescription details: ")

    with open("data.json", 'r') as data_file:
        data = json.load(data_file)
        data['lab_presc'].append({
            'id': patient_id,
            'lab_presc': lab_presc,
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    with open("data.json", 'w') as outfile:
        json.dump(data, outfile)

    print("Lab test prescription added successfully")



# these set of functions are shared between doctor and patir=ent as well. Upon login permissions are checked.

def read_medical_details(patient_id):

    with open("data.json", 'r') as data_file:
        data = json.load(data_file)
        for medical_record in data['medical_details']:
            if str(patient_id) == medical_record['id']:
                print("Patient id: ", medical_record['id'])
                print("Sickness details: ", medical_record['sickness'])
                print("Date: ", medical_record['date'])
                print("\n")



def read_drug_presc(patient_id):

    with open("data.json", 'r') as data_file:
        data = json.load(data_file)
        for drug_presc in data['drug_presc']:
            if str(patient_id) == drug_presc['id']:
                print("Patient id: ", drug_presc['id'])
                print("Drug prescription details: ", drug_presc['drug_details'])
                print("Date: ", drug_presc['date'])
                print("\n")



def read_lab_presc(patient_id):

    with open("data.json", 'r') as data_file:
        data = json.load(data_file)
        for lab_presc in data['lab_presc']:
            if str(patient_id) == lab_presc['id']:
                print("Patient id: ", lab_presc['id'])
                print("Lab test prescription details: ", lab_presc['lab_presc'])
                print("Date: ", lab_presc['date'])
                print("\n")





#############################################
######## Staff Related functions ############
#############################################

def staff_options(curr_user_id):

    print("Press 1 to add patient details \nPress 2 to edit account \nPress 3 to renew password \nPress 4 to view account\nPress -1 to exit\n ")

    while True:
        opt_number = input()
        
        if opt_number == '1':
            add_patient_details()
            print("Enter next option number: ")    
        elif opt_number == '2':
            edit_account(curr_user_id)
            print("Enter next option number: ")
        elif opt_number == '3':
            renew_password(curr_user_id)
            print("Enter next option number: ")
        elif opt_number == '4':
            view_account(curr_user_id)
            print("Enter next option number: ")
        elif opt_number == '-1':
            print("Thank you staff")
            break
        else:
            print("Invalid input. Try again")


def add_patient_details():

    name = input('Patient username: ')
    #this will be set temporarily by staff unitl user changes it later after creation of account
    temp_password = hash_password(input('Password: '))

    # write patient details to config file
    with open("config.json", 'r') as data_file:
        data = json.load(data_file)
        patient_id = len(data['users'])+1
        data['users'].append({
            'id': patient_id,
            'name': name,
            'password': temp_password,
            'user_type': "patient",
            'privilege_level': '4'
        })
    with open("config.json", 'w') as outfile:
        json.dump(data, outfile)

    print("Account created successfully")
    print("Please enter personal details of patient")

    patient_name = input('Patient name: ')
    age = input('Age: ')
    nic_number = input('NIC number: ')
    tel_number = input('Telephone number: ')

    # read and write patient details to data file
    with open("data.json", 'r') as json_data_file:
        data = json.load(json_data_file)
        data['personal_details'].append({
            'id': patient_id,
            'name': patient_name,
            'age': age,
            'nic_number': encode(nic_number),
            'tel_number': encode(tel_number)
        })
    with open("data.json", 'w') as outfile:
        json.dump(data, outfile)







#############################################
######## Patient Related functions ##########
#############################################


def patient_options(curr_user_id):

    print("Press 1 to view account\nPress 2 to edit account\nPress 3 to renew password\nPress 4 to view medical details\nPress 5 to view drug prescription\nPress 6 to view lab test prescription\nPress -1 to exit\n ")

    while True:
        opt_number = input()
        if opt_number == '1':
            view_account(curr_user_id)
            print("Enter next option number: ")
        elif opt_number == '2':
            edit_account(curr_user_id)
            print("Enter next option number: ")
        elif opt_number == '3':
            renew_password(curr_user_id)
            print("Enter next option number: ")
        elif opt_number == '4':
            read_medical_details(curr_user_id)
            print("Enter next option number: ")
        elif opt_number == '5':
            read_drug_presc(curr_user_id)
            print("Enter next option number: ")
        elif opt_number == '6':
            read_lab_presc(curr_user_id)
            print("Enter next option number: ")
        elif opt_number == '-1':
            print("Thank you patient")
            break
        else:
            print("Invalid input. Try again")    











def main() :

    n = input("Enter 1 to login and 2 to sign up: ")

    if n == "1" :
        curr_user = login()

    elif n == "2" :
        signup()
        print("Sign up successful. Please login")
        main()
        
    else :
        print("Invalid input")
        main()

    if curr_user:
        curr_user_id = curr_user.get('id')

        # user is admin
        if curr_user.get('privilege_level') == '1':
            print('Welcome admin')
            admin_options()

        
        # user is doctor
        elif curr_user.get('privilege_level') == '2':
            print('Welcome Doctor')
            doctor_options(curr_user_id)

        

        # user is from staff
        elif curr_user.get('privilege_level') == '3':
            print('Welcome Staff')
            staff_options(curr_user_id)

        # user is patient
        elif curr_user.get('privilege_level') == '4':
            print('Welcome')
            patient_options(curr_user_id)
 



main()
