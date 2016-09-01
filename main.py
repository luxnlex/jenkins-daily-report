# -*- coding: utf-8 -*-
"""
@description: Jenkins daily report
@author: luxnlex
"""

from datetime import datetime, timedelta
import re
from jenkinsapi.jenkins import Jenkins
import traceback
import func

paramsList = func.params()
jenkinsAddress = paramsList[0]
loginJenkins = paramsList[1][0:paramsList[1].find('|')]
passwordJenkins = paramsList[1][paramsList[1].find('|')+1:]
ReportPath = paramsList[2]
ReportPathToSent = paramsList[3]
ReportPathWorkspace = paramsList[4]
images_web_link = paramsList[5]
scripts_web_link = paramsList[6]



HtmlTemplateFile = open('configs\\templates\\template.htm', 'r')
HtmlTemplate = HtmlTemplateFile.read()
HtmlTemplateFile.close()

ErrorReportFile = open('configs\\templates\\error.htm', 'r')
ErrorReport = ErrorReportFile.read()
ErrorReportFile.close()

PopupScriptFile = open('configs\\scripts\\popup.css', 'r')
PopupScript = PopupScriptFile.read()
PopupScript += """
<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.0/jquery.min.js"></script>
<script type="text/javascript" src='""" + scripts_web_link + """/popup.js'></script>
"""
PopupScriptFile.close()

TableStyleFile = open('configs\\templates\\table.css', 'r')
TableStyle = TableStyleFile.read()
TableStyleFile.close()

SortScriptFile = open('configs\\scripts\\sort.js', 'r')
SortScript = SortScriptFile.read()
SortScriptFile.close()

PieChartFile = open('configs\\scripts\\piechart.js', 'r')
PieChart = PieChartFile.read()
PieChartFile.close()

Jenkins = Jenkins(jenkinsAddress,loginJenkins,passwordJenkins)

func.existFolder(ReportPath)
func.existFolder(ReportPathToSent)
func.existFolder(ReportPathWorkspace)

print(datetime.now().strftime("%d.%m.%Y %I:%M %p"))
print('-'*100)
func.versions(Jenkins.version)

StartSequenceNumber=0
HtmlParts = ''
IndexList = []
CountSuccess,CountFail,CountAbortedProceed=0,0,0
StartIndex=0

AllBuilds = Jenkins.keys()

for i in AllBuilds:
    CurrentNameJob = str(AllBuilds[StartIndex])   
    Job = Jenkins.get_job(CurrentNameJob)
    JobFullInfo = Job._data      

    if JobFullInfo.get('lastBuild')==None:
        StartIndex += 1
        continue
    else:
        if Job.is_enabled()==False:
            StartIndex += 1
            print('(!) Исключен отключенный проект!')
            continue
        else:
            StartIndex += 1
            GoodJob = Jenkins.get_job(CurrentNameJob)
            IndexList.append(str(GoodJob))
            print('(+) Проект ' + str(CurrentNameJob) + ' обработан успешно!')
print('-'*100)
print('Список проектов для формирования отчета успешно сформирован.')
print('Проекты не имеющие сборок пропускаются!')

CurrentDateFormatted = datetime.now().strftime("%Y-%m-%d")
try:
    for curPrj in IndexList:
        CurrentNameJobGood = str(curPrj)
        JobGood = Jenkins.get_job(CurrentNameJobGood)
        Build = JobGood.get_last_build()
        BuildStatus = func.buildStatus(Build.get_status())
        try:
            LastSuccessList = JobGood.get_last_good_build()
            LastSuccessDate = LastSuccessList.get_timestamp()
            LastSuccessNumber = LastSuccessList.get_number()
            CurrentNumber = JobGood.get_last_buildnumber()

            JenkinsDateTime = datetime.strptime(str(LastSuccessDate)[0:-6], '%Y-%m-%d %H:%M:%S') + timedelta(hours=3)
            DeltaDate = func.days(str(datetime.date(datetime.now())-datetime.date(JenkinsDateTime)))

            print('-'*100)
            print('Последний успех: '+ DeltaDate + ', ' + str(JenkinsDateTime))
            CountSuccessProjectNumbers = str(CurrentNumber-LastSuccessNumber)
            print('Количество завалившихся сборок с последней успешной: ' + CountSuccessProjectNumbers)

            CountSuccessProjectNumbers = func.builds(CountSuccessProjectNumbers)
        except:
            DeltaDate = str('Нет данных')
            CountSuccessProjectNumbers = str('Нет данных')
            JenkinsDateTime = str('-')
            print('-'*100)
            print('Последний успех: нет данных')
            print('Количество завалившихся сборок с последней успешной: нет данных')

        StartSequenceNumber += 1
        
        if BuildStatus == 'Протестировано успешно':
            CountSuccess += 1
        elif BuildStatus == 'Протестировано с ошибками':
            CountFail += 1
        else:
            CountAbortedProceed=CountAbortedProceed+1

        CountAll=CountSuccess+CountFail+CountAbortedProceed

        GoodJobFullInfo = JobGood._data

        JobDescription = GoodJobFullInfo.get('description')

        if len(str(StartSequenceNumber)) == 1:
            StartSequenceNumber = "0" + str(StartSequenceNumber)

        Tr = """
<tr {TrColor}>
<td width="3%"><center>{SequenceNumber}</center></td>
<td width="5%"><center><img src="{thumb}"></img></center></td>
<td width="22%"><a href=""" + GoodJobFullInfo.get('url') + """>""" + CurrentNameJobGood + """</a></td>
<td width="10%"><P class="ttp_lnk"><a href="#" title=" """ + JobDescription + """ ">Описание базы</a></td>
<td width="10%">""" + DeltaDate + """<br>""" + '(' + str(JenkinsDateTime) + ')' + """</td>
<td width="10%">""" + CountSuccessProjectNumbers + """</td>"""

        HtmlParts = HtmlParts + func.coloring(BuildStatus,Tr,images_web_link,StartSequenceNumber)

        HtmlReport = HtmlTemplate.format(CurrentDate=str(datetime.now().strftime("%d.%m.%Y %H-%M-%S")),HtmlPartsLoaded=HtmlParts,AllCount=CountAll,SuccessCount=CountSuccess,FailCount=CountFail,ReplaceScriptTemplate=PieChart,SortScript=SortScript,ReplacePopupScript=PopupScript,ReplaceTableStyle=TableStyle,sortPng=images_web_link + '/sort.png')
        print('Информация о проекте ' + str(CurrentNameJobGood) + ' успешно прочитана и добавлена в отчет!')
        StartSequenceNumber = int(StartSequenceNumber)
        ErrorReport = "" 
except Exception:
    print('Один из проектов не был ни разу запущен! Проверьте настройки!')
    HtmlReport = ""
    print(traceback.format_exc())
else:
    print('-'*100)
    print('Ошибок не обнаружено.')
finally:
    print('Файл отчета успешно выгружен!')

PercentSuccess = func.percent(CountSuccess,CountAll)
PercentFail = round((100-PercentSuccess),3)

func.saver(ReportPath,ReportPathToSent,ReportPathWorkspace,HtmlReport.replace('{ScriptSuccessAll}',str(PercentSuccess)).replace('{ScriptFailAll}',str(PercentFail)),ErrorReport)
func.result(PercentSuccess,PercentFail)