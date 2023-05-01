import os 
import PyPDF2


def String_pdf(file):
    pdfFileObj = open(file, 'rb')         
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pageObj = pdfReader.getPage(0)
    String = pageObj.extractText()
    String_list = String.split('\n')
    String_list_Aux = list(filter(lambda x: x != '' and x != ' ' and x!='  ', String_list))
    String_list_Aux.pop(0)
    String_curr = '\n'.join(String_list_Aux)
    return String_curr

def ComparePDF(today,yesterday,excel):
    rute_today  = today
    rute_yesterday = yesterday
    files_today = os.listdir(rute_today)
    files_yestarday = os.listdir(rute_yesterday)
    lista_cambios = []
    for x in files_today:
        for y in files_yestarday:
            if x == y:  
                file_today = rute_today + f'\\{x}'
                file_yestarday = rute_yesterday + f'\\{y}'
                String_curr_today = String_pdf(file_today)
                String_curr_yestarday = String_pdf(file_yestarday)
                if String_curr_today  != String_curr_yestarday:
                    radicado = x.replace('.pdf','')
                    lista_cambios.append(radicado)
                    #print(String_curr_today)
                else:
                    pass    
    cambios_aux = []
    for x in excel['RADICADO']:
        if x in lista_cambios:
            cambios_aux.append('X')
        else:
            cambios_aux.append('')
    
    return lista_cambios,cambios_aux
