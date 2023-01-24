from aip import AipSpeech


APP_ID = '22632304'
API_KEY = 'zUWDV4UgeRbah3tOYUS7CKUK'
SECRET_KEY = 'jmCuQmlVSWLdIRM9lz3GVcFlYtrUaWpd'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)



def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()



print(client.asr(get_file_content('./speak.wav'), 'wav', 16000, {'dev_pid': 1537,}))
