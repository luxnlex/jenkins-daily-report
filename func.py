# -*- coding: utf-8 -*-
"""
@description: Jenkins daily report
@author: luxnlex
"""
import os
import sys
from datetime import datetime, timedelta
import time
import re

def params():
    inFile = open('configs\\conf.ini', 'r')
    params = []
    for i in inFile.readlines():
    	params.append(i.strip())
    inFile.close()
    return params

def days(DeltaDate):
    if re.search('day,', DeltaDate):
        DeltaDate = DeltaDate[0:-13]
    elif re.search('days,', DeltaDate):
        DeltaDate = DeltaDate[0:-14]
    else:
        DeltaDate = '0'
        
    DeltaDate = str(DeltaDate)

    if DeltaDate[0] == '0':
        DeltaDate = """- Сегодня"""
    else:
        if len(DeltaDate) == 1 and DeltaDate != '-':
            if DeltaDate[-1] == '0' or 5 <= int(DeltaDate[-1]) <= 9 or 11 <= int(DeltaDate) <= 19:
                DeltaDate = """0""" + str(DeltaDate) + """ дней назад"""
            elif DeltaDate[-1] == '1':
                DeltaDate = """0""" + str(DeltaDate) + """ день назад"""
            else:
                DeltaDate = """0""" + str(DeltaDate) + """ дня назад""" 
        else:
            if DeltaDate[-1] == '0' or 5 <= int(DeltaDate[-1]) <= 9 or 11 <= int(DeltaDate) <= 19:
                DeltaDate = str(DeltaDate) + ' дней назад'
            elif DeltaDate[-1] == '1':
                DeltaDate = str(DeltaDate) + ' день назад'
            else:
                DeltaDate = str(DeltaDate) + ' дня назад'     
    return DeltaDate    

def builds(CountSuccessProjectNumbers):
    if CountSuccessProjectNumbers[0] == '0':
        CountSuccessProjectNumbers = """-"""
    else:    
        if len(CountSuccessProjectNumbers) == 1 and CountSuccessProjectNumbers != '-':
            if CountSuccessProjectNumbers[-1] == '0' or 5 <= int(CountSuccessProjectNumbers[-1]) <= 9 or 11 <= int(CountSuccessProjectNumbers) <= 19:
                CountSuccessProjectNumbers = """0""" + str(CountSuccessProjectNumbers) + """ сборок"""
            elif CountSuccessProjectNumbers[-1] == '1':
                CountSuccessProjectNumbers = """0""" + str(CountSuccessProjectNumbers) + """ сборка"""
            else:
                CountSuccessProjectNumbers = """0""" + str(CountSuccessProjectNumbers) + """ сборки"""
        else:
            if CountSuccessProjectNumbers[-1] == '0' or 5 <= int(CountSuccessProjectNumbers[-1]) <= 9 or 11 <= int(CountSuccessProjectNumbers) <= 19:
                CountSuccessProjectNumbers = str(CountSuccessProjectNumbers) + """ сборок"""
            elif CountSuccessProjectNumbers[-1] == '1':
                CountSuccessProjectNumbers = str(CountSuccessProjectNumbers) + """ сборка"""
            else:
                CountSuccessProjectNumbers = str(CountSuccessProjectNumbers) + """ сборки"""   
    return CountSuccessProjectNumbers

def existFolder(Folder):
	if not os.path.exists(Folder):
		os.makedirs(Folder)

def versions(JenkinsVer):
    print('Информация о рабочем окружении.')
    print('Версия ядра Windows: ' + str(sys.getwindowsversion().major) + '.' +
	      str(sys.getwindowsversion().minor) + ' build ' +
	      str(sys.getwindowsversion().build) + ' ' +
	      str(sys.getwindowsversion().service_pack))
    print('Версия интерпретатора Python: ' + str(sys.version_info.major) + '.' +
	      str(sys.version_info.minor) + '.' +
	      str(sys.version_info.micro) + ' ' +
	      str(sys.version_info.releaselevel))
    print('Версия системы CI Jenkins: ' + str(JenkinsVer))
    print('-'*100)

def percent(Success, All):
    Percent = round(((Success/All)*100),3)
    return(Percent)

def coloring(BuildStatusRus,Tr,images_web_link,StartSequenceNumber):
	if BuildStatusRus == 'Протестировано успешно':
		trColor = Tr.format(TrColor='bgcolor = "#90EE90"',thumb=images_web_link + '/up40px.png',SequenceNumber = StartSequenceNumber)
	elif BuildStatusRus == 'Протестировано с ошибками':
		trColor = Tr.format(TrColor='bgcolor = "#FA8072"',thumb=images_web_link + '/down40px.png',SequenceNumber = StartSequenceNumber)
	else:
		trColor = Tr.format(TrColor='bgcolor = "#D3D3D3"',thumb=images_web_link + '/na40px.png',SequenceNumber = StartSequenceNumber)
	return trColor

def result(PercentSuccess,PercentFail):
    print('-'*100)
    print('% успеха: ' + str(PercentSuccess))
    print('% провалов: ' + str(PercentFail))

def saver(ReportPath,ReportPathToSent,ReportPathWorkspace,HtmlReportComplete,ErrorReport):
    HtmlReportName = open(str(str(ReportPath) + '\\' + datetime.now().strftime("%Y.%m.%d %H-%M-%S")) + '.DailyReport.htm', 'w')
    HtmlReportName.write(HtmlReportComplete + ErrorReport)
    HtmlReportName.close()
    HtmlReportToSent = open(str(str(ReportPathToSent) + '\\') + 'DailyReport.htm', 'w')
    HtmlReportToSent.write(HtmlReportComplete + ErrorReport)
    HtmlReportToSent.close()
    HtmlReportWorkspace = open(str(str(ReportPathWorkspace) + '\\') + 'DailyReport.htm', 'w')
    HtmlReportWorkspace.write(HtmlReportComplete + ErrorReport)
    HtmlReportWorkspace.close()

def buildStatus(BuildStatus):
    return str(BuildStatus).replace('SUCCESS','Протестировано успешно').replace('FAILURE','Протестировано с ошибками').replace('ABORTED','Тестирование отменено вручную').replace('None','Тестирование еще не завершено')