from django.contrib import admin

# Register your models here.
from .models import CollegeMaster,StageToFileMapping,RoleMaster,FacultyMaster,StageMaster,ProcessMasterHistory,ProjectMembers,ProjectPanelMembers,ProjectToStageMapping,StageMasterHistory,ProcessToProgramMapping,ProcessToProgramMappingHistory,Certificates,EvaluationGrades,Students,ExternalUsers,LoginMaster,StageWorkFlowStates,StageActivities,Projects,TermMaster,ProcessMaster,DepartmentMaster,StreamMaster,ProgramMaster,StageActivitiesApprovals,ProcessOwner,ProcessOwnerHistory,StageActivitiesApprovalsHistory,StageWorkflowStatesHistory
mymodels = [CollegeMaster,StageToFileMapping, FacultyMaster,RoleMaster,StageMaster,ProcessMasterHistory,ProjectMembers,ProjectPanelMembers,ProjectToStageMapping,StageMasterHistory,ProcessToProgramMapping,ProcessToProgramMappingHistory,Certificates,EvaluationGrades,Students,ExternalUsers,LoginMaster,StageWorkFlowStates,StageActivities,Projects,TermMaster,ProcessMaster,DepartmentMaster,StreamMaster,ProgramMaster,StageActivitiesApprovals,ProcessOwner,ProcessOwnerHistory,StageActivitiesApprovalsHistory,StageWorkflowStatesHistory]
admin.site.register(mymodels)