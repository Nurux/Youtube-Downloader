from pytube import YouTube
import moviepy.editor as mpe
import PySimpleGUI as sg
import os

#Functions
def cria_clip(folder, title_video): #Junta o melhor video com o melhor audio em um unico clip
    clip = mpe.VideoFileClip( folder + '\Video_Maior_Qualidade.mp4')
    audio_clip = mpe.AudioFileClip(folder + '\Audio.mp3')

    final_clip = clip.set_audio(audio_clip)
    final_clip.write_videofile(folder + f'\{title_video}.mp4')

    os.remove(folder + '\Video_maior_qualidade.mp4')
    os.remove(folder + '\Audio.mp3')

def escolha_qualidade(): #Printa para o usuário uma janela para escolher a qualidade do video
    layout_escolha_de_qualidade = [
        [sg.Text('Escolha a qualidade do video')],
        [sg.Button('menor-qualidade', key='video_low'), sg.Button('media-qualidade', key='video_medium'), sg.Button('maior-qualidade', key='video_high')]
    ]
    janela_qualidade = sg.Window('Escolha a qualidade', layout_escolha_de_qualidade)

    event_quality, value = janela_qualidade.read()

    if event_quality == 'video_high':
        response = 'high'
        
    if event_quality == 'video_medium':
        response = 'medium'

    if event_quality == 'video_low':
        response = 'low'

    return response

def audio_high(link_video, folder, title_video): #Caso o usuário escolha a maior qualidade, o audio é baixado separadamente a fim de ser juntado em um clip
    audio_high = link_video.streams.get_audio_only()
    audio_high.download(folder, filename='Audio.mp3')
            
    cria_clip(folder, title_video)

def baixa_video(): #Opções de video para baixar
    folder = sg.popup_get_folder("Escolha a pasta para salvar")

    link_video = YouTube(values['url'])
    quality_video = escolha_qualidade()
        
    if quality_video == 'low':
        video = link_video.streams.first() 
        title_video = link_video.title
    elif quality_video == 'medium':
        video = link_video.streams.get_highest_resolution()
        title_video = link_video.title
    elif quality_video == 'high':
        list_video = link_video.streams.filter(mime_type='video/mp4', res='1080p', adaptive='True')
        video = list_video[0]
        title_video = 'Video_Maior_Qualidade'

    video.download(folder, filename=title_video + '.mp4')

    if quality_video == 'high':
        audio_high(link_video, folder, title_video)

def baixa_audio(): #Opção audio para baixar
    folder = sg.popup_get_folder("Escolha a pasta para salvar")

    link_video = YouTube(values['url'])
    title_video = link_video.title

    v_audio = link_video.streams.get_audio_only()
    v_audio.download(folder, filename=title_video + '.mp3')

#Inicio
sg.theme('DarkBlue3') #Define o tema da janela

#Layout da janela
layout = [  
    [sg.Text('Youtube Downloader', font='Roboto_Mono')],
    [sg.Text('Cole sua url aqui')],
    [sg.InputText(key='url')],
    [sg.Button('Download video', key='video'), sg.Button('Download audio', key='audio')],
]
window = sg.Window('Youtube', layout)

while True:
    #Pega os valores do input da janela
    event, values = window.read()

    #Tratamento de janela, caso seja fechada encerra o programa
    if event == sg.WIN_CLOSED:
        break
    
    #Caso opção for video
    if event == 'video':
        baixa_video()
        sg.popup('Download Completo °3°')
        break

    #Caso opção for audio
    if event == 'audio':
        baixa_audio()
        sg.popup('Download Completo °3°')
        break

window.close()
