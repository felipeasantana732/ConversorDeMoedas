import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # Para trabalhar com imagens
import requests  # Para fazer solicitações HTTP
from conversor import ApiConverte, cotacaoAtual

# Lista de moedas disponíveis
moedas_disponiveis = [
    "USD - Dólar Americano",
    "EUR - Euro",
    "BRL - Real Brasileiro",
    "JPY - Iene Japonês",
    "GBP - Libra Esterlina",
    "AUD - Dólar Australiano",
    "CAD - Dólar Canadense",
    "CHF - Franco Suíço",
    "CNY - Yuan Chinês",
    "INR - Rúpia Indiana",
    "BTC - Bitcoin"
]

# Função para obter a cotação atual da moeda


# Função para iniciar a interface
def iniciar_interface():
    janela = tk.Tk()
    janela.title("Conversor de Moedas")
    janela.geometry("400x500")
    janela.configure(bg="white")

    # Definindo o estilo dos widgets
    estilo = ttk.Style()
    estilo.configure('TLabel', font=('Helvetica', 12), background='white', foreground='black')
    estilo.configure('TButton', font=('Helvetica', 12), padding=6)
    estilo.configure('TCombobox', font=('Helvetica', 12), padding=5)
    estilo.map('TButton', foreground=[('active', 'white')], background=[('active', 'blue')])
    estilo.configure('TFrame', background='white')

    # Adicionando a logo
    try:
        logo_image = Image.open("./assets/logo.png")
        logo_image = logo_image.resize((250, 150), Image.Resampling.LANCZOS)
        logo = ImageTk.PhotoImage(logo_image)
        logo_label = ttk.Label(janela, image=logo, style='TLabel')
        logo_label.image = logo
        logo_label.pack(pady=0)
    except Exception as e:
        print(f"Erro ao carregar a logo: {e}")

    # Frame para inputs
    frame_inputs = ttk.Frame(janela, padding=(10, 0), style='TFrame')
    frame_inputs.pack(expand=True, fill='x')

    for i in range(3):
        frame_inputs.grid_columnconfigure(i, weight=1, uniform="col")

    ttk.Label(frame_inputs, text="Valor:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entrada_valor = ttk.Entry(frame_inputs, font=('Helvetica', 12))
    entrada_valor.grid(row=0, column=1, padx=10, pady=5, sticky="ew")  # 'ew' para preencher horizontalmente

    ttk.Label(frame_inputs, text="De:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    combo_de = ttk.Combobox(frame_inputs, values=moedas_disponiveis, state="readonly")
    combo_de.set("Escolha a moeda de origem")
    combo_de.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    ttk.Label(frame_inputs, text="Para:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    combo_para = ttk.Combobox(frame_inputs, values=moedas_disponiveis, state="readonly")
    combo_para.set("Escolha a moeda de destino")
    combo_para.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    # Frame para mostrar o resultado
    frame_resultado = ttk.Frame(janela, padding=(10, 0), style='TFrame')
    frame_resultado.pack(fill="x", pady=10)

    resultado_label = ttk.Label(frame_resultado, text="", font=('Helvetica', 12))
    resultado_label.pack(pady=5)

    espaçamento_label = ttk.Label(frame_resultado, text="", font=('Helvetica', 1))
    espaçamento_label.pack(pady=5)

    cotacao_label = ttk.Label(frame_resultado, text="", font=('Helvetica', 10))
    cotacao_label.pack(pady=5)
    
    def converter():
        try:
            valor_str = entrada_valor.get().strip()
            if not valor_str:
                raise ValueError("O campo de valor não pode estar vazio.")
            valor = float(valor_str.replace(',', '.'))

            moeda_de = combo_de.get().split(" - ")[0]
            moeda_para = combo_para.get().split(" - ")[0]

            if not moeda_de or not moeda_para:
                raise ValueError("Por favor, selecione as moedas de origem e destino.")

            resultado = ApiConverte(valor, moeda_de, moeda_para)

            # Atualiza o label de resultado com o valor convertido
            resultado_label.config(text=f"{valor:.2f} {moeda_de} = {resultado:.2f} {moeda_para}")

            # Obtendo a cotação atual
            cotacao = cotacaoAtual(moeda_de, moeda_para)
            if isinstance(cotacao, str):
                cotacao_label.config(text=f"Erro ao obter cotação: {cotacao}")
            else:
                cotacao_label.config(text=f"Cotação atual: 1 {moeda_de} = {cotacao:.2f} {moeda_para}")

        except ValueError as ve:
            resultado_label.config(text=f"Erro: {str(ve)}")
        except Exception as e:
            resultado_label.config(text=f"Erro inesperado: {e}")

    # Botão de conversão
    botao_converter = ttk.Button(janela, text="Converter", command=converter)
    botao_converter.pack(pady=15)

    janela.mainloop()

iniciar_interface()
