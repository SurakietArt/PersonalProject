from django.http import response
from django.shortcuts import render,redirect
from .models import *
import requests
from datetime import datetime


def home(request):
    all_case_data = Case.objects.all().values_list('country','case')
    list_all_case_data = list(all_case_data)
    date_data = Case.objects.values_list('case')
    for date_case_tuple in date_data:
        date_case_list = list(date_case_tuple)
        for date_case_dict in date_case_list:
            date_list = list(date_case_dict.keys())
    date_list.sort(key=lambda date: datetime.strptime(date, "%m/%d/%y"),reverse=True)  
    default_date = date_list[0]
    template_data = {}
    for each_case_data in list_all_case_data:
        country = each_case_data[0]
        dict_case = each_case_data[1]
        case = dict_case[default_date]
        template_data[country] = case
    sorted_template_data = dict(sorted(template_data.items(), key=lambda item: item[1],reverse=True))
    if request.method == 'POST':
        if 'date' in request.POST:
            select_date = request.POST['date']
            template_data = {}
            for each_case_data in list_all_case_data:
                country = each_case_data[0]
                dict_case = each_case_data[1]
                case = dict_case[select_date]
                template_data[country] = case
            sorted_template_data = dict(sorted(template_data.items(), key=lambda item: item[1],reverse=True))
            return render(request,'home.html',{"sorted_template_data":sorted_template_data,"date_list":date_list,"select_date":select_date})
    return render(request,'home.html',{"sorted_template_data":sorted_template_data,"date_list":date_list,"default_date":default_date})

def update(request):
    url = 'https://disease.sh/v3/covid-19/historical/KH%2CCH%2CNG%2CCZ%2CUZ%2CGF%2CDE%2CBH%2CMH%2CVE%2CRE%2CGY%2CBI%2CKI%2CJO%2CAU%2CEH%2CGE%2CLU%2CJP%2CBO%2CD2%2CAL%2CME%2CUS%2CBA%2CPG%2CLV%2CIR%2CGM%2CNC%2CKS%2CBN%2CBR%2CNO%2CGA%2CT2%2CIQ%2CSU%2CDJ%2CPL%2CSO%2CSR%2CZM%2CAN%2CY3%2CMM%2CGP%2CMX%2CMU%2CSA%2CLK%2CNR%2CMK%2CD1%2CGI%2CTW%2CCD%2CMP%2CET%2CAT%2CCN%2CMT%2CIL%2CLS%2CLA%2CBF%2CVC%2CPM%2CSI%2CLB%2CLR%2CAZ%2CES%2CQA%2COM%2CSK%2CCV%2CGB%2CBB%2CIE%2CCI%2CRW%2CTV%2CSM%2CER%2CGL%2CTM%2CKE%2CTJ%2CAI%2CFO%2CMG%2CLI%2CRU%2CVG%2CC1%2CSB%2CSC%2CMO%2CUG%2CMA%2CBW%2CTK%2CHK%2CSG%2CKR%2CML%2CAS%2CLT%2CZA%2CSH%2CNA%2CAD%2CNP%2CUY%2CLC%2CFK%2CMD%2CGT%2CAO%2CVN%2CRS%2CKM%2CGH%2CTZ%2CMQ%2CYE%2CM2%2CIM%2CTC%2CLY%2CHR%2CTG%2CSD%2CNU%2CD3%2CBZ%2CIT%2CFI%2CPY%2CAF%2CAE%2CPE%2CCG%2CHN%2CVI%2CCK%2CSL%2CPF%2CEG%2CWS%2CBY%2CPA%2CHT%2CBD%2CIN%2CJE%2CMS%2CMN%2CHU%2CID%2CBM%2CDM%2CNE%2CFJ%2CCM%2CDK%2CNL%2CTN%2CCY%2CM3%2CKP%2CVU%2CST%2CTD%2CNZ%2CCA%2CKG%2CJG%2CTT%2CGQ%2CT1%2CUA%2CZW%2CSY%2CTO%2CSZ%2CWF%2CTH%2CTL%2CBE%2CIS%2CBG%2CSS%2CTR%2CMW%2CGN%2CMY%2CAG%2CAR%2CRO%2CPS%2CJM%2CMV%2CGW%2CMR%2CSN%2CNF%2CKN%2CBT%2CPW%2CKZ%2CBJ%2CAW%2CCS%2CDO%2CY1%2CEC%2CNI%2CCU%2CKW%2CPT%2CY2%2CGR%2CCF%2CDZ%2CGU%2CGD%2CFR%2CMZ%2CEE%2CCL%2CPR%2CCR%2CAM%2CGG%2CM1%2CSE%2CPK%2CKY%2CMC%2CBS%2CE1%2CCO%2CSV%2CPH%2CPH?lastdays=30'
    ## get country code : https://public.opendatasoft.com/explore/dataset/countries-codes/table/?lang=
    response = requests.get(url)
    raw_data = response.json()
    for each_raw_data in raw_data:
        if each_raw_data == None:
            continue
        country_data = each_raw_data['country']
        country_target = Case.objects.filter(country=country_data)
        case_data = each_raw_data['timeline']['cases']
        country_target.update(case=case_data)
    all_case_data = Case.objects.all() 
    return render(request,'update.html',{"all_case_data":all_case_data})
