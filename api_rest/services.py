import requests
from datetime import datetime

class OpenF1Service:
    BASE_URL = "https://api.openf1.org/v1/sessions"

    @staticmethod
    def get_proximas_corridas(limit=4):
        # Busca as próximas corridas de 2026
        url = f"{OpenF1Service.BASE_URL}?session_name=Race&year=2026"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            todas_corridas = response.json()
            agora = datetime.now().isoformat() # Convertendo para ISO para comparação

            #Filtro: apenas corridas futuras onde a data de início é maior que agora
            proximas = [
                corrida for corrida in todas_corridas 
                if corrida.get('date_start') > agora 
            ]

            proximas.sort(key=lambda x: x.get('date_start'))

            # Retornamos as primeiras 4 encontradas
            return proximas[:limit]

        except Exception as e:
            print(f"Erro ao buscar próximas corridas: {e}")
            return []
