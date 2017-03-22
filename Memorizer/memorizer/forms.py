from django import forms

class factForm(forms.Form):
    htmlprompt = forms.CharField(max_length=200)
    htmlanswer = forms.CharField(max_length=200)

class userForm(forms.Form):
    htmlusername = forms.CharField(max_length=200)
    htmlpassword = forms.CharField(max_length=200)

class learnForm(forms.Form):
    htmlresponse = forms.CharField(max_length=200)

class radioForm(forms.Form):
    htmlradio= forms.CharField(max_length=200)

