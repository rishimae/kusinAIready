from django import forms

class SignUpForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter your name'}))
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}))
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Valid PH number'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))
    repassword = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Re-enter your password'}))

    def clean_repassword(self):
        password = self.cleaned_data.get('password')
        repassword = self.cleaned_data.get('repassword')
        if password and repassword and password != repassword:
            raise forms.ValidationError("Passwords do not match")
        return repassword
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    
class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6, required=True, widget=forms.TextInput(attrs={'placeholder': 'Enter OTP'}))
    
class PhoneNumberForm(forms.Form):
    phone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number'}))

class VerificationCodeForm(forms.Form):
    code = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'placeholder': 'Enter the code'}))

class NewPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password'}))
    re_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Re-enter new password'}))

    def clean_re_password(self):
        new_password = self.cleaned_data.get('new_password')
        re_password = self.cleaned_data.get('re_password')
        if new_password and re_password and new_password != re_password:
            raise forms.ValidationError("Passwords do not match")
        return re_password
