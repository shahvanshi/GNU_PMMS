from django.db import models

# Create your models here.
from django.db import models


# Create your models here.
class LoginMaster(models.Model):
    UserID = models.AutoField(primary_key=True)
    LoginID = models.CharField(max_length=50)
    Password = models.CharField(max_length=200)
    DerivedUserFrom = models.IntegerField(choices=((1, 'Student'), (2, 'Internal Faculty'), (3, 'External Faculty')))
    FacultyUserID = models.IntegerField(default=None)
    ExternalUserID = models.IntegerField(default=None)
    StudentUserID = models.IntegerField(default=None)
    IsActive = models.BooleanField(default=True)

    def __str__(self):
        return str(self.UserID)


class CollegeMaster(models.Model):
    CollegeID = models.AutoField(primary_key=True)
    CollegeCode = models.CharField(max_length=50, null=True)
    CollegeName = models.CharField(max_length=50, null=True)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    ModifiedDate = models.DateTimeField(auto_now=True)
    CreatedBy = models.IntegerField()
    ModifiedBy = models.IntegerField()

    def __str__(self):
        return self.CollegeName


class DepartmentMaster(models.Model):
    DepartmentID = models.AutoField(primary_key=True)
    collegeID = models.ForeignKey(CollegeMaster, on_delete=models.CASCADE)
    DepartmentCode = models.CharField(null=False, max_length=50)
    DepartmentName = models.CharField(null=False, max_length=100)
    CreatedBy = models.IntegerField()
    ModifiedBy = models.IntegerField()

    def __str__(self):
        return str(self.DepartmentID) + self.DepartmentName


class ProgramMaster(models.Model):
    ProgramID = models.AutoField(primary_key=True)
    ProgramName = models.CharField(max_length=50)
    ProgramAlias = models.CharField(max_length=50)
    IsActive = models.BooleanField(default=True)
    CreatedBy = models.IntegerField()
    ModifiedBy = models.IntegerField()
    CreatedDate = models.DateTimeField(auto_now_add=True)
    ModifiedDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.ProgramID) + " " + self.ProgramName


class StreamMaster(models.Model):
    StreamID = models.AutoField(primary_key=True)
    StreamName = models.CharField(max_length=50)
    StreamAlias = models.CharField(max_length=50)
    ProgramID = models.ForeignKey(ProgramMaster, on_delete=models.CASCADE)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    ModifiedDate = models.DateTimeField(auto_now=True)
    CreatedBy = models.IntegerField()
    ModifiedBy = models.IntegerField()

    def __str__(self):
        return self.StreamName + " " + self.StreamAlias


class RoleMaster(models.Model):
    RoleID = models.AutoField(primary_key=True)
    RoleName = models.CharField(max_length=50, unique=True)
    CreatedBy = models.IntegerField()
    ModifiedBy = models.IntegerField()
    CreatedDate = models.DateTimeField(auto_now_add=True)
    ModifiedDate = models.DateTimeField(auto_now=True)
    IsActive = models.BooleanField(default=True)

    def __str__(self):
        return self.RoleName


class FacultyMaster(models.Model):
    FacultyID = models.AutoField(primary_key=True)
    FacultyName = models.CharField(max_length=50)
    EmailAddress = models.EmailField()
    Designation = models.CharField(max_length=50)
    RoleID = models.ForeignKey(RoleMaster, on_delete=models.CASCADE)
    CollegeID = models.ForeignKey(CollegeMaster, on_delete=models.CASCADE)
    DepartmentID = models.ForeignKey(DepartmentMaster, on_delete=models.CASCADE)
    ProgramID = models.ForeignKey(ProgramMaster, on_delete=models.CASCADE)
    StreamID = models.ForeignKey(StreamMaster, on_delete=models.CASCADE)
    IsActive = models.BooleanField(default=True)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    ModifiedDate = models.DateTimeField(auto_now=True)
    CreatedBy = models.IntegerField()
    ModifiedBy = models.IntegerField()

    def __str__(self):
        return str(self.FacultyID) + " " + str(self.FacultyName)


class TermMaster(models.Model):
    TermID = models.AutoField(primary_key=True)
    TermName = models.CharField(max_length=50)
    TermAlias = models.CharField(max_length=50)
    ProgramID = models.ForeignKey(ProgramMaster, on_delete=models.CASCADE)
    StreamID = models.ForeignKey(StreamMaster, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.TermID) + self.TermName


class ProcessMaster(models.Model):
    ProcessID = models.AutoField(primary_key=True)
    ProcessName = models.CharField(max_length=50)
    ProjRegToBeDoneBy = models.IntegerField(choices=((1, 'Student'), (2, 'Faculty')))
    ProjHasToBe = models.IntegerField(choices=((1, 'Always Internal'), (2, 'Always External'), (3, 'Either')))
    ProjShallBeDoneBy = models.IntegerField(choices=((1, 'Individual'), (2, 'Team'), (3, 'Either')))
    NumberOfStages = models.IntegerField()
    InternalFaculty_Involvement_Needed = models.BooleanField(default=True)
    FacultyRequired = models.BooleanField(default=True)
    HODRequired = models.BooleanField()
    PrincipalRequired = models.BooleanField()
    PanelReviewRequired = models.BooleanField()
    ExternalGuideNeeded = models.BooleanField()
    FundingToBeProvided = models.BooleanField()
    ExpenseTrakingRequired = models.BooleanField()
    MaterialToBeProvided = models.BooleanField()
    FinalSubmissionEvaluated = models.BooleanField()
    Evaluator_Role = models.ForeignKey(RoleMaster, on_delete=models.CASCADE)
    Process_Reviewed = models.BooleanField(default=False)
    Process_Reviewed_By = models.IntegerField()
    Created_By = models.IntegerField()
    Modified_By = models.IntegerField()
    CreatedDate = models.DateTimeField(auto_now_add=True)
    ModifiedDate = models.DateTimeField(auto_now=True)
    IsActive = models.BooleanField(default=True)

    def __str__(self):
        return str(self.ProcessID) + " " + self.ProcessName


class StageMaster(models.Model):
    StageID = models.AutoField(primary_key=True)
    ProcessID = models.ForeignKey(ProcessMaster, on_delete=models.CASCADE)
    StageName = models.CharField(max_length=50)
    StageSeq = models.IntegerField()
    ReqAnyUpload = models.BooleanField(default=True)
    ActivityUpload = models.CharField(max_length=50)
    ActivityType = models.IntegerField(choices=((1, 'Team'), (2, 'Individual'), (3, 'Either')))
    RequireAnyApproval = models.BooleanField(default=True)
    InternalApprovalNeeded = models.BooleanField(default=True)
    InternalApprovalType = models.IntegerField()
    IsWorkflowDriven = models.BooleanField(default=True)
    ExternalGuideApprovalNeeded = models.BooleanField(default=True)
    MentorApprovalNeeded = models.BooleanField(default=True)
    PanelApprovalNeeded = models.BooleanField(default=True)
    DeanApprovalNeeded = models.BooleanField(default=True)
    RequireNoDueCertificate = models.BooleanField(default=True)
    CompletionCertiIssuedForStage = models.BooleanField(default=True)
    IsActive = models.BooleanField(default=True)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    ModifiedDate = models.DateTimeField(auto_now=True)
    CreatedBy = models.IntegerField()
    ModifiedBy = models.IntegerField()

    def __str__(self):
        return self.StageName


class ExternalUsers(models.Model):
    ExternalUserID = models.AutoField(primary_key=True)
    ExternalUserName = models.CharField(max_length=50)
    EmailAddress = models.EmailField()
    Qualification = models.CharField(max_length=50)
    Specialization = models.CharField(max_length=50)
    CompanyName = models.CharField(max_length=50)
    CurrentPosition = models.CharField(max_length=50)
    AreaOfInterest = models.CharField(max_length=50)
    MobileNumber = models.CharField(max_length=15)
    UserType = models.IntegerField(choices=((1, "External Guide"), (2, "External Mentor")))  # external guide, mentor
    ApprovalStatus = models.BooleanField(default=False)  # rejected?
    IsActive = models.BooleanField(default=True)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    ActionTakenBy = models.IntegerField()

    def __str__(self):
        return str(self.ExternalUserID) + " " + str(self.ExternalUserName)


class Projects(models.Model):
    ProjectID = models.AutoField(primary_key=True)
    CollegeID = models.ForeignKey(CollegeMaster, on_delete=models.CASCADE)
    DepartmentID = models.ForeignKey(DepartmentMaster, on_delete=models.CASCADE)
    ProcessID = models.ForeignKey(ProcessMaster, on_delete=models.CASCADE)
    TermID = models.ForeignKey(TermMaster, on_delete=models.CASCADE)
    ProjectName = models.CharField(max_length=50)
    Subject = models.CharField(max_length=50)
    Description = models.CharField(max_length=200)
    InternalGuide = models.ForeignKey(FacultyMaster, on_delete=models.CASCADE, related_name="InternalGuide")
    HOD = models.ForeignKey(FacultyMaster, on_delete=models.CASCADE, related_name="HOD")
    Principal = models.ForeignKey(FacultyMaster, on_delete=models.CASCADE, related_name="Principal")
    ExternalGuide = models.ForeignKey(ExternalUsers, on_delete=models.CASCADE)
    Dean = models.ForeignKey(FacultyMaster, on_delete=models.CASCADE, related_name="Dean")
    IsExternalProject = models.BooleanField()
    TermLead = models.IntegerField(default=0)
    Status = models.IntegerField(choices=((1, 'Pending'), (2, 'Approved'), (3, 'Rejected')), default=2)

    IsActive = models.BooleanField(default=True)
    CreatedBy = models.IntegerField(default=1)
    ModifiedBy = models.IntegerField(default=1)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    ModifiedDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.ProjectID) + self.ProjectName


class StageToFileMapping(models.Model):
    uploadID = models.AutoField(primary_key=True)
    ProjectID = models.ForeignKey(Projects, on_delete=models.CASCADE)
    StageID = models.ForeignKey(StageMaster, on_delete=models.CASCADE)
    File = models.FileField()
    FileName = models.CharField(max_length=200)
    FilePath = models.CharField(max_length=200)
    UploadedBy = models.CharField(max_length=200)

    def __str__(self):
        return str(self.FileName)


class ProcessMasterHistory(models.Model):
    ProcessHistoryID = models.AutoField(primary_key=True)
    ProcessID = models.ForeignKey(ProcessMaster, on_delete=models.CASCADE)
    ProcessName = models.CharField(max_length=50)
    ProjRegToBeDoneBy = models.IntegerField()
    ProjHasToBe = models.IntegerField()
    ProjShallBeDoneBy = models.IntegerField()
    NumberOfStages = models.IntegerField()
    InternalFacultyInvolvementNeeded = models.BooleanField(default=True)
    FacultyRequired = models.BooleanField(default=True)
    HODRequired = models.BooleanField()
    PrincipalRequired = models.BooleanField()
    PanelReviewRequired = models.BooleanField()
    ExternalGuideNeeded = models.BooleanField()
    FundingToBeProvided = models.BooleanField()
    ExpenseTrakingRequired = models.BooleanField()
    MaterialToBeProvided = models.BooleanField()
    FinalSubmissionEvaluated = models.BooleanField()
    EvaluationRole = models.IntegerField()
    ProcessReviewed = models.IntegerField()
    ProcessReviewedBy = models.IntegerField()
    CreatedBy = models.IntegerField()
    ModifiedBy = models.IntegerField()
    CreatedDate = models.DateTimeField(auto_now_add=True)
    ModifiedDate = models.DateTimeField(auto_now=True)
    IsActive = models.BooleanField(default=True)

    def __str__(self):
        return str(self.ProcessHistoryID) + " " + self.ProcessName


class ProcessOwner(models.Model):
    ProcessOwnerID = models.AutoField(primary_key=True)
    ProcessOwner = models.IntegerField()
    CreatedBy = models.IntegerField()
    ModifiedBy = models.IntegerField()
    CreatedDate = models.DateTimeField(auto_now_add=True)
    ModifiedDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.ProcessOwnerID) + " " + str(self.ProcessOwner)


class ProcessOwnerHistory(models.Model):
    ProcessOwnerHistoryID = models.AutoField(primary_key=True)
    ProcessOwnerID = models.ForeignKey(ProcessMaster, on_delete=models.CASCADE)
    ProcessOwner = models.ForeignKey(LoginMaster, on_delete=models.CASCADE)
    CreatedBy = models.IntegerField()
    CreatedDate = models.DateTimeField(auto_now_add=True)
    UpdateBunchID = models.IntegerField()

    def __str__(self):
        return str(self.ProcessOwnerHistoryID) + " " + str(self.ProcessOwner)


class ProcessToProgramMapping(models.Model):
    ProgMappingID = models.AutoField(primary_key=True)
    ProcessID = models.ForeignKey(ProcessMaster, on_delete=models.CASCADE)
    ProgramID = models.ForeignKey(ProgramMaster, on_delete=models.CASCADE)
    StreamID = models.ForeignKey(StreamMaster, on_delete=models.CASCADE)
    TermID = models.ForeignKey(TermMaster, on_delete=models.CASCADE)
    CreatedBy = models.IntegerField()
    ModifiedBy = models.IntegerField()
    CreatedDate = models.DateTimeField(auto_now_add=True)
    ModifiedDate = models.DateTimeField(auto_now=True)
    IsActive = models.BooleanField(default=True)

    def __str__(self):
        return str(self.ProgMappingID)


class ProcessToProgramMappingHistory(models.Model):
    ID = models.AutoField(primary_key=True)
    ProgMappingID = models.ForeignKey(ProcessToProgramMapping, on_delete=models.CASCADE)
    ProcessID = models.ForeignKey(ProcessMaster, on_delete=models.CASCADE)
    ProgramID = models.ForeignKey(ProgramMaster, on_delete=models.CASCADE)
    StreamID = models.ForeignKey(StreamMaster, on_delete=models.CASCADE)
    TermID = models.ForeignKey(TermMaster, on_delete=models.CASCADE)
    CreatedBy = models.IntegerField()
    ModifiedBy = models.IntegerField()
    CreatedDate = models.DateTimeField(auto_now_add=True)
    ModifiedDate = models.DateTimeField(auto_now=True)
    IsActive = models.BooleanField(default=True)

    def __str__(self):
        return str(self.ID)


class Students(models.Model):
    StudentID = models.AutoField(primary_key=True)
    StudentName = models.CharField(max_length=50)
    CollegeID = models.ForeignKey(CollegeMaster, on_delete=models.CASCADE)
    DepartmentID = models.ForeignKey(DepartmentMaster, on_delete=models.CASCADE)
    ProgramID = models.ForeignKey(ProgramMaster, on_delete=models.CASCADE)
    StreamID = models.ForeignKey(StreamMaster, on_delete=models.CASCADE)
    EnrollmentNumber = models.IntegerField()
    FirstName = models.CharField(max_length=50)
    MiddleName = models.CharField(max_length=50)
    LastName = models.CharField(max_length=50)
    EmailID = models.EmailField()
    Status = models.IntegerField(choices=((1, 'Pending'), (2, 'Approved'), (3, 'Rejected')))
    ApprovedBy = models.IntegerField()
    CreatedDate = models.DateTimeField(auto_now_add=True)
    ModifiedDate = models.DateTimeField(auto_now=True)
    CreatedBy = models.IntegerField()
    ModifiedBy = models.IntegerField()
    IsActive = models.BooleanField(default=True)
    DeactivationReason = models.TextField(max_length=300, null=True)

    def __str__(self):
        return self.FirstName + str(self.EnrollmentNumber)


class ProjectMembers(models.Model):
    MemberID = models.AutoField(primary_key=True)
    ProjectID = models.ForeignKey(Projects, on_delete=models.CASCADE)
    TeamMember = models.ForeignKey(Students, on_delete=models.CASCADE)
    CreatedBy = models.IntegerField()
    ModifiedBy = models.IntegerField()
    CreatedDate = models.DateTimeField(auto_now_add=True)
    ModifiedDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.MemberID)


class ProjectPanelMembers(models.Model):
    PrjPanelMemberID = models.AutoField(primary_key=True)
    PanelMember = models.ForeignKey(LoginMaster, on_delete=models.CASCADE)
    ProjectID = models.ForeignKey(Projects, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.PrjPanelMemberID)


class StageWorkFlowStates(models.Model):
    ApprovalStateID = models.AutoField(primary_key=True)
    ProcessID = models.ForeignKey(ProcessMaster, on_delete=models.CASCADE)
    StageID = models.ForeignKey(StageMaster, on_delete=models.CASCADE)
    ApprovalFacultyRole = models.IntegerField()
    ApprovalSequence = models.IntegerField()
    ApprovalType = models.IntegerField()

    def __str__(self):
        return str(self.ApprovalStateID)


class StageWorkflowStatesHistory(models.Model):
    ID = models.AutoField(primary_key=True)
    ApprovalStateID = models.ForeignKey(StageWorkFlowStates, on_delete=models.CASCADE)
    ProcessID = models.ForeignKey(ProcessMaster, on_delete=models.CASCADE)
    StageID = models.ForeignKey(StageMaster, on_delete=models.CASCADE)
    ApprovalFacultyRole = models.IntegerField()
    ApprovalSequence = models.IntegerField()
    ApprovalType = models.IntegerField()
    UpdateBunchID = models.IntegerField(default=ID)

    def __str__(self):
        return str(self.UpdateBunchID)


class StageMasterHistory(models.Model):
    StageHistoryID = models.AutoField(primary_key=True)
    StageID = models.ForeignKey(StageMaster, on_delete=models.CASCADE)
    ProcessID = models.ForeignKey(ProcessMaster, on_delete=models.CASCADE)
    StageName = models.CharField(max_length=50)
    StageSeq = models.IntegerField()
    ReqAnyUpload = models.BooleanField(default=True)
    ActivityType = models.IntegerField()
    RequireAnyApproval = models.BooleanField(default=True)
    InternalApprovalNeeded = models.BooleanField(default=True)
    InternalApprovalType = models.IntegerField()
    IsWorkflowDriven = models.BooleanField(default=True)
    ExternalGuideApprovalNeeded = models.BooleanField(default=True)
    MentorApprovalNeeded = models.BooleanField(default=True)
    PanelApprovalNeeded = models.BooleanField(default=True)
    DeanApprovalNeeded = models.BooleanField(default=True)
    RequireNoDueCertificate = models.BooleanField(default=True)
    CompletionCertiIssuedForStage = models.BooleanField(default=True)
    IsActive = models.BooleanField(default=True)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    CreatedBy = models.IntegerField()

    def __str__(self):
        return self.StageName


class StageActivities(models.Model):
    StageActivityID = models.AutoField(primary_key=True)
    ProjectID = models.ForeignKey(Projects, on_delete=models.CASCADE)
    StageID = models.ForeignKey(StageMaster, on_delete=models.CASCADE)
    Status = models.IntegerField(choices=((-1, "Locked"), (0, "Stage Unlocked"), (2, "Approved"), (1, "Submitted")))
    ActivityType = models.ForeignKey(StageMaster, on_delete=models.CASCADE, related_name="StageActivityType")
    # ActivityUpload = models.CharField(max_length=50)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    ModifiedDate = models.DateTimeField(auto_now=True)
    CreatedBy = models.IntegerField()
    ModifiedBy = models.IntegerField()

    def __str__(self):
        return str(self.StageActivityID)


class StageActivitiesApprovals(models.Model):
    StageApprovalID = models.AutoField(primary_key=True)
    ProjectID = models.ForeignKey(Projects, on_delete=models.CASCADE)
    StageActivityID = models.ForeignKey(StageActivities, on_delete=models.CASCADE)
    ApprovalMember = models.IntegerField()
    ApprovalStatus = models.IntegerField()

    def __str__(self):
        return str(self.StageApprovalID)


class StageActivitiesApprovalsHistory(models.Model):
    ApprovalHistoryID = models.AutoField(primary_key=True)
    StageApprovalID = models.ForeignKey(StageActivitiesApprovals, on_delete=models.CASCADE)
    ApprovalMember = models.IntegerField()
    ApprovalStatus = models.IntegerField()

    def __str__(self):
        return str(self.ApprovalHistoryID)


class ProjectToStageMapping(models.Model):
    PrjStageMappingID = models.AutoField(primary_key=True)
    ProjectID = models.ForeignKey(Projects, on_delete=models.CASCADE)
    StageID = models.ForeignKey(StageMaster, on_delete=models.CASCADE)
    StageName = models.CharField(max_length=50)

    def __str__(self):
        return str(self.PrjStageMappingID)


class Certificates(models.Model):
    CertificateID = models.AutoField(primary_key=True)
    ProjectID = models.ForeignKey(Projects, on_delete=models.CASCADE)
    StageActivityID = models.ForeignKey(StageActivities, on_delete=models.CASCADE)
    LoginID = models.ForeignKey(LoginMaster, on_delete=models.CASCADE)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    CollegeID = models.ForeignKey(CollegeMaster, on_delete=models.CASCADE)
    DepartmentID = models.ForeignKey(DepartmentMaster, on_delete=models.CASCADE)
    CurrentTerm = models.ForeignKey(TermMaster, on_delete=models.CASCADE)
    CertificateType = models.IntegerField(null=True)

    def __str__(self):
        return str(self.CertificateID)


class EvaluationGrades(models.Model):
    EvaluationID = models.AutoField(primary_key=True)
    ProjectID = models.ForeignKey(Projects, on_delete=models.CASCADE)
    StageActivityID = models.ForeignKey(StageActivities, on_delete=models.CASCADE)
    StudentLoginID = models.ForeignKey(LoginMaster, on_delete=models.CASCADE)
    CollegeID = models.ForeignKey(CollegeMaster, on_delete=models.CASCADE)
    DepartmentID = models.ForeignKey(DepartmentMaster, on_delete=models.CASCADE)
    CurrentTerm = models.ForeignKey(TermMaster, on_delete=models.CASCADE)
    Grade = models.IntegerField()
    CreatedDate = models.DateTimeField(auto_now_add=True)
    ModifiedDate = models.DateTimeField(auto_now=True)
    CreatedBy = models.IntegerField()

    def __str__(self):
        return str(self.EvaluationID) + " " + str(self.Grade)
