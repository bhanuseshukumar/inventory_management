from django.shortcuts import render, get_object_or_404
from matmgmt.models import BelPartNumber, PartMaster, Inventory, Reservation, StoreLocation, StockIssue
from .forms import CreateMaterialMasterForm, AddStockForm, MakeReservationForm, IssueReservationForm, AddLocationForm, SignupForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from itertools import chain

# Create your views here.
@login_required
def index(request):
	context = {}
	return render(request, 'matmgmt/index.html', context=context)

@login_required
def inventoryListView(request):
	#read inventory from database
	
	inventory = Inventory.objects.all()
	reserv_qty = []
	for inventory_item in inventory:
		reserv_list = Reservation.objects.filter(inventory = inventory_item, consumed = False)
		qty = 0
		if reserv_list :
			for reservs in reserv_list:
				qty += reservs.reservedQty
		reserv_qty.append(qty) 
	context = {
		"inventory" : inventory,
		"reserv_qty" : reserv_qty,
	}
	return render(request, 'matmgmt/inventorylist.html', context=context)

#To add new material master record.
@login_required
def create_material_master(request):
	if( request.method == 'POST' ):
		#bound the form with POST data
		form = CreateMaterialMasterForm(request.POST)

		if form.is_valid() :
			exist_in_db = PartMaster.objects.filter(belPartNo__belPartNo__iexact = form.cleaned_data['BEL_PART_NUMBER'],
									  mpn__iexact = form.cleaned_data["MPN"],
									  description__iexact = form.cleaned_data['description'])
			look_up_db = BelPartNumber.objects.filter(belPartNo = form.cleaned_data['BEL_PART_NUMBER'])
			if look_up_db :
				bel_part_number_record = look_up_db[0]
			else:		
				bel_part_number_record = BelPartNumber( belPartNo = form.cleaned_data['BEL_PART_NUMBER'] )
				bel_part_number_record.save()	#First save the bel part number

			if(exist_in_db):
				form.add_error('MPN','part list already exist')
			else:
				bpn_queryset = BelPartNumber.objects.filter(belPartNo = form.cleaned_data['BEL_PART_NUMBER'])
			
				mpn_record = PartMaster( user = request.user, belPartNo = bpn_queryset[0], mpn = form.cleaned_data["MPN"], description = form.cleaned_data['description'])

				mpn_record.save() # Now save the mpn record

				return HttpResponseRedirect( reverse("material_master") )
	else:
		# create an empty form for a new get request.
		form = CreateMaterialMasterForm()

	context = {
		'form': form,
		}

	return render(request,"matmgmt/create_material_master_form.html", context)

@login_required
def show_material(request):
	part_master = PartMaster.objects.all()

	context ={
		"part_master" :part_master,
	}
	return render(request,'matmgmt/show_material.html',context)

@login_required
def add_stock(request,pk):
	part = get_object_or_404(PartMaster,pk=pk)

	if(request.method == "POST"):
		form = AddStockForm(request.POST)

		if form.is_valid():
			qty = form.cleaned_data["Quantity"]
			store_loc_pk = request.POST.get('Primary_Location')
			store_loc = StoreLocation.objects.filter(id=store_loc_pk)[0]
			secondary_location = form.cleaned_data["Secondary_Location"]
			comment = form.cleaned_data["Comment"]
			free_stock = form.cleaned_data["free_stock"]

			inventory_instance = Inventory( owner=request.user, 
											partMaster = part,
											qty = qty,
											storeLoc = store_loc,
											secondary_loc = secondary_location,
											comment = comment,
											free_stock = free_stock)
			inventory_instance.save()

			return HttpResponseRedirect(reverse("stock-list") )
	else:
		#create a empty form to render
		form = AddStockForm()

	context ={
		"part" : part,
		"form" : form,
	}
	return render(request,'matmgmt/add_stock.html',context)

@login_required
def reservationsListView(request):
	reservations = Reservation.objects.exclude(consumed = True)
	context = {
		"reservations" :reservations,
	}
	return render(request,'matmgmt/reservations_list.html',context)

@login_required
def add_reservation(request,pk):
	inventory = get_object_or_404(Inventory, pk=pk)

	if(request.method == "POST"):
		form = MakeReservationForm(request.POST)

		if form.is_valid():
			reservedQty = form.cleaned_data["quantity"]
			comment = form.cleaned_data["comment"]
			inventory = inventory
			reservation_instance = Reservation(user = request.user,
											   inventory = inventory,
											   reservedQty =reservedQty,
											   comment =  comment)
			
			if(str(request.user) != str(inventory.owner) and inventory.free_stock == False):
				form.add_error('quantity',"Your not the owner of this inventory")
			elif (reservedQty > inventory.qty):
				form.add_error('quantity',"reserved Qty is more than stock")				
			else:
				reservation_instance.save()
				inventory.qty = inventory.qty - reservedQty
				inventory.save()
				return HttpResponseRedirect(reverse("reservations-list") )			
	else:
		form = 	MakeReservationForm()	
	context ={
		"inventory" : inventory,
		"form" : form,
	}	
	return render(request,'matmgmt/add_reservation.html',context)

@login_required
def consume(request,pk):
	reservation = get_object_or_404(Reservation,pk=pk, consumed = False)

	if(request.method == "POST"):
		form = IssueReservationForm(request.POST)
		if form.is_valid():
			comment = form.cleaned_data["comment"]
			if(str(request.user) != str(reservation.user.username)):
				form.add_error('comment',"can't consume other users reservations")
			else:
				stockIssue_instace = StockIssue(reservation = reservation, comment = comment)
				stockIssue_instace.save()
				reservation.consumed = True
				reservation.save()
				return HttpResponseRedirect( reverse("issues-list") )			

	else:
		form = IssueReservationForm()
	
	context ={
		"form" : form,
		"reservation" : reservation,
	}
	return render(request, 'matmgmt/consume.html', context)

@login_required
def issuesListView(request):
	stock_issues = StockIssue.objects.all()

	context = {
		"stock_issues" : stock_issues,
	}
	return render(request, 'matmgmt/issue_list.html', context)

@login_required
def issueFilterView(request,pk):
	inventory = Inventory.objects.filter(id=pk)[0]
	context ={}
	reservations = Reservation.objects.filter(inventory = inventory, consumed = True)
	stock_issues = 0
	if(len(reservations) > 0 ):
		stock_issues = reservations[0].stockissue_set.all()
		if(len(reservations) > 1):
			for i in range (1,len(reservations)):
				issues = reservations[i].stockissue_set.all()
				stock_issues = list(chain(stock_issues, issues))
	context = {
		"stock_issues" : stock_issues,
	}
	return render(request, 'matmgmt/issue_list.html', context)

@login_required
def addLocation(request):
	if(request.method == 'POST'):
		form = AddLocationForm(request.POST)
		if form.is_valid():
			loc = form.cleaned_data["primary_loc"]
			loc_prsnt = StoreLocation.objects.filter(primary_loc = loc)
			if loc_prsnt :
				form.add_error('primary_loc',"Location Already exists. Close Window")
			else:
				storeloc_instance = StoreLocation(user = request.user, primary_loc = loc )
				storeloc_instance.save()
				return HttpResponse('Location Successfully added. Close Window')

	else:
		form = AddLocationForm()
	context = {
		"form" : form,
	}
	return render(request,'matmgmt/add_location.html',context)


@login_required
def material_edit(request,pk):
	part_master = get_object_or_404(PartMaster,id=pk)

	if(request.method == "POST"):
		form = CreateMaterialMasterForm(request.POST)
		if form.is_valid():
			if(part_master.belPartNo.belPartNo != form.cleaned_data["BEL_PART_NUMBER"]):
				form.add_error("BEL_PART_NUMBER", "BPN change not allowed. Only mpn & description changes are allowed")
			else:
				part_master.mpn = form.cleaned_data["MPN"]
				part_master.description = form.cleaned_data["description"]
				part_master.save()
				return HttpResponseRedirect( reverse("material_master") )			
	else:		
		form = CreateMaterialMasterForm(initial = { 'BEL_PART_NUMBER' : part_master.belPartNo.belPartNo ,
													'MPN' : part_master.mpn,
													'description' : part_master.description,})
	context = {
		"form" : form,
	}
	return render(request, 'matmgmt/material_edit.html', context)


@login_required
def material_delete(request,pk):
	part_master = get_object_or_404(PartMaster,id=pk)
	stock_list = []
	context = {}
	form = {'BEL_PART_NUMBER' : part_master.belPartNo.belPartNo ,
		'MPN' : part_master.mpn,
		'description' : part_master.description,
		}
	if(request.method == "POST"):
		stock_list = part_master.inventory_set.all()
		if stock_list :
			stock_list = stock_list
			context["stock_list"]	= stock_list
		else:
			part_master.delete()
			return HttpResponseRedirect( reverse("material_master") )
	else:		
		form = form

	context["form"] = form
	return render(request, 'matmgmt/material_delete.html', context)	


@login_required
def stock_edit(request,pk):
	inventory = get_object_or_404(Inventory, id = pk)
	if(request.method == "POST"):
		form = AddStockForm(request.POST)

		if form.is_valid():
			qty = form.cleaned_data["Quantity"]
			store_loc_pk = request.POST.get('Primary_Location')
			store_loc = StoreLocation.objects.filter(id=store_loc_pk)[0]
			secondary_location = form.cleaned_data["Secondary_Location"]
			comment = form.cleaned_data["Comment"]
			if(str(request.user) != str(inventory.owner.username) and inventory.free_stock == False):
				form.add_error('Quantity',"You are not the owner of the inventory")
			else:
				inventory.qty = qty
				inventory.storeLoc = store_loc
				inventory.secondary_loc = secondary_location
				inventory.comment = comment
				inventory.free_stock = form.cleaned_data["free_stock"]
				inventory.save()
				return HttpResponseRedirect(reverse("stock-list") )
	else:
		#create a empty form to render
		form = AddStockForm(initial={	"Quantity" : inventory.qty,
									 	"Primary_Location" : inventory.storeLoc.id ,
									 	"Secondary_Location" : inventory.secondary_loc,
									 	"Comment" : inventory.comment,
										 "free_stock" :inventory.free_stock,
									 	} )

	context ={
		"inventory" : inventory,
		"form" : form,
	}
	return render(request,'matmgmt/stock_edit.html',context)

@login_required
def stock_delete(request,pk):
	inventory = get_object_or_404(Inventory,id=pk)
	reserv_list = []
	context = {}
	form = {'BEL_PART_NUMBER' : inventory.partMaster.belPartNo.belPartNo ,
		'MPN' : inventory.partMaster.mpn,
		'description' : inventory.partMaster.description,
		"quantity" : inventory.qty,
		}
	if(request.method == "POST"):
		reserv_list = inventory.reservation_set.all()
		if(str(request.user) != str(inventory.owner.username)):
			context["error_delete"] = "You are not the owner of the inventory"
		elif reserv_list :
			reserv_list = reserv_list
			context["reserv_list"]	= reserv_list
		else:
			inventory.delete()
			return HttpResponseRedirect( reverse("stock-list") )
	else:		
		form = form

	context["form"] = form
	return render(request, 'matmgmt/stock_delete.html', context)	
@login_required
def reservation_edit(request,pk):
	reservation = get_object_or_404(Reservation,id=pk)
	inventroy_ins = get_object_or_404(Inventory,id= reservation.inventory.id)
	if(request.method == "POST"):
		form = MakeReservationForm(request.POST)

		if form.is_valid():
			reservedQty = form.cleaned_data["quantity"]
			comment = form.cleaned_data["comment"]
			inventroy_ins.qty += reservation.reservedQty

			if(str(request.user) != str(reservation.user.username)):
				form.add_error('quantity',"Can't edit other users reservations")			
			elif (reservedQty > inventroy_ins.qty):
				form.add_error('quantity',"reserved Qty is more than stock")							
			else:
				reservation.comment = comment
				reservation.reservedQty = reservedQty
				inventroy_ins.qty = inventroy_ins.qty - reservedQty
				reservation.save()
				inventroy_ins.save()
				return HttpResponseRedirect(reverse("reservations-list") )			
	else:
		form = 	MakeReservationForm(initial={	"quantity" : reservation.reservedQty,
												"comment" : reservation.comment,

			})	
	context ={
		"inventory" : inventroy_ins,
		"form" : form,
	}	
	return render(request,'matmgmt/reservations_edit.html',context)	

@login_required
def reservation_delete(request,pk):
	reservation = get_object_or_404(Reservation,id=pk)
	inventroy_ins = get_object_or_404(Inventory,id= reservation.inventory.id)
	consume_records = StockIssue.objects.filter( reservation = reservation ) # didn't use get_object_or_404 purposefully since it inhibits user deleting reservations with out consumption records

	context = {}
	form = {'BEL_PART_NUMBER' : inventroy_ins.partMaster.belPartNo.belPartNo ,
		'MPN' : inventroy_ins.partMaster.mpn,
		'description' : inventroy_ins.partMaster.description,
		"quantity" : reservation.reservedQty,
		}
	if(request.method == "POST"):
		if(str(request.user) != str(reservation.user.username)):
			context["error_delete"] = "Can't delete others users reservations"
		elif(len(consume_records) != 0):
			context["error_delete"] = "Can't delete reservations with consume records"
		else:
			inventroy_ins.qty += reservation.reservedQty
			reservation.delete()
			inventroy_ins.save()
			return HttpResponseRedirect(reverse("reservations-list") )			
	else:		
		form = form

	context["form"] = form
	return render(request, 'matmgmt/reservations_delete.html', context)

@login_required
def issue_edit(request,pk):
	issue = get_object_or_404(StockIssue, id=pk)
	reservation = get_object_or_404(Reservation, id=issue.reservation.id)

	if(request.method == "POST"):
		form = IssueReservationForm(request.POST)
		if form.is_valid():
			comment = form.cleaned_data["comment"]
			if(str(request.user) != str(reservation.user.username)):
				form.add_error('comment',"Can't edit other users consume records")				
			else:
				issue.comment = comment
				issue.save()
				return HttpResponseRedirect( reverse("issues-list") )			

	else:
		form = IssueReservationForm(initial = {
												'comment' : issue.comment,
			})
	
	context ={
		"form" : form,
		"reservation" : reservation,
	}
	return render(request, 'matmgmt/issue_edit.html', context)

@login_required
def issue_delete(request,pk):
	issue = get_object_or_404(StockIssue, id=pk)
	reservation = get_object_or_404(Reservation, id=issue.reservation.id)
	inventroy_ins = get_object_or_404(Inventory,id= reservation.inventory.id)
	context = {}
	form = {'BEL_PART_NUMBER' : inventroy_ins.partMaster.belPartNo.belPartNo ,
		'MPN' : inventroy_ins.partMaster.mpn,
		'description' : inventroy_ins.partMaster.description,
		"quantity" : reservation.reservedQty,
		}
	if(request.method == "POST"):
		if(str(request.user) != str(reservation.user.username)):
			context["error_delete"] = "Can't delete other users consume records"		
		else:
			issue.delete()
			reservation.delete()
			reservation_set_for_inventory =  inventroy_ins.reservation_set.all()
			if(inventroy_ins.qty == 0 and not reservation_set_for_inventory):
				inventroy_ins.delete()
			return HttpResponseRedirect(reverse("issues-list") )			
	else:		
		form = form
	context["form"] = form
	return render(request, 'matmgmt/issue_delete.html', context)

@login_required
def reservationsFilterView(request,pk):
	inventory = get_object_or_404(Inventory, id=pk)
	reservations = Reservation.objects.filter(inventory = inventory, consumed = False)

	context = {
		"reservations" :reservations,
	}
	return render(request,'matmgmt/reservations_list.html',context)

def signupView(request):
	allowed_users = [217426, 217427, 217428, 217429]
	valid =1
	if(request.method == "POST"):
		form = SignupForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data["username"]
			email = form.cleaned_data["email"]
			password = form.cleaned_data["password"]
			#checking if user name is valid 6 digit number
			if(len(str(username)) != 6):
				form.add_error('username','Not a valid staffnumber')
				valid =0
			#checking if user name is already exists.
			user = User.objects.filter(username = username)	
			if(len(user) != 0):
				form.add_error('username', 'User already exist')
				valid = 0
			#checking if is part of allowed list of users
			if(username in allowed_users):
				print(username)
			else:
				valid = 0
				form.add_error('username', 'You are not authorized. Contact site Admin')
			#check if confirm password &  password both same
			cnf_password = form.cleaned_data["confirm_password"]
			if(cnf_password != password):
				valid = 0
				form.add_error("confirm_password","Passwords not matching")
				
			if(valid == 1):
				user_ins = User.objects.create_user(username, email, password)
				user_ins.save()
				user_ins.first_name = form.cleaned_data["first_name"]
				user_ins.first_name = form.cleaned_data["last_name"]
				user_ins.save()
				return HttpResponseRedirect( reverse("login") )

	else:
		form = SignupForm()
	
	context ={
		"form" : form,
	}
	return render(request, 'registration/signup.html', context)

def test(request):
	context={}
	return render(request, 'matmgmt/test.html',context)