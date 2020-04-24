from pdfDownloader import *
from awsProcessing import *
from postAwsProcessing import *
from os import listdir

if __name__ == '__main__':
    test = False
    myS3 = 'do-covid-19'
    if test:
        # jobId = '3256e214371aea597f64a056b4094fef1e612d5accb2bffdd19f3157eb2c11f8'
        # print("Started job with id: {}".format(jobId))
        # if (isJobComplete(jobId)):
        #     response = getJobResults(jobId)
        #     # result = get_table_csv_results(response)
        #     result = get_table_pd_results(response)
        #     a = pandizer(result)
        #     print(a)


        reportePath = '../input/ReporteDiario/*.pdf'
        rep = preparePathsForUpload(reportePath)
        for eachrep in rep:
            if not checkIfFileIsOnS3(myS3, eachrep[1]):
                upload_file(eachrep[0], myS3, eachrep[1])

    else:
        # REPORTE DIARIO
        obtenerReporteDiario('https://www.gob.cl/coronavirus/cifrasoficiales/', '../input/ReporteDiario/')
        reportePath = '../input/ReporteDiario/*.pdf'
        rep = preparePathsForUpload(reportePath)
        # Como sabemos si un archivo ya se proceso??
        # Revisemos el output
        outputFiles = listdir('../output/raw/ReporteDiario')

        for eachrep in rep:
            # Check if the file was uploaded
            if not checkIfFileIsOnS3(myS3, eachrep[1]):
                upload_file(eachrep[0], myS3, eachrep[1])

            # Check if the file was processed
            sourceFile = eachrep[1].split('/')[1].replace('.pdf', '')
            if [x for x in outputFiles if sourceFile in x]:
                print(sourceFile + ' was already processed')

            else:
                print('processing ' + sourceFile)
                upload_file(eachrep[0], myS3, eachrep[1])
                jobId = startJob(myS3, eachrep[1])
                myfile = open("jobs.log", 'a+')
                myfile.write(eachrep[1] + ': ' + jobId + '\n')
                myfile.close()
                if (isJobComplete(jobId)):
                    response = getJobResults(jobId)
                    result = get_table_pd_results(response)
                    a = pandizer(result)
                    dumpDict2csv(a, sourceFile, '../output/raw/ReporteDiario/')

        # INFORME SITUACION
        obtenerSituacionCOVID19('http://epi.minsal.cl/informes-covid-19/', '../input/InformeSituacionCOVID19/')
        situacionPath = '../input/InformeSituacionCOVID19/*.pdf'
        sit = preparePathsForUpload(situacionPath)
        outputFiles = listdir('../output/raw/InformeSituacionCOVID19')
        for eachsit in sit:
            sourceFile = eachsit[1].split('/')[1].replace('.pdf', '')

            if [x for x in outputFiles if sourceFile in x]:
                print(sourceFile + ' was already processed')
            else:
                print('processing ' + sourceFile)
                upload_file(eachsit[0], myS3, eachsit[1])
                jobId = startJob(myS3, eachsit[1])
                myfile = open("jobs.log", 'a+')
                myfile.write(eachsit[1] + ': ' + jobId + '\n')
                myfile.close()
                if (isJobComplete(jobId)):
                    response = getJobResults(jobId)
                    result = get_table_pd_results(response)
                    a = pandizer(result)
                    dumpDict2csv(a, sourceFile, '../output/raw/InformeSituacionCOVID19/')

        # INFORME EPIDEMIOLOGICO
        obtenerInformeEpidemiologico('https://www.gob.cl/coronavirus/cifrasoficiales/',
                                     '../input/InformeEpidemiologico/')
        infPath = '../input/InformeEpidemiologico/*.pdf'
        inf = preparePathsForUpload(infPath)
        outputFiles = listdir('../output/raw/InformeEpidemiologico')
        for eachinf in inf:
            sourceFile = eachinf[1].split('/')[1].replace('.pdf', '')

            if [x for x in outputFiles if sourceFile in x]:
                print(sourceFile + ' was already processed')
            else:
                print('processing ' + sourceFile)
                upload_file(eachinf[0], myS3, eachinf[1])
                jobId = startJob(myS3, eachinf[1])
                myfile = open("jobs.log", 'a+')
                myfile.write(eachinf[1] + ': ' + jobId + '\n')
                myfile.close()
                if (isJobComplete(jobId)):
                    response = getJobResults(jobId)
                    result = get_table_pd_results(response)
                    a = pandizer(result)
                    dumpDict2csv(a, sourceFile, '../output/raw/InformeEpidemiologico/')