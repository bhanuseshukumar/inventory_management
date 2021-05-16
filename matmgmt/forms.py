from django import forms
from matmgmt.models import BelPartNumber, PartMaster, Inventory, Reservation, StoreLocation, StockIssue
import re
from django.core.exceptions import ValidationError

def validate_bpn(value):
	# regular expression to check bpn don't have non digit characters in it.
	non_digit_char_re = re.compile( r'[^0-9]' )

	list_of_chars = non_digit_char_re.findall(value)
	#check if any chars other than digits
	if list_of_chars :
		raise ValidationError('Only enter 12 digit part Number', params={'value': value})
	else:
		if len(value) != 12 :
			raise ValidationError('BEL PART NUMBER must be 12 digits', params={'value': value})
		 
def validate_quantity(value):
	qty = value
	# Qty is invalid if it negative or zero
	if(qty <= 0):
		raise ValidationError("Enter positive non zero value", params={'value': value})

class CreateMaterialMasterForm(forms.Form):
	BEL_PART_NUMBER = forms.CharField(max_length = 12, help_text = "Enter 12 digit bel part number. If unknown use 999999999999", validators=[validate_bpn])

	MPN	= forms.CharField(max_length = 30,help_text = 'Enter the manufacturer part number')

	description = forms.CharField(max_length = 50,help_text='Enter part description')


class AddStockForm(forms.Form):

	Quantity = forms.IntegerField(help_text='Enter the qty', validators=[validate_quantity])

	Primary_Location = forms.ModelChoiceField(queryset = StoreLocation.objects.all(),help_text = 'Enter the Primary location')

	Secondary_Location = forms.CharField(max_length = 30, help_text="Enter slot/pack Number")

	Comment  = forms.CharField(max_length = 100, help_text='Add an optional comment here for reference')

	free_stock = forms.BooleanField( required=False, help_text = 'Check-To make it free stock. Uncheck- For Project Stock')



class MakeReservationForm(forms.Form):
	
	quantity = forms.IntegerField(help_text='Enter the qty', validators=[validate_quantity])

	comment  = forms.CharField(max_length = 100, help_text='Add an optional comment here for reference')



class IssueReservationForm(forms.Form):
	
	comment  = forms.CharField(max_length = 100, help_text='Add an optional comment here for reference')

class AddLocationForm(forms.Form):
	primary_loc = forms.CharField(max_length=30,help_text="Enter cupboard or drawer number")

class SignupForm(forms.Form):
	username = forms.IntegerField(help_text='Enter the Staff Number')
	password = forms.CharField(max_length=30,help_text="Enter Password", widget=forms.PasswordInput)
	confirm_password = forms.CharField(max_length=30,help_text="Confirm Password", widget=forms.PasswordInput)
	email	= forms.EmailField(help_text = "Enter intranet(bel.net) email Id")
	first_name = forms.CharField(max_length=30,help_text='Enter your First Name')
	last_name =  forms.CharField(max_length=30,help_text='Enter your Last Name')

	def clean_password(self):
		password = self.cleaned_data["password"]
		#check mininum password length 8
		if(len(str(password)) < 8):
				print(password)
				raise ValidationError("Must have minimum length of 8")
		
		#check for at least one digit in password
		digit_re = re.compile(r'\d+')
		digits = len(digit_re.findall(password))
		if(digits == 0):
			raise ValidationError("Must contain at least one digit")
		
		#check for atleast on capital letter
		capital_re = re.compile(r'[A-Z]+')
		no_cap_letters = len( capital_re.findall(password))
		if(no_cap_letters == 0):
			raise ValidationError("Must have atleast one capital letter")
		
		#check for atleast on special character
		special_re = re.compile(r'[@#$%^&+=]+')
		no_special_chars = len( special_re.findall(password))
		if(no_special_chars == 0):
			raise ValidationError("Must contain any one of special chars @ # $ % ^ & + =")

		return password

	def clean_email(self):
		email = str(self.cleaned_data["email"])
		email_re = re.compile(r'([a-z]{4,})@bel.net')
		valid = len(email_re.findall(email))
		if(valid !=1):
			raise ValidationError('Not a valid bel.net email address')
		return email
		