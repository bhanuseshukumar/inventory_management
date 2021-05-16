from django.test import TestCase
from matmgmt.forms import CreateMaterialMasterForm, AddStockForm, MakeReservationForm, IssueReservationForm, AddLocationForm, SignupForm
from matmgmt.models import BelPartNumber, PartMaster, Inventory, Reservation, StoreLocation, StockIssue
from django.contrib.auth.models import User


# Create your tests here.

class PartMasterModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #setup a non modifiable Object to use while testing
        bel_part_number_ins = BelPartNumber(belPartNo = '012345678912')
        bel_part_number_ins.save()
        part_master_ins = PartMaster(belPartNo = bel_part_number_ins, mpn = 'LMZ12003' , description = '3A power Regulator')
        part_master_ins.save()

    def setUp(self):
        pass

    #Testing the belPartNo label
    def test_belPartNo_label(self):
        partmaster_ins = PartMaster.objects.get(id=1)
        field_label = partmaster_ins._meta.get_field('belPartNo').verbose_name
        self.assertEqual(field_label, 'belPartNo')
    
        #Testing the belPartNo size & corresponding form field size
    def test_belPartNo_size(self):
        bel_part_no_ins = BelPartNumber.objects.get(id=1)
        bel_part_no_size = bel_part_no_ins._meta.get_field('belPartNo').max_length
        form = CreateMaterialMasterForm()
        field_size = form.fields['BEL_PART_NUMBER'].max_length

        self.assertEqual(12 ,bel_part_no_size)
        self.assertEqual(bel_part_no_size ,field_size)

        #Testing the mpn label
    def test_mpn_label(self):
        partmaster_ins = PartMaster.objects.get(id=1)
        field_label = partmaster_ins._meta.get_field('mpn').verbose_name
        self.assertEqual(field_label, 'mpn')

        #Testing the mpn size in the model aswell as in the form
    def test_mpn_size(self):
        partmaster_ins = PartMaster.objects.get(id=1)
        mpn_size = partmaster_ins._meta.get_field('mpn').max_length
        form = CreateMaterialMasterForm()
        form_field_size = form.fields['MPN'].max_length
        self.assertEqual(30, mpn_size)
        self.assertEqual(mpn_size, form_field_size)


        #Testing the description label
    def test_description_label(self):
        partmaster_ins = PartMaster.objects.get(id=1)
        field_label = partmaster_ins._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'description')

        #Testing the description size & corresponding form field size
    def test_description_size(self):
        partmaster_ins = PartMaster.objects.get(id=1)
        field_size = partmaster_ins._meta.get_field('description').max_length
        form = CreateMaterialMasterForm()
        form_field_size = form.fields['description'].max_length
        self.assertEqual(50, field_size)   
        self.assertEqual(field_size, form_field_size ) 


class InventoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #setup a non modifiable Object to use while testing
        bel_part_number_ins = BelPartNumber(belPartNo = '012345678912')
        bel_part_number_ins.save()
        part_master_ins = PartMaster(belPartNo = bel_part_number_ins, mpn = 'LMZ12003' , description = '3A power Regulator')
        part_master_ins.save()
        user_ins = User(username='217426', password = 'Bhanu#1149', email='bhanuseshuk@bel.co.in')
        user_ins.save()
        store_location_ins = StoreLocation(user = user_ins, primary_loc='CUP_BOARD1')
        store_location_ins.save()

        inventory_instance = Inventory( owner = user_ins, 
                                partMaster = part_master_ins,
                                qty = 100,
                                storeLoc = store_location_ins,
                                secondary_loc = 'packet1/slot1',
                                comment = 'test inventory ',
                                free_stock = False)      
        inventory_instance.save()                     

    def setUp(self):
        pass

    #Testing the owner field label
    def test_owner_label(self):
        inventory_ins = Inventory.objects.get(id=1)
        field_label = inventory_ins._meta.get_field('owner').verbose_name
        self.assertEqual('owner', field_label)
    
        #Testing the partmaster field label
    def test_partmaster_label(self):
        inventory_ins = Inventory.objects.get(id=1)
        field_label = inventory_ins._meta.get_field('partMaster').verbose_name
        self.assertEqual('partMaster', field_label)

        #Testing the qty field label in the model & it's corresponding field in forms
    def test_qty_label(self):
        inventory_ins = Inventory.objects.get(id=1)
        field_label = inventory_ins._meta.get_field('qty').verbose_name
        field_blank = inventory_ins._meta.get_field('qty').blank
        field_null = inventory_ins._meta.get_field('qty').null
        form = AddStockForm()
        form_field_required = form.fields['Quantity'].required
        self.assertEqual('qty', field_label)
        self.assertEqual(False, field_blank)
        self.assertEqual(False, field_null)
        self.assertEqual(True, form_field_required)

        #Testing the storeLoc field label in the model & it's corresponding field in forms
    def test_store_loc_label(self):
        inventory_ins = Inventory.objects.get(id=1)
        field_label = inventory_ins._meta.get_field('storeLoc').verbose_name
        field_blank = inventory_ins._meta.get_field('storeLoc').blank
        field_null = inventory_ins._meta.get_field('storeLoc').null
        form = AddStockForm()
        form_field_required = form.fields['Primary_Location'].required
        self.assertEqual('storeLoc', field_label)
        self.assertEqual(False, field_blank)
        self.assertEqual(False, field_null)
        self.assertEqual(True, form_field_required)        

        #Testing the secondary_loc field label in the model & it's corresponding field in forms
    def test_secondary_loc_label(self):
        inventory_ins = Inventory.objects.get(id=1)
        field_label = inventory_ins._meta.get_field('secondary_loc').verbose_name
        field_size = inventory_ins._meta.get_field('secondary_loc').max_length
        field_blank = inventory_ins._meta.get_field('secondary_loc').blank
        field_null = inventory_ins._meta.get_field('secondary_loc').null
        form = AddStockForm()
        form_field_required = form.fields['Secondary_Location'].required
        form_field_size = form.fields['Secondary_Location'].max_length
        self.assertEqual('secondary loc', field_label)
        self.assertEqual(30, field_size) 
        self.assertEqual(False, field_blank)
        self.assertEqual(False, field_null)
        self.assertEqual(True, form_field_required) 
        self.assertEqual(30, form_field_size)

        #Testing the free_stock  field label in the model & it's corresponding field in forms
    def test_free_stock_label(self):
        inventory_ins = Inventory.objects.get(id=1)
        field_label = inventory_ins._meta.get_field('free_stock').verbose_name
        field_default = inventory_ins._meta.get_field('free_stock').default
        form = AddStockForm()
        form_field_required = form.fields['free_stock'].required
        self.assertEqual('Free Stock', field_label)
        self.assertEqual(False, field_default)
        self.assertEqual(False, form_field_required)         

        #Testing the Comment  field label in the model & it's corresponding field in forms
    def test_comment_label(self):
        inventory_ins = Inventory.objects.get(id=1)
        field_label = inventory_ins._meta.get_field('comment').verbose_name
        field_size = inventory_ins._meta.get_field('comment').max_length
        field_null = inventory_ins._meta.get_field('comment').null
        field_blank = inventory_ins._meta.get_field('comment').blank
        form = AddStockForm()
        form_field_required = form.fields['Comment'].required
        form_field_size = form.fields['Comment'].max_length
        self.assertEqual('comment', field_label)
        self.assertEqual(100, field_size)
        self.assertEqual(False, field_null)
        self.assertEqual(False, field_blank)
        self.assertEqual(True, form_field_required)  
        self.assertEqual(100, form_field_size)      

class ReservationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #setup a non modifiable Object to use while testing
        bel_part_number_ins = BelPartNumber(belPartNo = '012345678912')
        bel_part_number_ins.save()
        part_master_ins = PartMaster(belPartNo = bel_part_number_ins, mpn = 'LMZ12003' , description = '3A power Regulator')
        part_master_ins.save()
        user_ins = User(username='217426', password = 'Bhanu#1149', email='bhanuseshuk@bel.co.in')
        user_ins.save()
        store_location_ins = StoreLocation(user = user_ins, primary_loc='CUP_BOARD1')
        store_location_ins.save()

        inventory_ins = Inventory( owner = user_ins, 
                                partMaster = part_master_ins,
                                qty = 100,
                                storeLoc = store_location_ins,
                                secondary_loc = 'packet1/slot1',
                                comment = 'test inventory ',
                                free_stock = False)      
        inventory_ins.save()   

        reservation_ins = Reservation(user=user_ins,
                                        inventory =inventory_ins,
                                        reservedQty = 10,
                                        comment="Test Reservation created",
                                        consumed = False )  
        reservation_ins.save()                                          

    def setUp(self):
        pass  
    #Testing the consumed  field label in the model & it's corresponding field in forms
    def test_consume_label(self):
        reservation_ins = Reservation.objects.get(id=1)
        field_label = reservation_ins._meta.get_field('consumed').verbose_name
        field_default = reservation_ins._meta.get_field('consumed').default
        form = MakeReservationForm()
        form_field_required = form.fields['comment'].required
        form_field_size = form.fields['comment'].max_length
        self.assertEqual('consumed', field_label)
        self.assertEqual(False, field_default)

    #Testing the Comment  field label in the model & it's corresponding field in forms
    def test_comment_label(self):
        reservation_ins = Reservation.objects.get(id=1)
        field_label = reservation_ins._meta.get_field('comment').verbose_name
        field_size = reservation_ins._meta.get_field('comment').max_length
        field_null = reservation_ins._meta.get_field('comment').null
        field_blank = reservation_ins._meta.get_field('comment').blank
        form = MakeReservationForm()
        form_field_required = form.fields['comment'].required
        form_field_size = form.fields['comment'].max_length
        self.assertEqual('comment', field_label)
        self.assertEqual(100, field_size)
        self.assertEqual(False, field_null)
        self.assertEqual(False, field_blank)
        self.assertEqual(True, form_field_required)  
        self.assertEqual(100, form_field_size)    

    #Testing the reservedQty field label in the model & it's corresponding field in forms
    def test_reservedQty_label(self):
        reservation_ins = Reservation.objects.get(id=1)
        field_label = reservation_ins._meta.get_field('reservedQty').verbose_name
        field_blank = reservation_ins._meta.get_field('reservedQty').blank
        field_null = reservation_ins._meta.get_field('reservedQty').null
        form = MakeReservationForm()
        form_field_required = form.fields['quantity'].required
        self.assertEqual('reservedQty', field_label)
        self.assertEqual(False, field_blank)
        self.assertEqual(False, field_null)
        self.assertEqual(True, form_field_required)                         

    #Testing the inventory field label in the model & it's corresponding field in forms
    def test_inventory_label(self):
        reservation_ins = Reservation.objects.get(id=1)
        field_label = reservation_ins._meta.get_field('inventory').verbose_name
        self.assertEqual('inventory', field_label)

    #Testing the user field label in the model & it's corresponding field in forms
    def test_user_label(self):
        reservation_ins = Reservation.objects.get(id=1)
        field_label = reservation_ins._meta.get_field('user').verbose_name
        self.assertEqual('user', field_label)

class StoreLocationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #setup a non modifiable Object to use while testing
        bel_part_number_ins = BelPartNumber(belPartNo = '012345678912')
        bel_part_number_ins.save()
        part_master_ins = PartMaster(belPartNo = bel_part_number_ins, mpn = 'LMZ12003' , description = '3A power Regulator')
        part_master_ins.save()
        user_ins = User(username='217426', password = 'Bhanu#1149', email='bhanuseshuk@bel.co.in')
        user_ins.save()
        store_location_ins = StoreLocation(user = user_ins, primary_loc='CUP_BOARD1')
        store_location_ins.save()                                        

    def setUp(self):
        pass   

    #Testing the user field label in the model & it's corresponding field in forms
    def test_user_label(self):
        store_location_ins = StoreLocation.objects.get(id=1)
        field_label = store_location_ins._meta.get_field('user').verbose_name
        self.assertEqual('user', field_label)

    #Testing the primary_location  field label in the model & it's corresponding field in forms
    def test_primary_location_label(self):
        store_location_ins = StoreLocation.objects.get(id=1)
        field_label = store_location_ins._meta.get_field('primary_loc').verbose_name
        field_size = store_location_ins._meta.get_field('primary_loc').max_length
        field_null = store_location_ins._meta.get_field('primary_loc').null
        field_blank = store_location_ins._meta.get_field('primary_loc').blank
        form = AddLocationForm()
        form_field_required = form.fields['primary_loc'].required
        form_field_size = form.fields['primary_loc'].max_length
        self.assertEqual('primary loc', field_label)
        self.assertEqual(30, field_size)
        self.assertEqual(False, field_null)
        self.assertEqual(False, field_blank)
        self.assertEqual(True, form_field_required)  
        self.assertEqual(30, form_field_size)        

class StockIssueModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        #setup a non modifiable Object to use while testing
        bel_part_number_ins = BelPartNumber(belPartNo = '012345678912')
        bel_part_number_ins.save()
        part_master_ins = PartMaster(belPartNo = bel_part_number_ins, mpn = 'LMZ12003' , description = '3A power Regulator')
        part_master_ins.save()
        user_ins = User(username='217426', password = 'Bhanu#1149', email='bhanuseshuk@bel.co.in')
        user_ins.save()
        store_location_ins = StoreLocation(user = user_ins, primary_loc='CUP_BOARD1')
        store_location_ins.save()

        inventory_ins = Inventory( owner = user_ins, 
                                partMaster = part_master_ins,
                                qty = 100,
                                storeLoc = store_location_ins,
                                secondary_loc = 'packet1/slot1',
                                comment = 'test inventory ',
                                free_stock = False)      
        inventory_ins.save()   

        reservation_ins = Reservation(user=user_ins,
                                        inventory =inventory_ins,
                                        reservedQty = 10,
                                        comment="Test Reservation created",
                                        consumed = False )  
        reservation_ins.save()

        stock_issue_ins = StockIssue(reservation = reservation_ins, comment = 'Test issue comment')
        stock_issue_ins.save()

    #Testing the reservation field label in the model & it's corresponding field in forms
    def test_reservation_label(self):
        stock_issue_ins = StockIssue.objects.get(id=1)
        field_label = stock_issue_ins._meta.get_field('reservation').verbose_name
        self.assertEqual('reservation', field_label)

    #Testing the Comment  field label in the model & it's corresponding field in forms
    def test_comment_label(self):
        stock_issue_ins = StockIssue.objects.get(id=1)
        field_label = stock_issue_ins._meta.get_field('comment').verbose_name
        field_size = stock_issue_ins._meta.get_field('comment').max_length
        field_null = stock_issue_ins._meta.get_field('comment').null
        field_blank = stock_issue_ins._meta.get_field('comment').blank
        form = MakeReservationForm()
        form_field_required = form.fields['comment'].required
        form_field_size = form.fields['comment'].max_length
        self.assertEqual('comment', field_label)
        self.assertEqual(100, field_size)
        self.assertEqual(False, field_null)
        self.assertEqual(False, field_blank)
        self.assertEqual(True, form_field_required)  
        self.assertEqual(100, form_field_size)         

