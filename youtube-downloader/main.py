from PySimpleGUI.PySimpleGUI import Window
from pytube import YouTube
from pytube import Playlist
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

def escolha_qualidade(playlist): #Printa para o usuário uma janela para escolher a qualidade do video
    if playlist == True:
        layout_escolha_de_qualidade = [
            [sg.Text('Escolha a qualidade do video')],
            [sg.Button('menor-qualidade', key='video_low'), sg.Button('maior-qualidade', key='video_medium')]
        ]
        janela_qualidade = sg.Window('Escolha a qualidade', layout_escolha_de_qualidade)
    else:   
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

def escolha_tipo_playlist(): #Printa para o usuário uma janela para escolher o tipo da playlist
    layout_escolha_playlist = [
        [sg.Text('Escolha o modo de playlist')],
        [sg.Button('Playlist de video', key='playlist_video'), sg.Button('Playlist de audio', key='playlist_audio')]
    ]
    janela_escolha_playlist = sg.Window('Escolha a Playlist', layout_escolha_playlist)

    event_playlist, value = janela_escolha_playlist.read()

    if event_playlist == 'playlist_video':
        response = 'p_video'
    
    if event_playlist == 'playlist_audio':
        response = 'p_audio'
    
    return response

def pega_audio(link_video, folder, title_video): #Caso o usuário escolha a maior qualidade, o audio é baixado separadamente a fim de ser juntado em um clip
    audio_high = link_video.streams.get_audio_only()
    audio_high.download(folder, filename='Audio.mp3')
            
    cria_clip(folder, title_video)

def baixa_video(values): #Opções de video para baixar
    
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

    video.download(folder, filename=f'{title_video}.mp4')

    if quality_video == 'high':
        pega_audio(link_video, folder, title_video)

def baixa_audio(values): #Opção audio para baixar

    folder = sg.popup_get_folder("Escolha a pasta para salvar")

    link_video = YouTube(values['url'])
    title_video = link_video.title

    v_audio = link_video.streams.get_audio_only()
    v_audio.download(folder, filename=f'{title_video}.mp3')

def baixa_playlist(values): #Opção de playlist para baixar
    
    folder = sg.popup_get_folder("Escolha a pasta para salvar")

    link_playlist = Playlist(values['url'])

    quality = escolha_tipo_playlist()

    playlist = True

    if quality == 'p_video':
        quality = escolha_qualidade(playlist)

        if quality == 'low':
            for video in link_playlist.videos:
                title = video.title
                video.streams.first().download(folder, filename=f'{title}.mp4')
        
        if quality == 'medium':
            for video in link_playlist.videos:
                title = video.title
                video.streams.get_highest_resolution().download(folder, filename=f'{title}.mp4')
        
    
    if quality == 'p_audio':
        for audio in link_playlist.videos:
            title = audio.title
            audio.streams.get_audio_only().download(folder, filename=f'{title}.mp3')

def main(): #Inicio do programa
    #Define o tema da janela
    sg.theme('DarkBlue3') 

    #Layout da janela
    layout = [  
        [sg.Text('Youtube Downloader', font='Roboto_Mono')],
        [sg.Text('Cole sua url aqui')],
        [sg.InputText(key='url')],
        [sg.Button('Download video', key='video'), sg.Button('Download audio', key='audio'), sg.Button('Download playlist', key='playlist')],
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
            baixa_video(values)
            sg.popup('Download Completo °3°')
            break

        #Caso opção for audio
        if event == 'audio':
            baixa_audio(values)
            sg.popup('Download Completo °3°')
            break

        if event == 'playlist':
            baixa_playlist(values)
            sg.popup('Download Completo °3°')
            break

    window.close()

if __name__ == '__main__':
    main()