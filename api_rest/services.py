import requests
from datetime import datetime

class OpenF1Service:
    BASE_URL = "https://api.openf1.org/v1"

    @staticmethod
    def get_proximas_corridas(limit=4):
        # Busca as próximas corridas de 2026
        url = f"{OpenF1Service.BASE_URL}/sessions?session_name=Race&year=2026"

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

            # Retorna as 4 primeiro encontradas
            return proximas[:limit]

        except Exception as e:
            print(f"Erro ao buscar próximas corridas: {e}")
            return []

    @staticmethod
    def listar_pilotos_atuais():
        url = f"{OpenF1Service.BASE_URL}/drivers?session_key=latest"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            pilotos = response.json()
            return pilotos
        except Exception as e:
            print(f"Erro ao buscar pilotos: {e}")
            return []

    @staticmethod
    def grid_resultado_corrida():
        url = f"{OpenF1Service.BASE_URL}/session_result?session_key=latest"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return []

    @staticmethod
    def listar_campeonato_detalhado():
        drivers_url = f"{OpenF1Service.BASE_URL}/drivers?session_key=latest"
        drivers_data = requests.get(drivers_url).json()

        standings_url = f"{OpenF1Service.BASE_URL}/championship_drivers?session_key=latest" 
        standings_data = requests.get(standings_url).json()

        pontos_map = {item['driver_number']: item for item in standings_data}
        
        grid_completo = []
        for driver in drivers_data:
            num = driver['driver_number']
            if num in pontos_map:
                driver['points_current'] = pontos_map[num].get('points_current', 0)
                driver['position_current'] = pontos_map[num].get('position_current', '-')
                driver['points_current'] = pontos_map[num].get('points_current', 0) - pontos_map[num].get('points_previous', 0)
                grid_completo.append(driver)
        return sorted(grid_completo, key=lambda x: x.get('points_current', 999), reverse=True)
