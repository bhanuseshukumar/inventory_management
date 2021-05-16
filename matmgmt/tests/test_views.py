from django.test import TestCase
from django.urls import reverse
from matmgmt.forms import CreateMaterialMasterForm, AddStockForm, MakeReservationForm, IssueReservationForm, AddLocationForm, SignupForm
from matmgmt.models import BelPartNumber, PartMaster, Inventory, Reservation, StoreLocation, StockIssue
from django.contrib.auth.models import User

class ShowMaterialViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        create_test_user(username=217426, password="Bhanu#1149", first_name='bhanu1', last_name='valluri1')
        create_test_user(username=217427, password="Bhanu#1149", first_name='bhanu2', last_name='valluri2')
        create_material_master_table(items_count=5, start_bel_part_no=123456789000, start_mpn='TEST MPN', start_description='TEST DESCRIPTION',user = 217426)
        create_material_master_table(items_count=5, start_bel_part_no=223456789000, start_mpn='TEST MPN', start_description='TEST DESCRIPTION',user = 217427)
        #----------- Testing show material view--------------
    def test_view_redirect_without_user_logged_in(self):
        #Teesting with path
        response = self.client.get('/matmgmt/list_material/')
        self.assertEqual(response.status_code, 302)       
        self.assertRedirects(response, '/accounts/login/?next=/matmgmt/list_material/')
        #testing same with the url name given in url.py
        response = self.client.get(reverse('material_master'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/matmgmt/list_material/')
    def test_view_after_user_logged_in(self):
        login = self.client.login(username='217426', password='Bhanu#1149')

        response = self.client.get(reverse('material_master'))
        #testing for status OK
        self.assertEqual(response.status_code, 200)
        #testing correct template is being used
        self.assertTemplateUsed(response, 'matmgmt/show_material.html')

    def test_show_material_view(self):
        item_count = 10
        login = self.client.login(username=217426, password='Bhanu#1149')
        
        response = self.client.get('/matmgmt/list_material/')
        self.assertEqual(response.status_code, 200)       
        self.assertTemplateUsed(response, 'matmgmt/show_material.html')
        #checking all the 10 items int the list are returned to template
        self.assertEqual(item_count, len(response.context['part_master']))
        #verify the returned context is same database
        for item in range(item_count):
            self.assertEqual(response.context['part_master'][item].user.username, PartMaster.objects.get(id=item+1).user.username)
            self.assertEqual(response.context['part_master'][item].belPartNo.belPartNo, PartMaster.objects.get(id=item+1).belPartNo.belPartNo)
            self.assertEqual(response.context['part_master'][item].mpn, PartMaster.objects.get(id=item+1).mpn)
            self.assertEqual(response.context['part_master'][item].description, PartMaster.objects.get(id=item+1).description)

class create_material_masterTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_test_user(username=217426, password="Bhanu#1149", first_name='bhanu1', last_name='valluri1')
    
    def test_view_redirection_without_user_loggedin(self):
        #----------- Testing material create view--------------
        response = self.client.get('/matmgmt/add_material/')
        self.assertEqual(response.status_code, 302)       
        self.assertRedirects(response, '/accounts/login/?next=/matmgmt/add_material/')

        response = self.client.get(reverse('add-material'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/matmgmt/add_material/')                  

    def test_view_with_user_loggedin(self):
        #----------- Testing material create view--------------
        login = self.client.login(username=217426, password='Bhanu#1149')
        response = self.client.get(reverse('add-material'))
        self.assertEqual(response.status_code, 200)
        #checking correct template is rendered
        self.assertTemplateUsed(response, 'matmgmt/create_material_master_form.html')                          

    def test_empty_material_form_rendered_on_get_request(self):
        login = self.client.login(username=217426, password='Bhanu#1149')
        
        response = self.client.get(reverse('add-material'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].initial,{})

    def test_meterial_creation_using_post_req(self):
        login = self.client.login(username=217426, password='Bhanu#1149')
        response = self.client.post(reverse('add-material'), {'BEL_PART_NUMBER':111122223333,"MPN":'manufacturer part no',"description":'part1 description'})
        self.assertRedirects(response, reverse('material_master'))
        db_bel_part_no = BelPartNumber.objects.get(belPartNo =111122223333 )
        db_part_master = PartMaster.objects.filter(belPartNo=db_bel_part_no)
        self.assertEqual(1,len(db_part_master))

    def test_meterial_creation_that_already_exist_in_db(self):
        login = self.client.login(username=217426, password='Bhanu#1149')
        response = self.client.post(reverse('add-material'), {'BEL_PART_NUMBER':111122223333,"MPN":'manufacturer part no',"description":'part1 description'})
        #lets create again same material & check for form error
        response = self.client.post(reverse('add-material'), {'BEL_PART_NUMBER':111122223333,"MPN":'manufacturer part no',"description":'part1 description'})
        self.assertFormError(response,"form", "MPN", "part list already exist")

class material_edit_view_Test(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_test_user(username=217426, password="Bhanu#1149", first_name='bhanu1', last_name='valluri1')    
        create_material_master_table(items_count=2, start_bel_part_no=123456789000, start_mpn='material_edit_view', start_description='material_edit_view',user = 217426)

    def test_view_redirect_without_user_logged_in(self):
        #Teesting with path
        response = self.client.get('/matmgmt/material/1/material-edit')
        self.assertEqual(response.status_code, 302)       
        self.assertRedirects(response, '/accounts/login/?next=/matmgmt/material/1/material-edit')
        #testing same with the url name given in url.py
        response = self.client.get(reverse('material-edit',kwargs={'pk':1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/matmgmt/material/1/material-edit')
   
    def test_view_with_user_loggedin(self):
        #-------------Testing Material edit view-------------------------
        login = self.client.login(username=217426, password='Bhanu#1149')
        response = self.client.get(reverse('material-edit',kwargs={'pk':1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'matmgmt/material_edit.html')  

    def test_initial_data_in_the_get_form_req(self):
        #-------------Testing Material edit view-------------------------
        login = self.client.login(username=217426, password='Bhanu#1149')
        response = self.client.get(reverse('material-edit',kwargs={'pk':2}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'].initial, {"BEL_PART_NUMBER" :"123456789001",
                                                            "MPN" : "material_edit_view1" ,
                                                            "description" : "material_edit_view1"})

    def test_post_form_req(self):
        #-------------Testing Material edit view-------------------------
        login = self.client.login(username=217426, password='Bhanu#1149')
        response = self.client.post(reverse('material-edit',kwargs={'pk':2}), {"BEL_PART_NUMBER" :"123456789001",
                                                                                "MPN" : "material_edit_view2" ,
                                                                                "description" : "material_edit_view2"})
        self.assertRedirects(response, reverse('material_master'))
        #checking againg whether posted data is saved by checking edit material initial data
        response = self.client.get(reverse('material-edit',kwargs={'pk':2}))
        self.assertEqual(response.context['form'].initial, {"BEL_PART_NUMBER" :"123456789001",
                                                            "MPN" : "material_edit_view2" ,
                                                            "description" : "material_edit_view2"})

class material_deleteTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_test_user(username=217426, password="Bhanu#1149", first_name='bhanu1', last_name='valluri1')    
        create_material_master_table(items_count=2, start_bel_part_no=123456789000, start_mpn='material_edit_view', start_description='material_edit_view',user = 217426)

    def test_view_redirect_without_user_logged_in(self):
        #-------------Testing Material delete view- with url as well as name------------------------                        
        response = self.client.get('/matmgmt/material/1/material-delete')
        self.assertEqual(response.status_code, 302)       
        self.assertRedirects(response, '/accounts/login/?next=/matmgmt/material/1/material-delete')

        response = self.client.get(reverse('material-delete',kwargs={'pk':1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/matmgmt/material/1/material-delete') 
        
    def test_view_with_user_loggedin(self):
        #-------------Testing Material delete view-------------------------                        
        login = self.client.login(username=217426, password='Bhanu#1149')

        response = self.client.get(reverse('material-delete',kwargs={'pk':1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'matmgmt/material_delete.html')   

    def test_initial_data_get_req_to_delete_material(self):
        #-------------Testing Material delete view-------------------------                        
        login = self.client.login(username=217426, password='Bhanu#1149')
        
        create_material_master_table(items_count=1, start_bel_part_no=123456789110, start_mpn='material_delete_view', start_description='material_delete_view',user = 217426)

        response = self.client.get(reverse('material-delete',kwargs={'pk':3}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['form'], {"BEL_PART_NUMBER" :"123456789110",
                                                            "MPN" : "material_delete_view0" ,
                                                            "description" : "material_delete_view0"})

    def test_data_post_req_to_delete_material(self):
        #-------------Testing Material delete view-------------------------                        
        login = self.client.login(username=217426, password='Bhanu#1149')
        create_material_master_table(items_count=1, start_bel_part_no=123456789110, start_mpn='material_delete_view', start_description='material_delete_view',user = 217426)
        response = self.client.post(reverse('material-delete',kwargs={'pk':3}))
        self.assertRedirects(response, reverse('material_master'))
        #checking deletion by accessing same material to receive 404 error
        response = self.client.get(reverse('material-delete',kwargs={'pk':3}))
        self.assertEqual(response.status_code, 404)


class add_stock_formview_Test(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_test_user(username=217426, password="Bhanu#1149", first_name='bhanu1', last_name='valluri1')    
        create_material_master_table(items_count=10, 
                                    start_bel_part_no=123456789000, 
                                    start_mpn='material_addstock_view', 
                                    start_description='material_add_stock_view', 
                                    user = 217426)
        create_test_user(username=217427, password="Bhanu#1149", first_name='bhanu2', last_name='valluri2')    
        create_primary_loc(start_location = 'cupboard', count=10, username = 217426)

    def test_view_redirect_without_user_logged_in(self):
        #-------------Testing inventory-add/stock-add view-------------------------                        
        response = self.client.get('/matmgmt/stock/1/add')
        self.assertEqual(response.status_code, 302)       
        self.assertRedirects(response, '/accounts/login/?next=/matmgmt/stock/1/add')

        response = self.client.get(reverse('add-stock', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/matmgmt/stock/1/add') 

    def test_view_with_user_loggedin(self):
            #-------------Testing inventory-add/stock-add view-------------------------                        
        login = self.client.login(username=217426, password='Bhanu#1149')
        response = self.client.get('/matmgmt/stock/1/add')
        self.assertEqual(response.status_code, 200)       
        self.assertTemplateUsed(response, 'matmgmt/add_stock.html')

        response = self.client.get(reverse('add-stock', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'matmgmt/add_stock.html')

    def test_initial_data_get_req_to_addstock_form_view(self):
        no_of_items = 10
        for i in range(no_of_items):
            if i>=5 :
                login = self.client.login(username=217426, password='Bhanu#1149')
            else:
                login = self.client.login(username=217427, password='Bhanu#1149')                

            response = self.client.get('/matmgmt/stock/'+str(i+1)+'/add')

            part = {"part_number" : response.context["part"].belPartNo.belPartNo,
                    "mpn"   :   response.context["part"].mpn,
                    "description" :    response.context["part"].description}
            db_part = {"part_number" : "12345678900" + str(i),
                        "mpn"   :   "material_addstock_view"+str(i),
                        "description" : "material_add_stock_view"+str(i)}
            
            self.assertEqual(part,db_part)
    
    def test_post_req_to_addstock_form_view(self):
        no_of_items = 10
        for i in range(no_of_items):
            if i<5 :
                login = self.client.login(username=217426, password='Bhanu#1149')
            else:
                login = self.client.login(username=217427, password='Bhanu#1149')                

            response = self.client.post(reverse('add-stock',kwargs={'pk':i+1}),data={   "Quantity" : i+10,
                                                                                        "Primary_Location" : i+1,
                                                                                        "Secondary_Location" : "second_loc-" + str(i),
                                                                                        "Comment" : 'comment'+str(i),
                                                                                        "free_stock" : False})
            self.assertRedirects(response, reverse("stock-list"))
            response = self.client.get(reverse("stock-list"))
            self.assertEqual(i+1,len(response.context['inventory']))
        
        inventory_query_set = Inventory.objects.all()
        for i in range(no_of_items):
            self.assertEqual(inventory_query_set[i].qty, i+10)
            self.assertEqual(inventory_query_set[i].storeLoc.primary_loc, "cupboard"+str(i))
            self.assertEqual(inventory_query_set[i].comment, "comment"+str(i))
            self.assertEqual(inventory_query_set[i].secondary_loc, "second_loc-"+str(i))
            self.assertEqual(inventory_query_set[i].free_stock, False)
            if i<5:
                self.assertEqual(inventory_query_set[i].owner.username, "217426")
            else:
                self.assertEqual(inventory_query_set[i].owner.username, "217427")

class inventoryListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_test_user(username=217426, password="Bhanu#1149", first_name='bhanu1', last_name='valluri1')    
        create_test_user(username=217427, password="Bhanu#1149", first_name='bhanu2', last_name='valluri2')    
        create_material_master_table(items_count=10, 
                                    start_bel_part_no=123456789000, 
                                    start_mpn='material_addstock_view', 
                                    start_description='material_add_stock_view', 
                                    user = 217426)
        create_primary_loc(start_location = 'cupboard', count=1, username = 217426)

    def test_view_redirect_without_user_logged_in(self):
        #-------------Testing inventory/stocklist view-------------------------                        
        response = self.client.get('/matmgmt/stock_list/')
        self.assertEqual(response.status_code, 302)       
        self.assertRedirects(response, '/accounts/login/?next=/matmgmt/stock_list/')

        response = self.client.get(reverse('stock-list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/matmgmt/stock_list/')     

    def test_view_with_user_loggedin(self):
        #-------------Testing inventory/stocklist view-------------------------                        
        login = self.client.login(username=217426, password='Bhanu#1149')
        create_inventory(username=217426, free_stock=False)
        response = self.client.get(reverse('stock-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'matmgmt/inventorylist.html')  
     #failing test case                
    def test_inventory_list_view(self):
        login = self.client.login(username=217426, password='Bhanu#1149')
        create_inventory(username=217426, free_stock=False)
        response = self.client.get(reverse('stock-list'))
        item_cnt = 10
        self.assertEqual(item_cnt, len(response.context["inventory"]))
        self.assertEqual(item_cnt, len(response.context["reserv_qty"]))
        #checking for zero reserved quantity of all
        self.assertEqual(0, sum(response.context["reserv_qty"]))
    
    def test_inventory_list_with_active_reservations_view(self):
        create_inventory(username=217426, free_stock=False,seed_qty = 100)
        do_reservation(username = 217426)
        login = self.client.login(username=217426, password='Bhanu#1149')
        response = self.client.get(reverse('stock-list'))
        item_cnt = 10
        for i in range(item_cnt):
            self.assertEqual(i+1, (response.context["reserv_qty"][i]))
        #Do a second reservation by second user
        do_reservation(username = 217426)
        #get again inventory list but now we had second reservations
        response = self.client.get(reverse('stock-list'))
        for i in range(item_cnt):
            self.assertEqual(2*(i+1), (response.context["reserv_qty"][i]))   

    def test_inventory_list_with_mutiples_users_reservations_view(self):
        create_inventory(username=217426, free_stock=False)
        do_reservation(username = 217426)
        login = self.client.login(username=217426, password='Bhanu#1149')
        response = self.client.get(reverse('stock-list'))
        item_cnt = 10
        for i in range(item_cnt):
            self.assertEqual(i+1, (response.context["reserv_qty"][i]))
        #Do a second reservation by second user
        create_inventory(username=217427, free_stock=False)
        do_reservation(username = 217427)
        #get again inventory list but now we had second user reservations also present
        response = self.client.get(reverse('stock-list'))
        self.assertEqual(item_cnt*2, len(response.context["reserv_qty"]))
        for i in range(item_cnt): #verifiy first user reserved qty
            self.assertEqual((i+1), (response.context["reserv_qty"][i]))
        for i in range(item_cnt,item_cnt*2): #verify second user reserved qty
            self.assertEqual((i+1-10), (response.context["reserv_qty"][i]))
    
    def test_inventory_list_with_users_consumptions_view(self):
        create_inventory(username=217426, free_stock=False)
        login = self.client.login(username=217426, password='Bhanu#1149')
        item_cnt = 10
        do_reservation(username = 217426)
        create_inventory(username=217427, free_stock=False) #create Inventory for 2nd user
        do_reservation(username = 217427)                                                     
        consume(username = 217427)  
        response = self.client.get(reverse('stock-list'))
        for i in range(item_cnt): #verifiy first user reserved qty
            self.assertEqual(i+1, response.context["reserv_qty"][i])        
        consume_flag = 0
        for i in range(item_cnt,item_cnt*2): #verify second user reserved qty taking into his consumptions into account
            if(consume_flag == 0):
                self.assertEqual(0, (response.context["reserv_qty"][i]))  
                consume_flag = 1
            else:
                self.assertEqual((i+1-10), (response.context["reserv_qty"][i]))
                consume_flag = 0

class stock_edit_view_Test(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_test_user(username=217426, password="Bhanu#1149", first_name='bhanu1', last_name='valluri1')    
        create_test_user(username=217427, password="Bhanu#1149", first_name='bhanu2', last_name='valluri2')    
        create_material_master_table(items_count=10, 
                                    start_bel_part_no=123456789000, 
                                    start_mpn='material_addstock_view', 
                                    start_description='material_add_stock_view', 
                                    user = 217426)
        create_primary_loc(start_location = 'cupboard', count=10, username = 217426)


    def test_view_redirect_without_user_logged_in(self):
        #-------------Testing inventory-edit/stock-edit view-------------------------                        
        response = self.client.get('/matmgmt/stock/1/stock-edit')
        self.assertEqual(response.status_code, 302)       
        self.assertRedirects(response, '/accounts/login/?next=/matmgmt/stock/1/stock-edit')

        response = self.client.get(reverse('stock-edit', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/matmgmt/stock/1/stock-edit')
    
    def test_view_with_user_loggedin(self):
        #-------------Testing inventory-edit/stock-edit view-------------------------  
        login = self.client.login(username=217427, password='Bhanu#1149')  
        create_inventory(username=217426, free_stock=False)

        response = self.client.get(reverse('stock-edit', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'matmgmt/stock_edit.html')

    def test_stock_edit_form_get_req_initial_data(self):
        #-------------Testing inventory-edit/stock-edit view-------------------------  
        login = self.client.login(username=217427, password='Bhanu#1149')  
        create_inventory(username=217426, free_stock=False)
        for i in range(10):
            response = self.client.get(reverse('stock-edit', kwargs={'pk':i+1}))
            inventory_context = {"partno" : response.context["inventory"].partMaster.belPartNo.belPartNo,
            "mpn"    : response.context["inventory"].partMaster.mpn,
            "description" : response.context["inventory"].partMaster.description,
            }
            inventory_ins = Inventory.objects.get(id=i+1)

            db_inventory = {
            "partno" : inventory_ins.partMaster.belPartNo.belPartNo,
            "mpn"    : inventory_ins.partMaster.mpn,
            "description" : inventory_ins.partMaster.description,
            }
            self.assertEqual(inventory_context, db_inventory) # checking heading 

            form_initial_data = {"qty" : response.context["form"].initial["Quantity"],
                "primary_location"    : response.context["form"].initial["Primary_Location"],
                "secondary_location" : response.context["form"].initial["Secondary_Location"],
                "comment"  : response.context["form"].initial["Comment"],
                "free_stock"  : response.context["form"].initial["free_stock"]
            }
            inventory_ins = Inventory.objects.get(id=i+1)

            form_db_data = {
            "qty" : inventory_ins.qty,
            "primary_location"    : inventory_ins.storeLoc.id,
            "secondary_location" : inventory_ins.secondary_loc,
            "comment" : inventory_ins.comment,
            "free_stock" :inventory_ins.free_stock
            }            
            self.assertEqual(form_db_data, form_initial_data) # checking initial data 


            self.assertTemplateUsed(response, 'matmgmt/stock_edit.html')

    def test_stock_edit_form_post_req(self):
        #-------------Testing inventory-edit/stock-edit view-------------------------  
        login = self.client.login(username=217426, password='Bhanu#1149')  
        create_inventory(username=217426, free_stock=False) # must login as same user
        for i in range(10):
            response = self.client.post(reverse('stock-edit', kwargs={'pk':i+1}), data={ "Quantity" : 20+i,
                                                                                        "Primary_Location" : 10-i,
                                                                                        "Secondary_Location" : "edit_second_loc-" + str(i),
                                                                                        "Comment" : 'edit_comment'+str(i),
                                                                                        "free_stock" : True})
            self.assertRedirects(response,reverse("stock-list"))   
            #check the updation status by checking initial data in the form again by going to edit inventory
            response = self.client.get(reverse('stock-edit', kwargs={'pk':i+1}))                                                                                     
            form_initial_data = {"qty" : response.context["form"].initial["Quantity"],
                "primary_location"    : response.context["form"].initial["Primary_Location"],
                "secondary_location" : response.context["form"].initial["Secondary_Location"],
                "comment"  : response.context["form"].initial["Comment"],
                "free_stock"  : response.context["form"].initial["free_stock"]
            }
            inventory_ins = Inventory.objects.get(id=i+1)

            form_db_data = {
            "qty" : 20+i,
            "primary_location"    : 10-i,
            "secondary_location" : "edit_second_loc-"+str(i),
            "comment" : "edit_comment"+str(i),
            "free_stock" :True
            }            
            self.assertEqual(form_db_data, form_initial_data) # checking initial data 

    def test_stock_edit_form_post_req_with_non_owner_user(self):
        #-------------Testing inventory-edit/stock-edit view-------------------------  
        login = self.client.login(username=217426, password='Bhanu#1149')  # Loging as diffrent user 217427
        create_inventory(username=217427, free_stock=False) #creating material as 217426
        for i in range(10):
            response = self.client.post(reverse('stock-edit', kwargs={'pk':i+1}), data={ "Quantity" : 20+i,
                                                                                        "Primary_Location" : 10-i,
                                                                                        "Secondary_Location" : "edit_second_loc-" + str(i),
                                                                                        "Comment" : 'edit_comment'+str(i),
                                                                                        "free_stock" : True})
            self.assertEqual(response.status_code, 200) # staying in the same page with error message in form errors list  
            #check the correct error message is displayed
            self.assertFormError(response, 'form', 'Quantity', 'You are not the owner of the inventory')
            
    def test_stock_edit_form_post_req_of_free_stock_with_non_owner_user(self):
        #-------------Testing inventory-edit/stock-edit view-------------------------  
        login = self.client.login(username=217426, password='Bhanu#1149')  # Loging as diffrent user 217427
        create_inventory(username=217427, free_stock=True) #creating material as 217426 but freestock
        for i in range(10):
            response = self.client.post(reverse('stock-edit', kwargs={'pk':i+1}), data={ "Quantity" : 20+i,
                                                                                        "Primary_Location" : 10-i,
                                                                                        "Secondary_Location" : "edit_second_loc-" + str(i),
                                                                                        "Comment" : 'edit_comment'+str(i),
                                                                                        "free_stock" : False})
            # should successfully redirect to inventory list since we are editing free stock                                                                                        
            self.assertRedirects(response,reverse("stock-list"))   
            #check the updation status by checking initial data in the form again by going to edit inventory
            response = self.client.get(reverse('stock-edit', kwargs={'pk':i+1}))                                                                                     
            form_initial_data = {"qty" : response.context["form"].initial["Quantity"],
                "primary_location"    : response.context["form"].initial["Primary_Location"],
                "secondary_location" : response.context["form"].initial["Secondary_Location"],
                "comment"  : response.context["form"].initial["Comment"],
                "free_stock"  : response.context["form"].initial["free_stock"]
            }
            inventory_ins = Inventory.objects.get(id=i+1)

            form_db_data = {
            "qty" : 20+i,
            "primary_location"    : 10-i,
            "secondary_location" : "edit_second_loc-"+str(i),
            "comment" : "edit_comment"+str(i),
            "free_stock" :False
            }            
            self.assertEqual(form_db_data, form_initial_data) # checking initial data   

     

class stock_delete_view_Test(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_test_user(username=217426, password="Bhanu#1149", first_name='bhanu1', last_name='valluri1')    
        create_test_user(username=217427, password="Bhanu#1149", first_name='bhanu2', last_name='valluri2')    
        create_material_master_table(items_count=10, 
                                    start_bel_part_no=123456789000, 
                                    start_mpn='material_delete_stock_view', 
                                    start_description='material_delete_stock_view', 
                                    user = 217426)
        create_primary_loc(start_location = 'cupboard', count=10, username = 217426)    

    def test_view_redirect_without_user_logged_in(self):
        #-------------Testing inventory-delete/stock-delete view-------------------------                        
        response = self.client.get('/matmgmt/stock/1/stock-delete')
        self.assertEqual(response.status_code, 302)       
        self.assertRedirects(response, '/accounts/login/?next=/matmgmt/stock/1/stock-delete')

        response = self.client.get(reverse('stock-delete', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/matmgmt/stock/1/stock-delete')       
    
    def test_view_with_user_loggedin(self):
        #-------------Testing inventory-delete/stock-delete view-------------------------                        
        login = self.client.login(username=217427, password='Bhanu#1149')
        create_inventory(username=217426, free_stock=False) 

        response = self.client.get(reverse('stock-delete', kwargs={'pk':1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'matmgmt/stock_delete.html') 

    def test_initial_data_get_req_to_stock_delete(self):
        #-------------Testing stock delete view-------------------------                        
        login = self.client.login(username=217426, password='Bhanu#1149')
        create_inventory(username=217426, free_stock=False) 

        for i in range(10):
            response = self.client.get(reverse('stock-delete',kwargs={'pk':i+1}))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context['form'], {"BEL_PART_NUMBER" :"12345678900"+str(i),
                                                                "MPN" : "material_delete_stock_view" +str(i) ,
                                                                "description" : "material_delete_stock_view"+str(i),
		                                                        "quantity" : i+10,})

    def test_data_post_req_to_stock_delete(self):
        #-------------Testing stock delete view-------------------------                        
        login = self.client.login(username=217426, password='Bhanu#1149')
        create_inventory(username=217426, free_stock=False) 

        for i in range(10):
            response = self.client.post(reverse('stock-delete',kwargs={'pk':i+1}))
            self.assertRedirects(response, reverse('stock-list'))
            #checking deletion by accessing same stock to receive 404 error
            response = self.client.get(reverse('stock-delete',kwargs={'pk':i+1}))
            self.assertEqual(response.status_code, 404)

    def test_other_user_stock_delete_restriction(self):
        #-------------Testing stock delete view-------------------------                        
        login = self.client.login(username=217426, password='Bhanu#1149')# create material as owner 2174276
        create_inventory(username=217427, free_stock=False) # try delete material as different user 217427

        for i in range(10):
            response = self.client.post(reverse('stock-delete',kwargs={'pk':i+1}))
            self.assertEqual(response.status_code, 200) # staying in the same page with error message in form errors list  
            #check the correct error message is displayed
            self.assertEqual(response.context["error_delete"],"You are not the owner of the inventory")

    def test_stock_delete_whose_reservations_exist(self):
        #-------------Testing stock delete view-------------------------                        
        login = self.client.login(username=217426, password='Bhanu#1149')# create material as owner 2174276
        create_inventory(username=217426, free_stock=False) # try delete material as different user 217427
        do_reservation(username = 217426)
        for i in range(10):
            response = self.client.post(reverse('stock-delete',kwargs={'pk':i+1}))
            self.assertEqual(response.status_code, 200) # staying in the same page with error message in form errors list  
            #check the correct error message is displayed
            self.assertGreater(len(response.context["reserv_list"]), 0)

class reservations_list_view_test(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_test_user(username=217426, password="Bhanu#1149", first_name='bhanu1', last_name='valluri1')    
        create_test_user(username=217427, password="Bhanu#1149", first_name='bhanu2', last_name='valluri2')    
        create_material_master_table(items_count=10, 
                                    start_bel_part_no=123456789000, 
                                    start_mpn='material_delete_stock_view', 
                                    start_description='material_delete_stock_view', 
                                    user = 217426)
        create_primary_loc(start_location = 'cupboard', count=10, username = 217426)      

    def test_view_redirect_without_user_logged_in(self):
        #-------------Testing reservation list view-------------------------                        
        response = self.client.get('/matmgmt/reservations_list/')
        self.assertEqual(response.status_code, 302)       
        self.assertRedirects(response, '/accounts/login/?next=/matmgmt/reservations_list/')

        response = self.client.get(reverse('reservations-list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/matmgmt/reservations_list/')  

    def test_view_with_user_loggedin(self):
        #-------------Testing reservation list view-------------------------  
        login = self.client.login(username=217426, password='Bhanu#1149')# create material as owner 2174276                            

        response = self.client.get(reverse('reservations-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'matmgmt/reservations_list.html') 

    def test_reservations_list(self):
        login = self.client.login(username=217426, password='Bhanu#1149')# create material as owner 2174276                            
        create_inventory(username=217426, free_stock=False) 
        do_reservation(username = 217426)
        response = self.client.get(reverse('reservations-list'))
        self.assertEqual(10,len(response.context["reservations"]))        

    def test_reservations_list_with_consumed_exist(self):
        login = self.client.login(username=217426, password='Bhanu#1149')# create material as owner 2174276                            
        create_inventory(username=217426, free_stock=False, seed_qty =100) 
        do_reservation(username = 217426)   #creates 10 reservations
        consume(username = 217426)      # consumes 5
        consume(username = 217426)      # consumes 5/2 ~= 3
        response = self.client.get(reverse('reservations-list'))
        
        self.assertEqual(2,len(response.context["reservations"])) 

class add_reservation_Test(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_test_user(username=217426, password="Bhanu#1149", first_name='bhanu1', last_name='valluri1')    
        create_test_user(username=217427, password="Bhanu#1149", first_name='bhanu2', last_name='valluri2')    

        create_material_master_table(items_count=10, 
                                    start_bel_part_no=123456789000, 
                                    start_mpn='material_addstock_view', 
                                    start_description='material_add_stock_view', 
                                    user = 217426)
        create_primary_loc(start_location = 'cupboard', count=10, username = 217426)

    def test_view_redirect_without_user_logged_in(self):
        #-------------Testing add reservation view-------------------------                        
        response = self.client.get('/matmgmt/reservation/1/add')
        self.assertEqual(response.status_code, 302)       
        self.assertRedirects(response, '/accounts/login/?next=/matmgmt/reservation/1/add')

        response = self.client.get(reverse('add-reservation', kwargs ={'pk':1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/matmgmt/reservation/1/add')

    def test_view_with_user_loggedin(self):
         #-------------Testing add reservation view-------------------------                        
        login = self.client.login(username=217426, password='Bhanu#1149')# create material as owner 2174276                            
        create_inventory(username=217427, free_stock=False)   # purposefuly tryto to create inventory using other user material master
        response = self.client.get(reverse('add-reservation', kwargs ={'pk':1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'matmgmt/add_reservation.html') 

    def test_initial_data_get_req_to_add_reservation_form_view(self):
        login = self.client.login(username=217426, password='Bhanu#1149')# create material as owner 2174276                            
        create_inventory(username=217426, free_stock=False)   
        create_inventory(username=217427, free_stock=False) 
        no_of_items = 20
        for i in range(no_of_items):
            if i>=10 :
                login = self.client.login(username=217427, password='Bhanu#1149')
            else:
                login = self.client.login(username=217426, password='Bhanu#1149')                

            response = self.client.get(reverse('add-reservation', kwargs ={'pk':i+1}))
            
            self.assertEqual(response.context["inventory"], Inventory.objects.get(id = i+1))

    def test_post_req_to_add_reservation_form_view(self):
        login = self.client.login(username=217426, password='Bhanu#1149')# create material as owner 2174276                            
        create_inventory(username=217426, free_stock=False)   
        create_inventory(username=217427, free_stock=False) 
        no_of_items = 20
        for i in range(no_of_items):
            if i>=10 :
                login = self.client.login(username=217427, password='Bhanu#1149')
            else:
                login = self.client.login(username=217426, password='Bhanu#1149')                 

            response = self.client.post(reverse('add-reservation', kwargs ={'pk':i+1}), data = {
                                                                                                "quantity" : (i%10)+1 ,
                                                                                                "comment" :'testing make reservation'+str(i) })
            self.assertRedirects(response, reverse('reservations-list'))
        response = self.client.get(reverse('reservations-list'))
        self.assertEqual(20,len(response.context["reservations"])) 

    def test_post_req_to_add_reservation_form_with_qty_morethan_available_qty_view(self):
        login = self.client.login(username=217426, password='Bhanu#1149')# create material as owner 2174276                            
        create_inventory(username=217426, free_stock=False)  #user 1 creates 10 stock
        create_inventory(username=217427, free_stock=False)  #another 10 by user 2
        no_of_items = 20 # total inventory by user1 & user2
        for i in range(no_of_items):
            if i>=10 :#login appropriately
                login = self.client.login(username=217427, password='Bhanu#1149')
            else:
                login = self.client.login(username=217426, password='Bhanu#1149')                 
            # try to reserve more quantity
            response = self.client.post(reverse('add-reservation', kwargs ={'pk':i+1}), data = {
                                                                                                "quantity" : (i%10)+11 ,
                                                                                                "comment" :'testing make reservation'+str(i) })
            self.assertEqual(response.status_code, 200) # checking to remain in same page
            self.assertFormError(response, 'form', 'quantity', 'reserved Qty is more than stock')

    def test_post_req_to_add_reservation_to_other_users_inventory(self):
        login = self.client.login(username=217427, password='Bhanu#1149')# user2 logs in
        create_inventory(username=217426, free_stock=False)  #user 1 creates 10 stock
        no_of_items = 10 # total inventory by user1 
        for i in range(no_of_items):
            # try to reserve more quantity
            response = self.client.post(reverse('add-reservation', kwargs ={'pk':i+1}), data = {
                                                                                                "quantity" : (i%10)+1 ,
                                                                                                "comment" :'testing make reservation'+str(i) })
            self.assertEqual(response.status_code, 200) # checking to remain in same page
            self.assertFormError(response, 'form', 'quantity', 'Your not the owner of this inventory')

    def test_post_req_to_add_reservation_to_other_users_free_inventory(self):
        login = self.client.login(username=217427, password='Bhanu#1149')# user2 logs in
        create_inventory(username=217426, free_stock=True)  #user 1 creates 10 stock
        no_of_items = 10 # total inventory by user1 
        for i in range(no_of_items):
            # try to reserve more quantity
            response = self.client.post(reverse('add-reservation', kwargs ={'pk':i+1}), data = {
                                                                                                "quantity" : (i%10)+1 ,
                                                                                                "comment" :'testing make reservation'+str(i) })
            response = self.client.get(reverse('reservations-list'))
        self.assertEqual(10,len(response.context["reservations"]))                                  

class reservation_edit_Test(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_test_user(username=217426, password="Bhanu#1149", first_name='bhanu1', last_name='valluri1')    
        create_test_user(username=217427, password="Bhanu#1149", first_name='bhanu2', last_name='valluri2')    

        create_material_master_table(items_count=10, 
                                    start_bel_part_no=123456789000, 
                                    start_mpn='material_addstock_view', 
                                    start_description='material_add_stock_view', 
                                    user = 217426)
        create_primary_loc(start_location = 'cupboard', count=10, username = 217426)

    def test_view_redirect_without_user_logged_in(self):
        #-------------Testing edit reservation list view-------------------------                        
        response = self.client.get('/matmgmt/reservation/1/reservation-edit')
        self.assertEqual(response.status_code, 302)       
        self.assertRedirects(response, '/accounts/login/?next=/matmgmt/reservation/1/reservation-edit')

        response = self.client.get(reverse('reservation-edit', kwargs ={'pk':1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/matmgmt/reservation/1/reservation-edit') 
    def test_view_with_user_loggedin(self):
        #-------------Testing edit reservation list view-------------------------                        
        login = self.client.login(username=217427, password='Bhanu#1149')
        create_inventory(username=217426, free_stock=True)  #user 1 creates 10 stock
        do_reservation(username = 217426)
        for i in range(10):
            response = self.client.get(reverse('reservation-edit', kwargs ={'pk':1}))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'matmgmt/reservations_edit.html') 

    def test_reservation_edit_form_get_req_initial_data(self):
        #-------------Testing reservation-edit view-------------------------  
        login = self.client.login(username=217426, password='Bhanu#1149')  
        create_inventory(username=217426, free_stock=False)
        do_reservation(username=217426)
        for i in range(10):
            response = self.client.get(reverse('reservation-edit', kwargs={'pk':i+1}))
            inventory_ins = Inventory.objects.get(id=i+1)
            self.assertEqual(response.context["inventory"],inventory_ins ) # checking heading 

            form_initial_data = {"quantity" : response.context["form"].initial["quantity"],
                "comment"  : response.context["form"].initial["comment"],
            }
            reservation_ins = Reservation.objects.get(id=i+1)

            form_db_data = {
            "quantity" : reservation_ins.reservedQty,
            "comment" : reservation_ins.comment,
            }            
            self.assertEqual(form_db_data, form_initial_data) # checking initial data 

    def test_reservation_edit_form_post_req(self):
        #-------------Testing inventory-edit/stock-edit view-------------------------  
        login = self.client.login(username=217426, password='Bhanu#1149')  
        create_inventory(username=217426, free_stock=False) # must login as same user
        do_reservation(username=217426)
        for i in range(10):
            response = self.client.post(reverse('reservation-edit', kwargs={'pk':i+1}), data = {
                                                                                                "quantity" :(i%10)+2,
                                                                                                "comment" :'testing edit reservation'+str(i+1) })
            self.assertRedirects(response,reverse("reservations-list"))   
            #check the updation status by checking initial data in the form again by going to edit inventory
            response = self.client.get(reverse('reservation-edit', kwargs={'pk':i+1}))                                                                                     
            form_initial_data = {"quantity" : response.context["form"].initial["quantity"],
                "comment"  : response.context["form"].initial["comment"],
            }
            reservation_ins = Reservation.objects.get(id=i+1)

            form_db_data = {
            "quantity" : (i%10)+2,
            "comment" : "testing edit reservation"+str(i+1),
            }            
            self.assertEqual(form_db_data, form_initial_data) # checking initial data 

    def test_reservation_edit_form_post_req_with_non_owner_user(self):
        #-------------Testing inventory-edit/stock-edit view-------------------------  
        login = self.client.login(username=217426, password='Bhanu#1149')  # Loging as diffrent user 217427
        create_inventory(username=217427, free_stock=True) #creating material as 217426
        do_reservation(username = 217427)
        for i in range(10):
            response = self.client.post(reverse('reservation-edit', kwargs={'pk':i+1}), data = {
                                                                                                "quantity" :(i%10)+2,
                                                                                                "comment" :'testing edit reservation'+str(i+1) })
            self.assertEqual(response.status_code, 200) # staying in the same page with error message in form errors list  
            #check the correct error message is displayed
            self.assertFormError(response, 'form', 'quantity', "Can't edit other users reservations")

    def test_reservation_edit_form_post_req_with_reserve_qty_more_than_available_qty(self):
        #-------------Testing inventory-edit/stock-edit view-------------------------  
        login = self.client.login(username=217427, password='Bhanu#1149')  # Loging as diffrent user 217427
        create_inventory(username=217427, free_stock=True) #creating material as 217426
        do_reservation(username = 217427)
        for i in range(10):
            
            response = self.client.post(reverse('reservation-edit', kwargs={'pk':i+1}), data = {
                                                                                                "quantity" :i+11,
                                                                                                "comment" :'testing edit reservation'+str(i+1) })
            self.assertEqual(response.status_code, 200) # staying in the same page with error message in form errors list  
            #check the correct error message is displayed
            self.assertFormError(response, 'form', 'quantity', "reserved Qty is more than stock")


class reservation_delete_view(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_test_user(username=217426, password="Bhanu#1149", first_name='bhanu1', last_name='valluri1')    
        create_test_user(username=217427, password="Bhanu#1149", first_name='bhanu2', last_name='valluri2')    

        create_material_master_table(items_count=10, 
                                    start_bel_part_no=123456789000, 
                                    start_mpn='material_addstock_view', 
                                    start_description='material_addstock_view', 
                                    user = 217426)
        create_primary_loc(start_location = 'cupboard', count=10, username = 217426)
        

    def test_view_redirect_without_user_logged_in(self):
        #-------------Testing delete reservation list view-------------------------                        
        response = self.client.get('/matmgmt/reservation/1/reservation-delete')
        self.assertEqual(response.status_code, 302)       
        self.assertRedirects(response, '/accounts/login/?next=/matmgmt/reservation/1/reservation-delete')

        response = self.client.get(reverse('reservation-delete', kwargs ={'pk':1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/matmgmt/reservation/1/reservation-delete') 

    def test_view_with_user_loggedin(self):
        #-------------Testing delete reservation list view-------------------------    
        login = self.client.login(username=217426, password='Bhanu#1149')                    
        create_inventory(username=217426, free_stock=True)  #user 1 creates 10 stock
        do_reservation(username = 217426)   # same user makes reservation for each     
        response = self.client.get(reverse('reservation-delete', kwargs ={'pk':10}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'matmgmt/reservations_delete.html')

    def test_initial_data_get_req_to_delete_material(self):
        #-------------Testing reservations delete view-------------------------                        
        login = self.client.login(username=217426, password='Bhanu#1149')                    
        create_inventory(username=217426, free_stock=True)  #user 1 creates 10 stock
        do_reservation(username = 217426)   # same user makes reservation for each  
        for i in range(10):
            response = self.client.get(reverse('reservation-delete', kwargs ={'pk':i+1}))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context['form'], {"BEL_PART_NUMBER" :"12345678900"+str(i),
                                                                "MPN" : "material_addstock_view"+str(i) ,
                                                                "description" : "material_addstock_view"+str(i),
                                                                "quantity" : i+1})

    def test_data_post_req_to_delete_reservation(self):
        #-------------Testing reservations delete view-------------------------                        
        login = self.client.login(username=217426, password='Bhanu#1149')                    
        create_inventory(username=217426, free_stock=True)  #user 1 creates 10 stock
        do_reservation(username = 217426)   # same user makes reservation for each  
        for i in range(10):
            response = self.client.post(reverse('reservation-delete', kwargs ={'pk':i+1}))
            self.assertRedirects(response,reverse("reservations-list")) 

            #checking deletion by accessing same reservation to receive 404 error
            response = self.client.get(reverse('reservation-delete', kwargs ={'pk':i+1}))
            self.assertEqual(response.status_code, 404)

    def test_data_post_req_to_delete_restriction_to_other_user_reservation(self):
        #-------------Testing reservations delete view-------------------------                        
        login = self.client.login(username=217427, password='Bhanu#1149')#login as different user
        create_inventory(username=217426, free_stock=True)  #user 1 creates 10 stock
        do_reservation(username = 217426)   # same user makes reservation for each  
        for i in range(10):
            response = self.client.post(reverse('reservation-delete', kwargs ={'pk':i+1}))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context["error_delete"],"Can't delete others users reservations")

    def test_data_post_req_to_delete_restriction_with_consume_data_pointing_2_reservations(self):
        #-------------Testing reservations delete view-------------------------                        
        login = self.client.login(username=217426, password='Bhanu#1149')#login as different user
        create_inventory(username=217426, free_stock=False)  #user 1 creates 10 stock
        do_reservation(username = 217426)   # same user makes reservation for each  
        consume(username = 217426)
        for i in range(10):
            response = self.client.post(reverse('reservation-delete', kwargs ={'pk':i+1}))
            if((i+1)%2 == 0):
                self.assertRedirects(response,reverse("reservations-list")) 
            else:
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.context["error_delete"], "Can't delete reservations with consume records")

class reservationsFilterView(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_test_user(username=217426, password="Bhanu#1149", first_name='bhanu1', last_name='valluri1')    
        create_test_user(username=217427, password="Bhanu#1149", first_name='bhanu2', last_name='valluri2')    

        create_material_master_table(items_count=10, 
                                    start_bel_part_no=123456789000, 
                                    start_mpn='material_addstock_view', 
                                    start_description='material_addstock_view', 
                                    user = 217426)
        create_primary_loc(start_location = 'cupboard', count=10, username = 217426)   

    def test_view_redirect_without_user_logged_in(self):
        #-------------Testing filtered reservation list view-------------------------                        
        response = self.client.get('/matmgmt/reservation/1/filter')
        self.assertEqual(response.status_code, 302)       
        self.assertRedirects(response, '/accounts/login/?next=/matmgmt/reservation/1/filter')

        response = self.client.get(reverse('reservation-filter', kwargs ={'pk':1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/matmgmt/reservation/1/filter') 
    
    def test_view_with_user_loggedin(self):
        #-------------Testing filtered reservation list view-------------------------                        
        login = self.client.login(username=217426, password='Bhanu#1149')                    
        create_inventory(username=217426, free_stock=False)  #user 1 creates 10 stock
        do_reservation(username = 217426, reserv_qty_rule=2)   # same user makes reservation for each 
        do_reservation(username = 217426, reserv_qty_rule=2)   # same user makes reservation for each     
        do_reservation(username = 217426, reserv_qty_rule=2)   # same user makes reservation for each     
        consume(username = 217426) #consuming all the odd records. 
        response = self.client.get(reverse('reservation-filter', kwargs ={'pk':1}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["reservations"]) ,0) # all the reservations would have consumed
        response = self.client.get(reverse('reservation-filter', kwargs ={'pk':2}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["reservations"]) ,3)

class consume_view_Test(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_test_user(username=217426, password="Bhanu#1149", first_name='bhanu1', last_name='valluri1')    
        create_test_user(username=217427, password="Bhanu#1149", first_name='bhanu2', last_name='valluri2')    

        create_material_master_table(items_count=10, 
                                    start_bel_part_no=123456789000, 
                                    start_mpn='material_addstock_view', 
                                    start_description='material_addstock_view', 
                                    user = 217426)
        create_primary_loc(start_location = 'cupboard', count=10, username = 217426) 

    def test_view_redirect_without_user_logged_in(self):
        #-------------Testing consume  view-------------------------                        
        response = self.client.get('/matmgmt/reservation/1/consume')
        self.assertEqual(response.status_code, 302)       
        self.assertRedirects(response, '/accounts/login/?next=/matmgmt/reservation/1/consume')

        response = self.client.get(reverse('consume', kwargs ={'pk':1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/matmgmt/reservation/1/consume') 

    def test_view_with_user_loggedin(self):
        #-------------Testing consume  view-------------------------                        
        login = self.client.login(username=217426, password='Bhanu#1149')  
        create_inventory(username=217426, free_stock=False)  #user 1 creates 10 stock        
        do_reservation(username = 217426)              
        response = self.client.get(reverse('consume', kwargs ={'pk':1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'matmgmt/consume.html') 

    def test_get_req_to_consume_form_view(self):
        #-------------Testing consume  view-------------------------                        
        login = self.client.login(username=217426, password='Bhanu#1149')  
        create_inventory(username=217426, free_stock=False)  #user 1 creates 10 stock        
        do_reservation(username = 217426)
        for i in range(10):
            response = self.client.get(reverse('consume', kwargs ={'pk':i+1}))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(Reservation.objects.get(id = i+1), response.context["reservation"])

    def test_post_req_to_consume_form_view(self):
        #-------------Testing consume  view-------------------------                        
        login = self.client.login(username=217426, password='Bhanu#1149')  
        create_inventory(username=217426, free_stock=True)  #user 1 creates 10 stock        
        do_reservation(username = 217426)
        for i in range(10):
            response = self.client.post(reverse('consume', kwargs ={'pk':i+1}), data = {"comment" : "test consume"+str(i)})
            self.assertRedirects(response, reverse('issues-list')) 
            response =  self.client.get(reverse('issues-list')) 
            self.assertEqual(i+1,len(response.context["stock_issues"])) # checking if issues list is updated with new consume records
            # also check if reservation is removed from the list
            response =  self.client.get(reverse('reservations-list')) 
            self.assertEqual(9-i,len(response.context["reservations"])) 

    def test_post_req_to_consume_form_by_a_non_owner_of_reservation(self):
        #-------------Testing consume  view-------------------------                        
        create_inventory(username=217426, free_stock=True)  #user 1 creates 10 stock        
        do_reservation(username = 217426)
        login = self.client.login(username=217427, password='Bhanu#1149')  #login as different user

        for i in range(10):
            response = self.client.post(reverse('consume', kwargs ={'pk':i+1}), data = {"comment" : "test consume"+str(i)})
            self.assertEqual(response.status_code, 200) 
            self.assertFormError(response, 'form', 'comment', "can't consume other users reservations")


class issuesListView(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_test_user(username=217426, password="Bhanu#1149", first_name='bhanu1', last_name='valluri1')    
        create_test_user(username=217427, password="Bhanu#1149", first_name='bhanu2', last_name='valluri2')    

        create_material_master_table(items_count=10, 
                                    start_bel_part_no=123456789000, 
                                    start_mpn='material_addstock_view', 
                                    start_description='material_addstock_view', 
                                    user = 217426)
        create_primary_loc(start_location = 'cupboard', count=10, username = 217426)   

    def test_view_redirect_without_user_logged_in(self):
        #-------------Testing issues  view-------------------------                        
        response = self.client.get('/matmgmt/issues/')
        self.assertEqual(response.status_code, 302)       
        self.assertRedirects(response, '/accounts/login/?next=/matmgmt/issues/')

        response = self.client.get(reverse('issues-list'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/matmgmt/issues/')

    def test_view_with_user_loggedin(self):
        login = self.client.login(username=217426, password='Bhanu#1149')  
        #-------------Testing issues  view-------------------------                        
        create_inventory(username=217426, free_stock=True)  #user 1 creates 10 stock        
        do_reservation(username = 217426)
        consume(username = 217426)  # consumes alternative records       
        response = self.client.get(reverse('issues-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(5,len(response.context["stock_issues"]))
        self.assertTemplateUsed(response, 'matmgmt/issue_list.html') 

    def test_view_with_zero_records(self):
        login = self.client.login(username=217426, password='Bhanu#1149')  
        #-------------Testing issues  view-------------------------                        
        create_inventory(username=217426, free_stock=True)  #user 1 creates 10 stock        
        do_reservation(username = 217426)
        response = self.client.get(reverse('issues-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(0,len(response.context["stock_issues"]))

class issue_edit_view_Test(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_test_user(username=217426, password="Bhanu#1149", first_name='bhanu1', last_name='valluri1')    
        create_test_user(username=217427, password="Bhanu#1149", first_name='bhanu2', last_name='valluri2')    

        create_material_master_table(items_count=10, 
                                    start_bel_part_no=123456789000, 
                                    start_mpn='material_addstock_view', 
                                    start_description='material_addstock_view', 
                                    user = 217426)
        create_primary_loc(start_location = 'cupboard', count=10, username = 217426)   

    def test_view_redirect_without_user_logged_in(self):
        #-------------Testing issues  edit-------------------------                        
        response = self.client.get('/matmgmt/issue/1/issue-edit')
        self.assertEqual(response.status_code, 302)       
        self.assertRedirects(response, '/accounts/login/?next=/matmgmt/issue/1/issue-edit')

        response = self.client.get(reverse('issue-edit', kwargs={"pk":1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/matmgmt/issue/1/issue-edit')

    def test_view_with_user_loggedin(self):
        login = self.client.login(username=217426, password='Bhanu#1149') 
        create_inventory(username = 217426, free_stock = False) 
        do_reservation(username = 217426)
        consume(username = 217426)
        #-------------Testing issues  edit-------------------------                        
        for i in range(5):
            response = self.client.get(reverse('issue-edit', kwargs={"pk":i+1}))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'matmgmt/issue_edit.html')         

    def test_get_req_to_consume_edit_form_initial_data(self):
        login = self.client.login(username=217426, password='Bhanu#1149') 
        create_inventory(username = 217426, free_stock = False) 
        do_reservation(username = 217426)
        consume(username = 217426)
        #-------------Testing issues  edit-------------------------                        
        for i in range(5):
            response = self.client.get(reverse('issue-edit', kwargs={"pk":i+1}))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context["form"].initial["comment"],"test issue"+str(i*2))
            self.assertEqual(response.context["reservation"], response.context["reservation"])

    def test_post_req_to_consume_edit_form_data(self):
        login = self.client.login(username=217426, password='Bhanu#1149') 
        create_inventory(username = 217426, free_stock = False) 
        do_reservation(username = 217426)
        consume(username = 217426)
        #-------------Testing issues  edit-------------------------                        
        for i in range(5):
            response = self.client.post(reverse('issue-edit', kwargs={"pk":i+1}), data = {"comment" : "post_req_success"+str(i) })
            self.assertRedirects(response, reverse("issues-list"))
            #check updation by going to edit link again.
            response = self.client.get(reverse('issue-edit', kwargs={"pk":i+1}))
            self.assertEqual(response.context["form"].initial["comment"],"post_req_success"+str(i))

    def test_restrict_post_req_to_consume_edit_form_of_other_users(self):
        login = self.client.login(username=217427, password='Bhanu#1149') #login as different user
        create_inventory(username = 217426, free_stock = True) 
        do_reservation(username = 217426)
        consume(username = 217426)
        #-------------Testing issues  edit-------------------------                        
        for i in range(5):
            response = self.client.post(reverse('issue-edit', kwargs={"pk":i+1}), data = {"comment" : "post_req_success"+str(i) })
            self.assertEqual(response.status_code, 200) # staying in same form with error code
            #check updation by going to edit link again.
            self.assertFormError(response,"form", 'comment', "Can't edit other users consume records")

class issues_delete_view_Test(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_test_user(username=217426, password="Bhanu#1149", first_name='bhanu1', last_name='valluri1')    
        create_test_user(username=217427, password="Bhanu#1149", first_name='bhanu2', last_name='valluri2')    

        create_material_master_table(items_count=10, 
                                    start_bel_part_no=123456789000, 
                                    start_mpn='issue_delete_stock_view', 
                                    start_description='issue_delete_stock_view', 
                                    user = 217426)
        create_primary_loc(start_location = 'cupboard', count=10, username = 217426)


    def test_view_redirect_without_user_logged_in(self):
        #-------------Testing issues  delete-------------------------                        
        response = self.client.get('/matmgmt/issue/1/issue-delete')
        self.assertEqual(response.status_code, 302)       
        self.assertRedirects(response, '/accounts/login/?next=/matmgmt/issue/1/issue-delete')

        response = self.client.get(reverse('issue-delete', kwargs={"pk":1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/matmgmt/issue/1/issue-delete') 

    def test_view_with_user_loggedin(self):
        #-------------Testing issues  delete-------------------------                        
        login = self.client.login(username=217426, password='Bhanu#1149') 
        create_inventory(username = 217426, free_stock = False) 
        do_reservation(username = 217426)
        consume(username = 217426)
        for i in range(5):
            response = self.client.get(reverse('issue-delete', kwargs={"pk":i+1}))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'matmgmt/issue_delete.html')        

    def test_initial_data_get_req_to_issue_delete(self):
        #-------------Testing stock delete view-------------------------                        
        login = self.client.login(username=217426, password='Bhanu#1149')
        create_inventory(username = 217426, free_stock = False) 
        do_reservation(username = 217426)
        consume(username = 217426)
        for i in range(5):
            response = self.client.get(reverse('issue-delete',kwargs={'pk':i+1}))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.context['form'], {"BEL_PART_NUMBER" :"12345678900"+str(i*2),
                                                                "MPN" : "issue_delete_stock_view" +str(i*2) ,
                                                                "description" : "issue_delete_stock_view"+str(i*2),
		                                                        "quantity" : (i*2+1),})

    def test_data_post_req_to_issue_delete(self):
        #-------------Testing stock delete view-------------------------                        
        login = self.client.login(username=217426, password='Bhanu#1149')
        create_inventory(username = 217426, free_stock = False) 
        do_reservation(username = 217426)
        consume(username = 217426) 
        for i in range(5):
            response = self.client.post(reverse('issue-delete',kwargs={'pk':i+1}))
            self.assertRedirects(response, reverse('issues-list'))
            #checking deletion by accessing same stock to receive 404 error
            response = self.client.post(reverse('issue-delete',kwargs={'pk':i+1}))
            self.assertEqual(response.status_code, 404)

    def test_other_user_issues_delete_restriction(self):
        #-------------Testing issues delete view-------------------------                        
        login = self.client.login(username=217427, password='Bhanu#1149') # loging as other user
        create_inventory(username = 217426, free_stock = False) 
        do_reservation(username = 217426)
        consume(username = 217426) 
        for i in range(5):
            response = self.client.post(reverse('issue-delete',kwargs={'pk':i+1}))
            #checking deletion by accessing other user issue 
            self.assertEqual(response.status_code, 200) # staying in the same page with error message in form errors list  
            #check the correct error message is displayed
            self.assertEqual(response.context["error_delete"],"Can't delete other users consume records")


class issueFilterView(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_test_user(username=217426, password="Bhanu#1149", first_name='bhanu1', last_name='valluri1')    
        create_test_user(username=217427, password="Bhanu#1149", first_name='bhanu2', last_name='valluri2')    

        create_material_master_table(items_count=10, 
                                    start_bel_part_no=123456789000, 
                                    start_mpn='material_addstock_view', 
                                    start_description='material_addstock_view', 
                                    user = 217426)
        create_primary_loc(start_location = 'cupboard', count=10, username = 217426)   

    def test_view_redirect_without_user_logged_in(self):
        #-------------Testing issues  filter view-------------------------                        
        response = self.client.get('/matmgmt/issue/1/filter')
        self.assertEqual(response.status_code, 302)       
        self.assertRedirects(response, '/accounts/login/?next=/matmgmt/issue/1/filter')

        response = self.client.get(reverse('issue-filter', kwargs={"pk":1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/matmgmt/issue/1/filter')   
    
    def test_view_with_user_loggedin(self):
        #-------------Testing filtered reservation list view-------------------------                        
        login = self.client.login(username=217426, password='Bhanu#1149') 
        create_inventory(username = 217426, free_stock = False,seed_qty=100) 
        do_reservation(username = 217426, reserv_qty_rule=2)
        #-------------Testing issues  filter view-------------------------                        
        for i in range(10):
            response = self.client.get(reverse('issue-filter', kwargs={"pk":i+1}))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(0, (response.context["stock_issues"])) # checking with zero consume recoreds
        self.assertTemplateUsed(response, 'matmgmt/issue_list.html') 

    def test_filtered_consume_records_list(self):
        #-------------Testing filtered reservation list view-------------------------                        
        login = self.client.login(username=217426, password='Bhanu#1149') 
        create_inventory(username = 217426, free_stock = False,seed_qty=100) 
        do_reservation(username = 217426, reserv_qty_rule=2)
        consume_all(username = 217426)
        #-------------Testing issues  filter view with 1 consume recored-------------------------  
        for i in range(10):                      
            response = self.client.get(reverse('issue-filter', kwargs={"pk":i+1}))
            self.assertEqual(1, len(response.context["stock_issues"]))

        do_reservation(username = 217426, reserv_qty_rule=2) #creating second reservations
        consume_all(username = 217426)                 #creating second consume record
        #-------------Testing issues  filter view with 2 consume recored-------------------------                        
        for i in range(10):
            response = self.client.get(reverse('issue-filter', kwargs={"pk":i+1}))
            self.assertEqual(2, len(response.context["stock_issues"]))

        do_reservation(username = 217426, reserv_qty_rule=2) #creating 3rd reservations
        consume_all(username = 217426)                 #creating 3rd consume record
        #-------------Testing issues  filter view with 3 consume recored-------------------------                        
        for i in range(10):
            response = self.client.get(reverse('issue-filter', kwargs={"pk":i+1}))
            self.assertEqual(3, len(response.context["stock_issues"]))


        do_reservation(username = 217426, reserv_qty_rule=2) #creating 4 reservations
        consume_all(username = 217426)                 #creating 4 consume record
        do_reservation(username = 217426, reserv_qty_rule=2) #creating 5 reservations
        consume_all(username = 217426)                 #creating 5 consume record        
        #-------------Testing issues  filter view with 3 consume recored-------------------------                        
        for i in range(10):
            response = self.client.get(reverse('issue-filter', kwargs={"pk":i+1}))
            self.assertEqual(5, len(response.context["stock_issues"]))

class addLocationTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_test_user(username=217426, password="Bhanu#1149", first_name='bhanu1', last_name='valluri1') 

    def test_view_redirect_without_user_logged_in(self):
         #-------------Store loc add------------------------                        
        response = self.client.get('/matmgmt/storeloc/add')
        self.assertEqual(response.status_code, 302)       
        self.assertRedirects(response, '/accounts/login/?next=/matmgmt/storeloc/add')

        response = self.client.get(reverse('add-location'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/matmgmt/storeloc/add')  
    
    def test_view_with_user_loggedin(self):
        #-------------Store loc add------------------------                        
        login = self.client.login(username=217426, password='Bhanu#1149') 

        response = self.client.get(reverse('add-location'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'matmgmt/add_location.html') 

    def test_post_request_to_add_location_form(self):
        #-------------Store loc add------------------------                        
        login = self.client.login(username=217426, password='Bhanu#1149') 

        response = self.client.post(reverse('add-location'),data={"primary_loc" : "test_form_view"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual("test_form_view", StoreLocation.objects.filter(id=1)[0].primary_loc)

    def test_to_restriction_while_adding_same_location_second_time(self):
        #-------------Store loc add------------------------                        
        login = self.client.login(username=217426, password='Bhanu#1149') 

        response = self.client.post(reverse('add-location'),data={"primary_loc" : "test_form_view"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual("test_form_view", StoreLocation.objects.filter(id=1)[0].primary_loc)

        #adding same location again
        response = self.client.post(reverse('add-location'),data={"primary_loc" : "test_form_view"})
        self.assertEqual(response.status_code, 200)#checking to stay on same page with error
        self.assertFormError(response, "form", 'primary_loc', 'Location Already exists. Close Window')

class signup_form_Test(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_test_user(username=217427, password="Bhanu#1149", first_name='bhanu1', last_name='valluri1') 
    
    def test_signup_form_get_req_test(self):
        #-------------sign up view test------------------------                        
        response = self.client.get('/matmgmt/signup')
        self.assertEqual(response.status_code, 200)       
        self.assertTemplateUsed(response, 'registration/signup.html')

        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_signup_form_post_req_test(self):
        response = self.client.post(reverse('signup'), data={"username" : 217426,
                                                             "password" : "Bhanu#1149",
                                                             "confirm_password" : "Bhanu#1149",
                                                             "email" : "bhanuseshukumar@bel.net",
                                                             "first_name" :"bhanu",
                                                             "last_name" : "valluri"})
        self.assertRedirects(response, reverse("login"))

    def test_signup_form_post_req_with_unequal_passwords(self):
        response = self.client.post(reverse('signup'), data={"username" : 217426,
                                                             "password" : "Bhanuu#1149",
                                                             "confirm_password" : "Bhanu#1149",
                                                             "email" : "bhanuseshukumar@bel.net",
                                                             "first_name" :"bhanu",
                                                             "last_name" : "valluri"})
        self.assertFormError(response,'form','confirm_password', 'Passwords not matching')

    def test_signup_form_post_req_with_prohibted_username(self):
        response = self.client.post(reverse('signup'), data={"username" : 123456,
                                                             "password" : "Bhanu#1149",
                                                             "confirm_password" : "Bhanu#1149",
                                                             "email" : "bhanuseshukumar@bel.net",
                                                             "first_name" :"bhanu",
                                                             "last_name" : "valluri"})
        self.assertFormError(response,'form','username', 'You are not authorized. Contact site Admin')

    def test_signup_form_post_req_with_existed_username(self):
        response = self.client.post(reverse('signup'), data={"username" : 217426,
                                                             "password" : "Bhanu#1149",
                                                             "confirm_password" : "Bhanu#1149",
                                                             "email" : "bhanuseshukumar@bel.net",
                                                             "first_name" :"bhanu",
                                                             "last_name" : "valluri"})
        response = self.client.post(reverse('signup'), data={"username" : 217426,
                                                             "password" : "Bhanu#1149",
                                                             "confirm_password" : "Bhanu#1149",
                                                             "email" : "bhanuseshukumar@bel.net",
                                                             "first_name" :"bhanu",
                                                             "last_name" : "valluri"})                                                             
        self.assertFormError(response,'form','username', 'User already exist')




#---------------------helper functions------------------------------
def create_material_master_table(items_count, start_bel_part_no, start_mpn, start_description, user):
    # Create material master records for tests
    bel_part_number = start_bel_part_no
    for part_master_id in range(items_count):
        part_number_ins = BelPartNumber.objects.create(belPartNo = bel_part_number + part_master_id)
        part_number_ins.save()
        part_master_ins = PartMaster.objects.create(
            user = User.objects.get(username = user),
            belPartNo = part_number_ins,
            mpn = start_mpn + str(part_master_id) ,
            description = start_description + str(part_master_id)
        )
        part_master_ins.save()

def create_test_user(username, password, first_name, last_name):
        new_user = User.objects.create_user(username=username, password=password)
        new_user.first_name= first_name
        new_user.last_name = last_name
        new_user.save()

def create_primary_loc(start_location , count, username ):
    user = User.objects.get(username = username)
    for i in range(count):
        store = StoreLocation.objects.create(user = user, primary_loc = start_location+str(i))
        store.save()

def create_inventory(username, free_stock, seed_qty = 10):
    parts = PartMaster.objects.all()
    user = User.objects.get(username = username)
    primary_loc = StoreLocation.objects.all()[0]

    for i in range(len(parts)):
        inventory_ins = Inventory.objects.create(
                                                    owner = user,
                                                    partMaster = parts[i],
                                                    qty = i+seed_qty,
                                                    storeLoc = primary_loc,
                                                    secondary_loc = 'secondary_loc'+str(i),
                                                    free_stock = free_stock,
                                                    comment = "comment" + str(i)
        )
        inventory_ins.save()



def do_reservation(username,reserv_qty_rule=1):
    user = User.objects.get(username=username)
    inventory_list  = Inventory.objects.filter(owner = user )
    i = 0
    for i in range(len(inventory_list)):
        if (reserv_qty_rule == 2):
            reserv_qty = 1
        else:
            reserv_qty = i+1
        reservation_ins = Reservation.objects.create(
                                                        user = user,
                                                        inventory = inventory_list[i],
                                                        reservedQty = reserv_qty,
                                                        comment = 'reserved' + str(i),
                                                        consumed = False

        )
        inventory_list[i].qty = inventory_list[i].qty - (reserv_qty)
        inventory_list[i].save()        
        reservation_ins.save()
#consumes alternative reservations of a user
def consume(username):
    user = User.objects.get(username=username)
    reservations_list = Reservation.objects.filter(user = user)
    consume_flag = 0
    for i in range(len(reservations_list)):
        if(consume_flag == 0):
            if(reservations_list[i].consumed != True):
                reservations_list[i].consumed = True
                reservations_list[i].save()
                issue_obj = StockIssue.objects.create(reservation = reservations_list[i] , comment = 'test issue'+str(i))
                issue_obj.save()
                consume_flag =1
        else:
            if(reservations_list[i].consumed != True):
                consume_flag = 0
def consume_all(username):
    user = User.objects.get(username=username)
    reservations_list = Reservation.objects.filter(user = user)
    consume_flag = 0
    for i in range(len(reservations_list)):
        if(reservations_list[i].consumed != True):
            reservations_list[i].consumed = True
            reservations_list[i].save()
            issue_obj = StockIssue.objects.create(reservation = reservations_list[i] , comment = 'test issue'+str(i))
            issue_obj.save()
