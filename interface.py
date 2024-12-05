#importação das bibliotecas e dependências que serão utilizadas no projeto
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # Biblioteca para manipulação de imagens
import requests  # Biblioteca para realizar requisições HTTP
from conversor import ApiConverte, cotacaoAtual, Moedas  # Importando funções e classes específicas do projeto

# Cria uma variável que recebe um vetor (lista) de moedas disponíveis no programa
moedasDisponiveis = Moedas()

# Cria uma interface gráfica onde o programa irá rodar
# Biblioteca tkinter não é nativa do Python para GUIs, mas totalmente construída com Python
def iniciarInterface():
    # Cria a janela principal do programa com título e configurações iniciais
    janela = tk.Tk()
    janela.title("Conversor de Moedas")
    janela.geometry("400x500")  # Define as dimensões iniciais da janela
    janela.configure(bg="white")  # Define o fundo da janela como branco

    # Configurações de estilo para a interface gráfica, baseadas em classes de widgets
    estilo = ttk.Style()
    estilo.configure('TLabel', font=('Helvetica', 12), background='white', foreground='black')  # Estilo para rótulos
    estilo.configure('TButton', font=('Helvetica', 12), padding=6)  # Estilo para botões
    estilo.configure('TCombobox', font=('Helvetica', 12), padding=5)  # Estilo para comboboxes
    estilo.map('TButton', foreground=[('active', 'white')], background=[('active', 'blue')])  # Estilo dinâmico para botões
    estilo.configure('TFrame', background='white')  # Estilo para os frames

    # Bloco de tratamento de exceções para o carregamento da imagem da logo
    try:
        # Carrega e redimensiona a imagem da logo para exibição na interface
        logoImage = Image.open("./assets/logo.png")
        logoImage = logoImage.resize((250, 150), Image.Resampling.LANCZOS)
        logo = ImageTk.PhotoImage(logoImage)  # Converte a imagem para uso no tkinter
        # Adiciona a imagem à janela principal
        logoLabel = ttk.Label(janela, image=logo, style='TLabel')
        logoLabel.image = logo  # Armazena referência para evitar descarte
        logoLabel.pack(pady=0)  # Adiciona espaçamento vertical
    except Exception as e:
        # Exibe uma mensagem no console em caso de falha no carregamento da logo
        print(f"Erro ao carregar a logo: {e}")

    # Criação de um frame (container) para os campos de entrada
    frameInputs = ttk.Frame(janela, padding=(10, 0), style='TFrame')
    frameInputs.pack(expand=True, fill='x')  # Configura o preenchimento horizontal do frame

    # Configura a largura uniforme das colunas no frame
    for i in range(3):
        frameInputs.grid_columnconfigure(i, weight=1, uniform="col")

    # Campo para entrada de valor
    ttk.Label(frameInputs, text="Valor:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entradaValor = ttk.Entry(frameInputs, font=('Helvetica', 12))  # Campo de texto para valor
    entradaValor.grid(row=0, column=1, padx=10, pady=5, sticky="ew")  # Preenchimento horizontal

    # Campo para seleção da moeda de origem
    ttk.Label(frameInputs, text="De:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    comboDe = ttk.Combobox(frameInputs, values=moedasDisponiveis, state="readonly")  # Combobox para moedas de origem
    comboDe.set("Escolha a moeda de origem")  # Placeholder padrão
    comboDe.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    # Campo para seleção da moeda de destino
    ttk.Label(frameInputs, text="Para:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    comboPara = ttk.Combobox(frameInputs, values=moedasDisponiveis, state="readonly")  # Combobox para moedas de destino
    comboPara.set("Escolha a moeda de destino")  # Placeholder padrão
    comboPara.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    # Frame para exibir os resultados
    frameResultado = ttk.Frame(janela, padding=(10, 0), style='TFrame')
    frameResultado.pack(fill="x", pady=10)

    # Rótulo para exibir o resultado da conversão
    resultadoLabel = ttk.Label(frameResultado, text="", font=('Helvetica', 12))
    resultadoLabel.pack(pady=5)

    # Espaçamento adicional para separar o resultado e a cotação
    espacamentoLabel = ttk.Label(frameResultado, text="", font=('Helvetica', 1))
    espacamentoLabel.pack(pady=5)

    # Rótulo para exibir a cotação atual da moeda
    cotacaoLabel = ttk.Label(frameResultado, text="", font=('Helvetica', 10))
    cotacaoLabel.pack(pady=5)

    # Função para realizar a conversão
    def converter():
        try:
            # Obtém o valor inserido no campo de texto
            valorStr = entradaValor.get().strip()
            if not valorStr:
                raise ValueError("O campo de valor não pode estar vazio.")
            valor = float(valorStr.replace(',', '.'))  # Converte o valor para ponto flutuante

            # Obtém as moedas de origem e destino selecionadas
            moedaDe = comboDe.get().split(" - ")[0]
            moedaPara = comboPara.get().split(" - ")[0]

            # Valida se ambas as moedas foram selecionadas
            if not moedaDe or not moedaPara:
                raise ValueError("Por favor, selecione as moedas de origem e destino.")

            # Realiza a conversão chamando a API
            resultado = ApiConverte(valor, moedaDe, moedaPara)
            resultadoLabel.config(text=f"{valor:.2f} {moedaDe} = {resultado:.2f} {moedaPara}")

            # Obtém a cotação atual da moeda
            cotacao = cotacaoAtual(moedaDe, moedaPara)
            if isinstance(cotacao, str):  # Valida se ocorreu um erro
                cotacaoLabel.config(text=f"Erro ao obter cotação: {cotacao}")
            else:
                cotacaoLabel.config(text=f"Cotação atual: 1 {moedaDe} = {cotacao:.2f} {moedaPara}")

        except ValueError as ve:
            # Exibe mensagens de erro relacionadas a validações de entrada
            resultadoLabel.config(text=f"Erro: {str(ve)}")
        except Exception as e:
            # Exibe mensagens de erro para outros problemas inesperados
            resultadoLabel.config(text=f"Erro inesperado: {e}")

    # Botão para executar a conversão
    botaoConverter = ttk.Button(janela, text="Converter", command=converter)
    botaoConverter.pack(pady=15)

    # Inicia o loop principal da interface gráfica
    janela.mainloop()

# Inicia a interface chamando a função principal
iniciarInterface()
