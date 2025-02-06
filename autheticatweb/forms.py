from django import forms
from .models import Sale, Purchase

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['sale_to', 'quantity', 'measurement_unit', 'product', 'category', 'serial_no','rms_id', 'box_type', 'date', 'verified_by', 'description']
    
    # Optionally, you can manually customize widgets here, like setting 'readonly' for category if needed
    # Example:
    category = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly', 'placeholder': 'It will be auto selected on the basis of your product'}), required=False)
    serial_no = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter serial numbers separated by comma or newline'}), required=True)
    verified_by= forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly', 'placeholder': 'The data will be saved according to your username.'}), required=False)
    description = forms.CharField(
    widget=forms.Textarea(attrs={'placeholder': 'Enter discription'}),
    required=False,
    initial='Thankyou' 
     
      # Default value set kiya
)
    rms_id = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter RMS IDs separated by comma or newline'}),
        required=False
    )




class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['purchased_from', 'quantity', 'measurement_unit', 'product', 'category', 'serial_no', 'rms_id','box_type', 'date', 'verified_by', 'description']
    
    # Optionally, you can manually customize widgets here, like setting 'readonly' for category if needed
    # Example:
    category = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly', 'placeholder': 'It will be auto selected on the basis of your product'}), required=False)
    serial_no = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter serial numbers separated by comma or newline'}), required=True)
    verified_by= forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly', 'placeholder': 'The data will be saved according to your username.'}), required=False)
    description = forms.CharField(
    widget=forms.Textarea(attrs={'placeholder': 'Enter discription'}),
    required=False,
    initial='Thankyou'  # Default value set kiya
)
    rms_id = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Enter RMS IDs separated by comma or newline'}),
        required=False
    )


from django import forms
from .models import Sale

class ReturnItemForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['serial_no']  # Sirf 'serial_no' field include karenge
        widgets = {
            'serial_no': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter Serial Number'
            }),
        }
