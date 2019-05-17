from django.shortcuts import render, HttpResponse, redirect
from django.db import connection, transaction
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import ExternalUsers,LoginMaster, ProjectMembers, Projects, ProjectToStageMapping, StageMaster, StageActivities
from .forms import ExternalRegistration, FileUpload, ActivityApproval, LoginForm, RegisterStudent, \
    LoginRegistrationForm, ProjectRegistration


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/app')
    else:
        form = UserCreationForm()

        args = {'form': form}
        return render(request, 'reg_ext_user.html', args)


def externalRegistration(request):
    if request.method == "POST":
        form = ExternalRegistration(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    form = ExternalRegistration()
    return render(request, 'reg_ext_user.html', {'form': form})

def viewExternalUser(request):
    extusr = ExternalUsers.objects.filter(ApprovalStatus=True)
    return render(request,'view_ext_user.html',locals())

def studentRegistration(request):
    if request.method == "POST":
        form = RegisterStudent(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    form = RegisterStudent()
    return render(request, 'reg_student.html', {'form': form})

def loginRegistration(request):

    if request.method == 'POST':
        form=LoginRegistrationForm(request.POST)
        print(form.errors)
        if form.is_valid():
            print(form.cleaned_data)
            id = form.cleaned_data['Login_ID']
            pwd=form.cleaned_data['Password']
            usertype=int(form.cleaned_data['User_Type'])
            uid =int(form.cleaned_data['User_ID'])
            cursor = connection.cursor()
            if usertype == 1:

                cursor.execute("INSERT INTO app_loginmaster ('LoginID','Password','DerivedUserFrom','StudentUserID','FacultyUserID','ExternalUserID','isActive') VALUES (%s,%s,%s,%s,%s,%s,%s)",
                               (str(id), str(pwd),usertype,uid,0,0,True))
                print(usertype)
                #form.save()
                transaction.commit()
                return HttpResponse("Student Registered successfully")
            if usertype == 2:

                cursor.execute("INSERT INTO app_loginmaster ('LoginID','Password','DerivedUserFrom','StudentUserID','FacultyUserID','ExternalUserID','isActive') VALUES (%s,%s,%s,%s,%s,%s,%s)",
                               (str(id), str(pwd),usertype,0,uid,0,True))
                print(usertype)
                #form.save()
                transaction.commit()
                return HttpResponse("Internal Faculty Registered successfully")
            if usertype == 3:

                cursor.execute("INSERT INTO app_loginmaster ('LoginID','Password','DerivedUserFrom','StudentUserID','FacultyUserID','ExternalUserID','isActive') VALUES (%s,%s,%s,%s,%s,%s,%s)",
                               (str(id), str(pwd),usertype,0,0,uid,True))
                #form.save()
                print(usertype)
                transaction.commit()
                return HttpResponse("External Faculty Registered successfully")

    form=LoginRegistrationForm()
    return render(request, 'reg_login.html', locals())

def registerProject(request):
    if request.method == "POST":
        form = ProjectRegistration(request.POST)
        if form.is_valid():
            #form.save()
            cursor = connection.cursor()
            CollegeID_id = form.cleaned_data["College_ID"].pk
            DepartmentID_id = form.cleaned_data["Department_ID"].pk
            ProcessID_id = form.cleaned_data["Process_ID"].pk
            TermID_id = form.cleaned_data["Term_ID"].pk
            TermLead = form.cleaned_data["Term_Lead"]
            ProjectName = form.cleaned_data["Project_Name"]
            Subject = form.cleaned_data["Subject"]
            Description = form.cleaned_data["Description"]
            InternalGuide_id = form.cleaned_data["Internal_Guide"].pk
            HOD_id = form.cleaned_data["HOD"].pk
            Principal_id = form.cleaned_data["Principal"].pk
            ExternalGuide_id = form.cleaned_data["External_Guide"].pk
            Dean_id = form.cleaned_data["Dean"].pk
            IsExternalProject = str(form.cleaned_data["Is_External_Project"])

            cursor.execute("INSERT INTO app_projects (CollegeID_id,DepartmentID_id,ProcessID_id,TermID_id,TermLead,ProjectName, Subject, Description, InternalGuide_id, HOD_id, Principal_id, ExternalGuide_id, Dean_id, IsExternalProject,Status) VALUES \
            (%s, %s, %s, %s, %s,%s,%s,%s,%s,%s, %s, %s, %s, %s,0)", (CollegeID_id,DepartmentID_id,ProcessID_id,TermID_id,TermLead,ProjectName, Subject, Description, InternalGuide_id, HOD_id, Principal_id, ExternalGuide_id, Dean_id, IsExternalProject))
            transaction.commit()
            row = cursor.execute("SELECT ProcessID_id FROM app_projects WHERE app_projects.ProcessID_id = ProcessID ")
            print(row.fetchone())
            return redirect('/app/studentDashboard')
    form = ProjectRegistration()
    return render(request, 'reg_project.html', {'form': form})

def studentDashboard(request):
    pid = Projects.objects.filter(TermLead = request.session['id']).values('ProjectID')
    print(pid)
    stuproj = []
        #pid_list.append(pid[0]['ProjectID'])
    #print(pid)
    stuproj = Projects.objects.filter(ProjectID__in = pid).only('CollegeID','ProjectName')
    #print('ProjectName: ',str(stuproj[0]).split(' ')[1])
    #print('CollegeID: ', str(stuproj[0]).split(' ')[0])
    #stuproj= Projects.objects.select_related('InternalGuide')
    #stuproj.LinkColumn('ProjectName')
    #print(stuproj['InternalGuide'])
    #print(stuproj)
    return render(request, 'student_dashboard.html', locals())


def stageDetails(request,id):
    pid = id
    stageid = ProjectToStageMapping.objects.filter(ProjectID = pid).values('StageID')
    stage = StageMaster.objects.filter(StageID__in = stageid)
    status1 = StageActivities.objects.filter(ProjectID=pid).filter( StageID__in=stageid)
    #print(status1)
    if request.method == 'POST':
        form = FileUpload(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            f = str(form.cleaned_data['ProjectID'])+'_'+str(form.cleaned_data['StageID'])+'_'+str(form.cleaned_data['File'])
            print(f)
            handle_uploaded_file(request.FILES['File'],f)
            from django.db import connection, transaction
            cursor = connection.cursor()
            cursor.execute("UPDATE app_stageactivities SET Status = '1' WHERE ProjectID_id = %s and StageID_id= %s",(str(pid), str(form.cleaned_data["StageID"].pk)))
            form.save()
            return HttpResponse("File uploaded successfully")
    form = FileUpload()


    return render(request,'stage_detail.html',locals())


def handle_uploaded_file(f,fn):
    namedest = 'app/upload/'+fn+'_'+f.name
    with open(namedest, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    #return namedest


def facultyDashboard(request):
    pid = Projects.objects.filter(InternalGuide = request.session['id']).values("ProjectID")
    stuproj = Projects.objects.filter(ProjectID__in=pid).only('CollegeID', 'ProjectName')
    return render(request,"faculty_dashboard.html",locals())

def externalFacultyDashboard(request):
    pid = Projects.objects.filter(ExternalGuide = 1).values("ProjectID")
    stuproj = Projects.objects.filter(ProjectID__in=pid).only('CollegeID', 'ProjectName')
    return render(request,"external_faculty_dashboard.html",locals())


def facultyApproval(request,id):
    pid = id
    stageid = ProjectToStageMapping.objects.filter(ProjectID=pid).values('StageID')
    stage = StageMaster.objects.filter(StageID__in=stageid)
    status1 = StageActivities.objects.filter(ProjectID=pid).filter(StageID__in=stageid)

    if request.method == 'POST':

        form = ActivityApproval(request.POST)
        print(form.errors)

        if form.is_valid():
            from django.db import connection, transaction
            cursor = connection.cursor()
            if form.is_valid():
                status = form.cleaned_data

                #Data modifying operation - commit required
                #print(status["StageID"].pk)
                cursor.execute("UPDATE app_stageactivities SET Status = %s WHERE ProjectID_id = %s and StageID_id= %s",(str(status["Status"]), str(pid), str(status["StageID"].pk)))
                transaction.commit()
                cursor.execute("UPDATE app_stageactivities SET Status = 0 WHERE ProjectID_id = %s and StageID_id = %s", (str(pid), str(status["StageID"].pk + 1)))
                transaction.commit()
    #        print(form.cleaned_data)
     #       form.save
                return HttpResponse("Status Changed")
    form=ActivityApproval()
    return render(request, 'stageApproval.html', locals())

def my_custom_sql(request,id):
    pid = id
    stageid = ProjectToStageMapping.objects.filter(ProjectID=pid).values('StageID')

    status1 = StageActivities.objects.filter(ProjectID=pid).filter(StageID__in=stageid)
    form = ActivityApproval(request.POST)
    from django.db import connection, transaction
    cursor = connection.cursor()
    if(form.is_valid()):
        status=form.cleaned_data["Status"]
    # Data modifying operation - commit required
    cursor.execute("UPDATE StageActivities SET Status = %s WHERE ProjectID = %s and StageID= %s", [status1,pid,stageid])
    transaction.commit_unless_managed()

    return render(request, 'stageApproval.html', locals())


def login(request):
    #username = id
    #passsword = pwd
    if request.method=='POST':
        form = LoginForm(request.POST)
        print(form.errors)
        if form.is_valid():
            id = form.cleaned_data['Login_ID']
            pwd = form.cleaned_data['Password']

            flag = LoginMaster.objects.filter(LoginID=id,Password=pwd)
            if flag:
                request.session['username'] = id
                role = LoginMaster.objects.filter(LoginID=id,Password=pwd).values("DerivedUserFrom")
                print(role[0]['DerivedUserFrom'])
                if role[0]['DerivedUserFrom'] == 1:
                    request.session['id'] = LoginMaster.objects.filter(LoginID=id,Password=pwd).values("StudentUserID")[0]["StudentUserID"]
                    return redirect('/app/studentDashboard')
                elif role[0]['DerivedUserFrom'] == 2:
                    request.session['id'] = LoginMaster.objects.filter(LoginID=id,Password=pwd).values("FacultyUserID")[0]["FacultyUserID"]
                    return redirect('/app/facultyDashboard')
                elif role[0]['DerivedUserFrom'] == 3:
                    request.session['id'] = LoginMaster.objects.filter(LoginID=id,Password=pwd).values("ExternalUserID")[0]["ExternalUserID"]
                    return redirect('/app/externalFacultyDashboard')

    form = LoginForm()
    return render(request, 'login.html', locals())

def logout(request):
    try:
        del request.session['username']
        del request.session['id']
    except:
        pass
    return redirect('/app/login')