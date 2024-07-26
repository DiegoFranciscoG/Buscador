import os
import requests
import vlc
from animeflv import AnimeFLV

def download_episode(url, file_name):
    response = requests.get(url, stream=True)
    with open(file_name, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
    print(f'Episodio descargado como {file_name}')

def play_episode(file_name):
    player = vlc.MediaPlayer(file_name)
    player.play()
    input("Presiona Enter para detener la reproducción...")

with AnimeFLV() as api:
    elements = api.search(input('Buscar Anime: '))
    for i, element in enumerate(elements):
        print(f'{i}. {element.title}')
    try:
        choice = int(input('Elige una opción: '))
        info = api.get_anime_info(elements[choice].id)
        info.episodes.reverse()
        for j, episode in enumerate(info.episodes):
            print(f'{j}. {episode.id}')
        index_episode = int(input('Elige un episodio: '))
        serie = elements[choice].id
        capitulo = info.episodes[index_episode].id
        results = api.get_links(serie, capitulo)
        for result in results:
            print(f'{result.server}: {result.link}')

        download_option = input("¿Deseas descargar este episodio? (s/n): ")
        if download_option.lower() == 's':
            download_link = results[0].link  # Selecciona el primer enlace para la descarga
            file_name = f"{elements[choice].title}_E{info.episodes[index_episode].id}.mp4"
            download_episode(download_link, file_name)

        play_option = input("¿Deseas reproducir este episodio? (s/n): ")
        if play_option.lower() == 's':
            if download_option.lower() != 's':
                file_name = input("Introduce la ruta del archivo de video: ")
            play_episode(file_name)

    except Exception as e:
        print(e)
