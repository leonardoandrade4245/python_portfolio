from tkinter import *
import pandas as pd
import requests
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

API_KEY = "14cff45182069bb3941ceec752a35e99"
CIDADE = "São Paulo"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CIDADE}&appid={API_KEY}&lang=pt_br&units=metric"

class Aplicacao:
    def __init__(self):
        # Criando a interface
        self.layout = Tk()
        self.layout.title("Dados do Clima-Tempo")
        self.layout.geometry("800x600")
        
        # Configurando o fundo da janela principal
        self.layout.configure(bg="lightblue")
        
        # Criando o Frame dentro da janela
        self.tela = Frame(self.layout, bg="lightblue")
        
        # Inicializando a lista para armazenar as temperaturas e horários
        self.dados_temperatura = []
        
        # Criando os elementos na tela
        self.titulo_interface = Label(self.tela, text="Veja o clima Tempo Atual.", fg="black", bg="lightblue", pady=10, font=("Arial", 16, "bold"))
        self.clima_atual = Label(self.tela, text=f"Clima atual: -°C", bg="lightblue", font=("Arial", 14))
        self.status_atual = Label(self.tela, text=f"Status da umidade atual: -", bg="lightblue", font=("Arial", 14))
        
        # Criando o botão com bordas arredondadas
        self.exportar_clima = Button(self.tela, text="Salvar", command=self.exportar_arquivo, relief="flat", bg="white", bd=0, highlightbackground="black", activebackground="black", font=("Arial", 14), width=15, height=2, padx=10, pady=5)
        self.gerar_grafico = Button(self.tela, text="Gerar Gráfico", command=self.gerar_grafico, relief="flat", bg="white", bd=0, highlightbackground="black", activebackground="black", font=("Arial", 14), width=15, height=2, padx=10, pady=5)

        # Posicionando elementos na tela
        self.tela.pack(fill=BOTH, expand=True)
        self.titulo_interface.pack(pady=20)
        self.clima_atual.pack_forget()
        self.status_atual.pack_forget()
        self.exportar_clima.pack(pady=20)
        self.gerar_grafico.pack(pady=10)

        # Inicializando a variável para o gráfico
        self.canvas_grafico = None
        self.figura = None

        mainloop()

    def atualizar_dados_clima(self):
        """ Obtém os dados da API e armazena na classe """
        resposta = requests.get(URL)
        dados = resposta.json()

        # Obtém informações do clima
        self.temperatura = dados["main"]["temp"]
        self.descricao = dados["weather"][0]["description"]
        self.data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")

    def exportar_arquivo(self):
        """ Exporta os dados climáticos para um CSV sem substituir os dados existentes """
        # Atualiza os dados do clima antes de exportar
        self.atualizar_dados_clima()

        # Exibe as labels de clima após o botão salvar ser clicado
        self.clima_atual.config(text=f"Clima atual: {self.temperatura}°C")
        self.status_atual.config(text=f"Status da umidade atual: {self.descricao.capitalize()}")

        self.clima_atual.pack(pady=10)
        self.status_atual.pack(pady=10)

        # Adiciona a nova medição ao gráfico e à lista de dados
        self.dados_temperatura.append((self.data_hora, self.temperatura))

        # Salvando no arquivo CSV
        dados = pd.DataFrame(
            {
                'Data e Hora': [self.data_hora],
                'Cidade': [CIDADE],
                'Temperatura (°C)': [self.temperatura],
                'Descrição': [self.descricao.capitalize()]
            }
        )

        # Abrindo o arquivo no modo append ('a') para adicionar os dados ao invés de substituir
        dados.to_csv('clima_exportado.csv', mode='a', header=False, index=False)

        print("Arquivo salvo com sucesso!")

    def gerar_grafico(self):
        """ Gera o gráfico da Temperatura ao longo do tempo """
        # Lê o arquivo CSV
        dados_csv = pd.read_csv('clima_exportado.csv')

        # Converte a coluna 'Data e Hora' para datetime
        dados_csv['Data e Hora'] = pd.to_datetime(dados_csv['Data e Hora'], format="%d/%m/%Y %H:%M")

        # Cria o gráfico
        plt.figure(figsize=(10, 6))
        plt.plot(dados_csv['Data e Hora'], dados_csv['Temperatura (°C)'], marker='o', color='b', label='Temperatura')
        plt.title('Temperatura ao Longo do Tempo', fontsize=16)
        plt.xlabel('Data e Hora', fontsize=12)
        plt.ylabel('Temperatura (°C)', fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(True)

        # Altera o fundo do gráfico para azul claro
        self.figura = plt.gcf()
        self.figura.patch.set_facecolor('lightblue')  # Altera o fundo para azul claro

        # Usa o tight_layout para ajustar o layout e evitar cortes
        plt.tight_layout()

        # Converte a figura do gráfico para o formato compatível com o Tkinter
        if self.canvas_grafico:
            self.canvas_grafico.get_tk_widget().destroy()

        self.canvas_grafico = FigureCanvasTkAgg(self.figura, master=self.tela)
        self.canvas_grafico.get_tk_widget().pack(pady=20)
        self.canvas_grafico.draw()

# Iniciando a aplicação
tl = Aplicacao()
