from django import forms

from app.models import ExternalUsers, StageToFileMapping, StageActivities, Students, LoginMaster, Projects, \
    CollegeMaster, DepartmentMaster, ProcessMaster, TermMaster, FacultyMaster


class ExternalRegistration(forms.ModelForm):
    class Meta:
        model = ExternalUsers
        fields = ('ExternalUserName', 'EmailAddress', 'MobileNumber', 'Qualification', 'UserType', 'CompanyName',
                  'CurrentPosition',
                  'AreaOfInterest', 'Specialization')


class RegisterStudent(forms.ModelForm):
    class Meta:
        model = Students
        fields = ('StudentName', 'CollegeID', 'DepartmentID', 'ProgramID', 'StreamID', 'EnrollmentNumber', 'FirstName',
                  'MiddleName', 'LastName', 'EmailID')


class LoginRegistrationForm(forms.Form):
    Login_ID = forms.CharField()
    Password = forms.CharField(widget=forms.PasswordInput)
    User_Type = forms.ChoiceField(choices=((1, 'Student'), (2, 'Internal Faculty'), (3, 'External Faculty')))
    User_ID = forms.CharField()


class FileUpload(forms.ModelForm):
    class Meta:
        model = StageToFileMapping

        fields = ('ProjectID', 'FileName', 'File', 'FilePath', 'StageID', 'UploadedBy')
        widgets = {'ProjectID': forms.HiddenInput(), 'FileName': forms.HiddenInput(), 'StageID': forms.HiddenInput(),
                   'FilePath': forms.HiddenInput()}


class ActivityApproval(forms.ModelForm):
    class Meta:
        model = StageActivities
        fields = ('ProjectID', 'StageID', 'ActivityType', 'Status', 'ModifiedBy', 'CreatedBy')
        widgets = {'ProjectID': forms.HiddenInput(), 'ActivityType': forms.HiddenInput(),
                   'StageID': forms.HiddenInput(), 'CreatedBy': forms.HiddenInput(), 'ModifiedBy': forms.HiddenInput()}


class LoginForm(forms.Form):
    Login_ID = forms.CharField(max_length=11)
    Password = forms.CharField(widget=forms.PasswordInput())


class ProjectRegistration(forms.Form):
    College_ID = forms.ModelChoiceField(queryset=CollegeMaster.objects.all())
    Department_ID = forms.ModelChoiceField(queryset=DepartmentMaster.objects.all())
    Process_ID = forms.ModelChoiceField(queryset=ProcessMaster.objects.all())
    Term_ID = forms.ModelChoiceField(queryset=TermMaster.objects.all())
    Term_Lead = forms.IntegerField()
    Project_Name = forms.CharField(max_length=50)
    Subject = forms.CharField(max_length=50)
    Description = forms.CharField(max_length=200)
    Internal_Guide = forms.ModelChoiceField(queryset=FacultyMaster.objects.all().filter(RoleID=4))
    HOD = forms.ModelChoiceField(queryset=FacultyMaster.objects.all().filter(RoleID=3))
    Principal = forms.ModelChoiceField(queryset=FacultyMaster.objects.all().filter(RoleID=2))
    External_Guide = forms.ModelChoiceField(queryset=ExternalUsers.objects.all())
    Dean = forms.ModelChoiceField(queryset=FacultyMaster.objects.all().filter(RoleID=1))
    Is_External_Project = forms.BooleanField()

    #    fields = ('HOD','Principal','ExternalGuide','Dean','IsExternalProject')
