from pytube import YouTube
import PySimpleGUI as sg
import os

#Function
def qualidade():
    layout_escolha_de_qualidade = [
        [sg.Text('Escolha a qualidade do video')],
        [sg.Button('menor-qualidade', key='video_low'), sg.Button('maior-qualidade', key='video_high')]
    ]
    janela_qualidade = sg.Window('Escolha a qualidade', layout_escolha_de_qualidade)

    event_quality, value = janela_qualidade.read()

    if event_quality == 'video_high':
        resp = 'high'
    
    if event_quality == 'video_low':
        resp = 'low'

    return resp



#Defini tema da janela
sg.theme('DarkBlue3')

# Layout da janela
layout = [  
    [sg.Text('Youtube Downloader', font='Roboto_Mono')],
    [sg.Text('Cole sua url aqui')],
    [sg.InputText(key='url')],
    [sg.Button('Download video', key='video'), sg.Button('Download audio', key='audio')],
]
window = sg.Window('Youtube', layout)

#Codigo em si
while True:
    #Pega os valores do input da janela
    event, values = window.read()

    #Tratamento de janela, caso seja fechada encerra o programa
    if event == sg.WIN_CLOSED:
        break
    
    #Caso opção for video
    if event == 'video':

        #Pede para o usuário buscar pasta de salvamento
        folder = sg.popup_get_folder("Escolha a pasta para salvar")

        #Pega o link passado na janela e o atribui a variavel yt
        link_video = YouTube(values['url'])

        quality_video = qualidade()
        
        if quality_video == 'low':
            video = link_video.streams.get_lowest_resolution()
            
        elif quality_video == 'high':
            video = link_video.streams.get_highest_resolution()
        
        video.download(folder)
        sg.popup('Download Completo °3°')
        break

    #Caso opção for audio
    if event == 'audio':
        #Pede para o usuário buscar pasta de salvamento
        folder = sg.popup_get_folder("Escolha a pasta para salvar")

        #Pega o link passado na janela e o atribui a variavel yt
        link_video = YouTube(values['url'])

        #pega o link e passa a função, pega somente o audio do video
        v_audio = link_video.streams.get_audio_only()

        #Salva o audio baixado na variavel out_file em seguida usa a lib os para criar um splitext
        out_file = v_audio.download(folder)
        base, exp = os.path.splitext(out_file)

        #Atribui a extensão e a base a variavel new_file e usa a lib os para dar rename no arquivo transformando-o assim em um mp3 
        new_file = base + '.mp3'
        os.rename(out_file, new_file)

        #Retorna mensssagem para usuario
        sg.popup('Download Completo °3°')
        break


window.close()



    
    
    

