from datetime import date
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

# Create your models here.
class BelPartNumber(models.Model):
	#bel partnumber for maintaining part list
	belPartNo = models.CharField(max_length = 12, blank = False, help_text = "Enter 12 digit bel part number. If unknown use 999999999999", unique = True,verbose_name = "BEL PART NUMBER")

	def __str__(self):
		return f'{self.belPartNo}'

class PartMaster(models.Model):
	user = models.ForeignKey(User,on_delete = models.RESTRICT,null=True)

	belPartNo = models.ForeignKey('BelPartNumber',on_delete = models.RESTRICT,blank=False,help_text="Select bel part number or add new")
	
	mpn = models.CharField(max_length = 30,help_text = 'select mpn or add new')

	description = models.CharField(max_length = 50,help_text='select part description or add new')

	def __str__(self):
		return f'{self.belPartNo.belPartNo} {self.mpn} {self.description}'

class Inventory(models.Model):

	owner = models.ForeignKey(User,on_delete = models.RESTRICT,null= True)

	partMaster = models.ForeignKey("PartMaster",on_delete = models.RESTRICT,help_text="select the partnumber or add new")

	qty = models.PositiveIntegerField(blank=False,null=False,help_text='Enter the qty')

	storeLoc = models.ForeignKey("StoreLocation",on_delete = models.RESTRICT,blank=False,null=False,help_text='select or add a storage location for the inventary')

	secondary_loc = models.CharField(max_length = 30,blank=False,help_text="Enter slot/pack Number",default='default')

	creationDate = models.DateField(auto_now=False, auto_now_add=True)	#inventory created date

	modifiedDate = models.DateField(auto_now=True, auto_now_add=False)

	free_stock = models.BooleanField(verbose_name="Free Stock", default=False)

	comment = models.CharField(max_length = 100,blank= False,help_text='Add an optional remarks here for reference')


	def __str__(self):
		return f'{self.partMaster}'


class Reservation(models.Model):
	user = models.ForeignKey(User,on_delete = models.RESTRICT,null=True)

	inventory = models.ForeignKey("Inventory",on_delete = models.RESTRICT)

	reservedQty = models.PositiveIntegerField(blank=False,null=False)

	creationDate = models.DateField(auto_now=False, auto_now_add=True)	#inventory created date

	modifiedDate = models.DateField(auto_now=True, auto_now_add=False)

	comment = models.CharField(max_length = 100,blank= False,null=False,help_text='Add an optional remark for what it is reserved for easy reference')

	consumed = models.BooleanField(default= False)
	def __str__(self):
		return f'{self.inventory}'

class StoreLocation(models.Model):
	user = models.ForeignKey(User,on_delete = models.RESTRICT,null=True)

	primary_loc = models.CharField(max_length=30,blank=False,help_text="Enter cupboard or drawer number")

	def __str__(self):
		return f'{self.primary_loc}'



class StockIssue(models.Model):
	reservation = models.ForeignKey(Reservation,on_delete = models.RESTRICT)

	issueDate = models.DateField(auto_now=False, auto_now_add=True)	

	comment = models.CharField(max_length = 100,blank= False,null = False,help_text='Add an optional remark for where it is used for easy reference')

	def __str__(self):
		return f'{self.reservation}'
