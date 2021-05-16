import datetime
from django.test import TestCase
from django.utils import timezone
from matmgmt.forms import CreateMaterialMasterForm, AddStockForm, MakeReservationForm, IssueReservationForm, AddLocationForm, SignupForm
from matmgmt.models import BelPartNumber, PartMaster, Inventory, Reservation, StoreLocation, StockIssue
from django.contrib.auth.models import User


class TestCreateMaterialMasterForm(TestCase):
    def test_bel_part_number_field(self):
        form = CreateMaterialMasterForm()
        self.assertTrue(form.fields['BEL_PART_NUMBER'].label is None or form.fields['BEL_PART_NUMBER'].label == 'bel part number')
        self.assertEqual(form.fields['BEL_PART_NUMBER'].help_text, 'Enter 12 digit bel part number. If unknown use 999999999999')

    def test_form_field_validations(self):
        form = CreateMaterialMasterForm( data = { "BEL_PART_NUMBER" :'123456789212', "MPN" :'lmz12003', "description" :'3A power regulator'})
        self.assertTrue(form.is_valid())

        #Testing for invalid bel part number
        form = CreateMaterialMasterForm( data = { "BEL_PART_NUMBER" :'invalid_partnumber', "MPN" :'lmz12003', "description" :'3A power regulator'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["BEL_PART_NUMBER"][0], 'Only enter 12 digit part Number')



        #Testing for invalid bel part number with less than 12 digits
        form = CreateMaterialMasterForm( data = { "BEL_PART_NUMBER" :'123', "MPN" :'lmz12003', "description" :'3A power regulator'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["BEL_PART_NUMBER"][0], 'BEL PART NUMBER must be 12 digits')
        
        #Testing for invalid 13 digit bel part number
        form = CreateMaterialMasterForm( data = { "BEL_PART_NUMBER" :'1234123412345', "MPN" :'lmz12003', "description" :'3A power regulator'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["BEL_PART_NUMBER"][0], 'BEL PART NUMBER must be 12 digits')

        #Testing for invalid 11 digit bel part number
        form = CreateMaterialMasterForm( data = { "BEL_PART_NUMBER" :'12341234123', "MPN" :'lmz12003', "description" :'3A power regulator'})
        self.assertFalse(form.is_valid())        
        self.assertEqual(form.errors["BEL_PART_NUMBER"][0], 'BEL PART NUMBER must be 12 digits')

        #Testing with a blank mpn
        form = CreateMaterialMasterForm( data = { "BEL_PART_NUMBER" :'123412341234', "MPN" :'', "description" :'3A power regulator'})
        self.assertFalse(form.is_valid())         

        #Testing with a blank description
        form = CreateMaterialMasterForm( data = { "BEL_PART_NUMBER" :'123412341234', "MPN" :'LMZ12003', "description" :''})
        self.assertFalse(form.is_valid())         

class TestAddStockForm(TestCase):
    def test_form_field_labels_help_text(self):
        form = AddStockForm()
        self.assertTrue(form.fields['Quantity'].label is None or form.fields['Quantity'].label == 'quantity')
        self.assertEqual(form.fields['Quantity'].help_text, 'Enter the qty')

        self.assertTrue(form.fields['Primary_Location'].label is None or form.fields['Primary_Location'].label == 'primary location')
        self.assertEqual(form.fields['Primary_Location'].help_text, 'Enter the Primary location')

        self.assertTrue(form.fields['Secondary_Location'].label is None or form.fields['Secondary_Location'].label == 'secondary location')
        self.assertEqual(form.fields['Secondary_Location'].help_text, 'Enter slot/pack Number')

        self.assertTrue(form.fields['Comment'].label is None or form.fields['Comment'].label == 'comment')
        self.assertEqual(form.fields['Comment'].help_text, 'Add an optional comment here for reference')

        self.assertTrue(form.fields['free_stock'].label is None or form.fields['free_stock'].label == 'free stock')
        self.assertEqual(form.fields['free_stock'].help_text, 'Check-To make it free stock. Uncheck- For Project Stock')

    def test_AddStockForm_field_validations(self):
        #setup a non modifiable Object to use while testing
        user_ins = User(username='217426', password = 'Bhanu#1149', email='bhanuseshuk@bel.co.in')
        user_ins.save()
        store_location_ins = StoreLocation(user = user_ins, primary_loc='CUP_BOARD1')
        store_location_ins.save()    
        store_location_ins = StoreLocation(user = user_ins, primary_loc='CUP_BOARD2')
        store_location_ins.save()          
        #valid form field verification
        form = AddStockForm( data = {
                                     "Quantity" :1, 
                                     "Primary_Location" : 2, 
                                     "Secondary_Location" :'3A power regulator',
                                     "Comment" : 'TEST COMMENT',
                                     "free_stock" : False})
        self.assertTrue(form.is_valid())

        #invalid zero quantity  form field verification
        form = AddStockForm( data = {
                                     "Quantity" :'0', 
                                     "Primary_Location" : 2, 
                                     "Secondary_Location" :'3A power regulator',
                                     "Comment" : 'TEST COMMENT',
                                     "free_stock" : False})
        form.is_valid()
        self.assertEqual(form.errors['Quantity'][0], 'Enter positive non zero value')

        #invalid negative quantity  form field verification
        form = AddStockForm( data = {
                                     "Quantity" :-1, 
                                     "Primary_Location" : 2, 
                                     "Secondary_Location" :'3A power regulator',
                                     "Comment" : 'TEST COMMENT',
                                     "free_stock" : False})
        form.is_valid()
        self.assertEqual(form.errors['Quantity'][0], 'Enter positive non zero value')        

        #secondary location field required true verification
        form = AddStockForm( data = {
                                     "Quantity" :1, 
                                     "Primary_Location" : 2, 
                                     "Secondary_Location" :'',
                                     "Comment" : 'TEST COMMENT',
                                     "free_stock" : False})
        self.assertFalse(form.is_valid())

        #comment field required true verification
        form = AddStockForm( data = {
                                     "Quantity" :1, 
                                     "Primary_Location" : 2, 
                                     "Secondary_Location" :'slot2',
                                     "Comment" : '',
                                     "free_stock" : False})
        self.assertFalse(form.is_valid())

class TestMakeReservationForm(TestCase):
    def test_form_field_labels_help_text(self):
        form = MakeReservationForm()
        self.assertTrue(form.fields['quantity'].label is None or form.fields['quantity'].label == 'quantity')
        self.assertEqual(form.fields['quantity'].help_text, 'Enter the qty')    

        self.assertTrue(form.fields['comment'].label is None or form.fields['comment'].label == 'comment')
        self.assertEqual(form.fields['comment'].help_text, 'Add an optional comment here for reference')
    
    def test_form_field_validations(self):
        form = MakeReservationForm(data = {
                                     "quantity" :1, 
                                     "comment" : 'test_comment for reservation'})
        self.assertTrue(form.is_valid())
        #invalid negative quantity
        form = MakeReservationForm(data = {
                                     "quantity" :-1, 
                                     "comment" : 'test_comment for reservation'})
        self.assertFalse(form.is_valid())        

        #invalid zero quantity
        form = MakeReservationForm(data = {
                                     "quantity" :0, 
                                     "comment" : 'test_comment for reservation'})
        self.assertFalse(form.is_valid())           
        #checking invlid blank comment
        form = MakeReservationForm(data = {
                                     "quantity" :1, 
                                     "comment" : ''})
        self.assertFalse(form.is_valid())   

class TestIssueReservationForm(TestCase):
     def test_form_field_labels_help_text(self):
        form = IssueReservationForm()

        self.assertTrue(form.fields['comment'].label is None or form.fields['comment'].label == 'comment')
        self.assertEqual(form.fields['comment'].help_text, 'Add an optional comment here for reference')   

     def test_form_field_validations(self):
        form = IssueReservationForm(data = {
                                     "comment" : 'test_comment for reservation'})
        self.assertTrue(form.is_valid())

        #checking invlid blank comment
        form = IssueReservationForm(data = {
                                     "comment" : ''})
        self.assertFalse(form.is_valid())        

class TestAddLocationForm(TestCase):
     def test_form_field_labels_help_text(self):
        form = AddLocationForm()

        self.assertTrue(form.fields['primary_loc'].label is None or form.fields['primary_loc'].label == 'primary loc')
        self.assertEqual(form.fields['primary_loc'].help_text, 'Enter cupboard or drawer number')   
        #checking valid  location
     def test_form_field_validations(self):
        form = AddLocationForm(data = {
                                     "primary_loc" : 'CUP_BOARD1'})
        self.assertTrue(form.is_valid())

        #checking invlid blank location
        form = AddLocationForm(data = {
                                     "primary_loc" : ''})
        self.assertFalse(form.is_valid())          

class TestSignupForm(TestCase):
     def test_form_field_labels_help_text(self):
        form = SignupForm()

        self.assertTrue(form.fields['username'].label is None or form.fields['username'].label == 'username')
        self.assertEqual(form.fields['username'].help_text, 'Enter the Staff Number')      

        self.assertTrue(form.fields['password'].label is None or form.fields['password'].label == 'username')
        self.assertEqual(form.fields['password'].help_text, 'Enter Password')  
        self.assertEqual(form.fields['password'].max_length, 30)  

        self.assertTrue(form.fields['confirm_password'].label is None or form.fields['confirm_password'].label == 'confirm password')
        self.assertEqual(form.fields['confirm_password'].help_text, 'Confirm Password')  
        self.assertEqual(form.fields['confirm_password'].max_length, 30) 

        self.assertTrue(form.fields['email'].label is None or form.fields['email'].label == 'email')
        self.assertEqual(form.fields['email'].help_text, 'Enter intranet(bel.net) email Id')  

        self.assertTrue(form.fields['first_name'].label is None or form.fields['first_name'].label == 'first name')
        self.assertEqual(form.fields['first_name'].help_text, 'Enter your First Name') 
        self.assertEqual(form.fields['first_name'].max_length, 30) 

        self.assertTrue(form.fields['last_name'].label is None or form.fields['last_name'].label == 'last name')
        self.assertEqual(form.fields['last_name'].help_text, 'Enter your Last Name')         
        self.assertEqual(form.fields['last_name'].max_length, 30) 
        #checking valid  location
     def test_form_field_validations(self):
         #checking valid form
        form = SignupForm(data = {
                                     "username" : '217426',
                                     'password': 'Bhanu#1149',
                                     'confirm_password' :'Bhanu#1149' ,
                                     "email" : 'bhanuseshuk@bel.net',
                                     "first_name" :'bhanu' ,
                                     "last_name" : 'valluri'})
        self.assertTrue(form.is_valid())        

         #checking invalid shortpassword field
        form = SignupForm(data = {
                                     "username" : '217426',
                                     'password': 'Bhanu#1',
                                     'confirm_password' :'Bhanu#1149' ,
                                     "email" : 'bhanuseshuk@bel.net',
                                     "first_name" :'bhanu' ,
                                     "last_name" : 'valluri'})
        self.assertFalse(form.is_valid())         
        self.assertEqual(form.errors['password'][0], 'Must have minimum length of 8')   

         #check for at least one digit in password
        form = SignupForm(data = {
                                     "username" : '217426',
                                     'password': 'Bhanu#onetwo',
                                     'confirm_password' :'Bhanu#onetwo' ,
                                     "email" : 'bhanuseshuk@bel.net',
                                     "first_name" :'bhanu' ,
                                     "last_name" : 'valluri'})
        self.assertFalse(form.is_valid())         
        self.assertEqual(form.errors['password'][0], 'Must contain at least one digit')

         #check for atleast on capital letter
        form = SignupForm(data = {
                                     "username" : '217426',
                                     'password': 'bhanu#1143',
                                     'confirm_password' :'bhanu#1143' ,
                                     "email" : 'bhanuseshuk@bel.net',
                                     "first_name" :'bhanu' ,
                                     "last_name" : 'valluri'})
        self.assertFalse(form.is_valid())         
        self.assertEqual(form.errors['password'][0], 'Must have atleast one capital letter')           

         #check for atleast on special character
        form = SignupForm(data = {
                                     "username" : '217426',
                                     'password': 'bhanuD1143',
                                     'confirm_password' :'bhanuD1143' ,
                                     "email" : 'bhanuseshuk@bel.net',
                                     "first_name" :'bhanu' ,
                                     "last_name" : 'valluri'})
        self.assertFalse(form.is_valid())         
        self.assertEqual(form.errors['password'][0], 'Must contain any one of special chars @ # $ % ^ & + =')         
         #checking invalid email id
        form = SignupForm(data = {
                                     "username" : '217426',
                                     'password': 'Bhanu#1149',
                                     'confirm_password' :'Bhanu#1149' ,
                                     "email" : 'bhanuseshuk@bl.net',
                                     "first_name" :'bhanu' ,
                                     "last_name" : 'valluri'})
        self.assertFalse(form.is_valid())   
        self.assertEqual(form.errors['email'][0], 'Not a valid bel.net email address')         
