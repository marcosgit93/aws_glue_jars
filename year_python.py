# Função para verificar se o ano é bissexto
def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


# Iteração pelos dias, meses e anos
for year in range(2023, 2024):  # Anos de 2023 a 2023
    for month in range(1, 13):  # Meses de 1 a 12
        days_in_month = 31  # Maioria dos meses têm 31 dias por padrão

        if month == 2:  # Fevereiro tem 28 ou 29 dias dependendo se é um ano bissexto
            if is_leap_year(year):
                days_in_month = 29
            else:
                days_in_month = 28
        elif month in [4, 6, 9, 11]:  # Abril, junho, setembro e novembro têm 30 dias
            days_in_month = 30

        for day in range(1, days_in_month + 1):  # Dias de 1 até o número de dias no mês
            # Formatar o dia e o mês com zero à esquerda se necessário
            formatted_day = str(day).zfill(2)
            formatted_month = str(month).zfill(2)

            # Imprimir a data
            print(f"Data: {formatted_day}/{formatted_month}/{year}")
