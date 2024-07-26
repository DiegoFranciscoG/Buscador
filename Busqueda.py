import os
import requests
import vlc
from animeflv import AnimeFLV

def fetch_video(url, destination):
    response = requests.get(url, stream=True)
    with open(destination, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
    print(f'Video guardado como {destination}')

def play_video(file_path):
    player = vlc.MediaPlayer(file_path)
    player.play()
    input("Presiona Enter para detener la reproducción...")

with AnimeFLV() as client:
    search_results = client.search(input('Introduce el nombre del anime: '))
    for idx, anime in enumerate(search_results):
        print(f'{idx}. {anime.title}')
    
    try:
        selection = int(input('Selecciona el número del anime: '))
        anime_details = client.get_anime_info(search_results[selection].id)
        anime_details.episodes.reverse()
        
        for ep_idx, episode in enumerate(anime_details.episodes):
            print(f'{ep_idx}. {episode.id}')
        
        episode_choice = int(input('Selecciona el número del episodio: '))
        series_id = search_results[selection].id
        episode_id = anime_details.episodes[episode_choice].id
        links = client.get_links(series_id, episode_id)
        
        for link in links:
            print(f'{link.server}: {link.link}')

        download_choice = input("¿Quieres descargar este episodio? (s/n): ")
        if download_choice.lower() == 's':
            video_url = links[0].link  # Selecciona el primer enlace para la descarga
            file_path = f"{search_results[selection].title}_E{anime_details.episodes[episode_choice].id}.mp4"
            fetch_video(video_url, file_path)

        play_choice = input("¿Quieres reproducir este episodio? (s/n): ")
        if play_choice.lower() == 's':
            if download_choice.lower() != 's':
                file_path = input("Introduce la ruta del archivo de video: ")
            play_video(file_path)

    except Exception as e:
        print(f'Error: {e}')
