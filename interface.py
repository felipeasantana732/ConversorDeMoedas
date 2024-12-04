import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import requests
from conversor import ApiConverte, cotacaoAtual

moedasDisponiveis = [
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

def iniciarInterface():
    janela = tk.Tk()
    janela.title("Conversor de Moedas")
    janela.geometry("400x500")
    janela.configure(bg="white")

    estilo = ttk.Style()
    estilo.configure('TLabel', font=('Helvetica', 12), background='white', foreground='black')
    estilo.configure('TButton', font=('Helvetica', 12), padding=6)
    estilo.configure('TCombobox', font=('Helvetica', 12), padding=5)
    estilo.map('TButton', foreground=[('active', 'white')], background=[('active', 'blue')])
    estilo.configure('TFrame', background='white')

    try:
        logoImage = Image.open("./assets/logo.png")
        logoImage = logoImage.resize((250, 150), Image.Resampling.LANCZOS)
        logo = ImageTk.PhotoImage(logoImage)
        logoLabel = ttk.Label(janela, image=logo, style='TLabel')
        logoLabel.image = logo
        logoLabel.pack(pady=0)
    except Exception as e:
        print(f"Erro ao carregar a logo: {e}")

    frameInputs = ttk.Frame(janela, padding=(10, 0), style='TFrame')
    frameInputs.pack(expand=True, fill='x')

    for i in range(3):
        frameInputs.grid_columnconfigure(i, weight=1, uniform="col")

    ttk.Label(frameInputs, text="Valor:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entradaValor = ttk.Entry(frameInputs, font=('Helvetica', 12))
    entradaValor.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    ttk.Label(frameInputs, text="De:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    comboDe = ttk.Combobox(frameInputs, values=moedasDisponiveis, state="readonly")
    comboDe.set("Escolha a moeda de origem")
    comboDe.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    ttk.Label(frameInputs, text="Para:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    comboPara = ttk.Combobox(frameInputs, values=moedasDisponiveis, state="readonly")
    comboPara.set("Escolha a moeda de destino")
    comboPara.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    frameResultado = ttk.Frame(janela, padding=(10, 0), style='TFrame')
    frameResultado.pack(fill="x", pady=10)

    resultadoLabel = ttk.Label(frameResultado, text="", font=('Helvetica', 12))
    resultadoLabel.pack(pady=5)

    espacamentoLabel = ttk.Label(frameResultado, text="", font=('Helvetica', 1))
    espacamentoLabel.pack(pady=5)

    cotacaoLabel = ttk.Label(frameResultado, text="", font=('Helvetica', 10))
    cotacaoLabel.pack(pady=5)

    def converter():
        try:
            valorStr = entradaValor.get().strip()
            if not valorStr:
                raise ValueError("O campo de valor não pode estar vazio.")
            valor = float(valorStr.replace(',', '.'))

            moedaDe = comboDe.get().split(" - ")[0]
            moedaPara = comboPara.get().split(" - ")[0]

            if not moedaDe or not moedaPara:
                raise ValueError("Por favor, selecione as moedas de origem e destino.")

            resultado = ApiConverte(valor, moedaDe, moedaPara)
            resultadoLabel.config(text=f"{valor:.2f} {moedaDe} = {resultado:.2f} {moedaPara}")

            cotacao = cotacaoAtual(moedaDe, moedaPara)
            if isinstance(cotacao, str):
                cotacaoLabel.config(text=f"Erro ao obter cotação: {cotacao}")
            else:
                cotacaoLabel.config(text=f"Cotação atual: 1 {moedaDe} = {cotacao:.2f} {moedaPara}")

        except ValueError as ve:
            resultadoLabel.config(text=f"Erro: {str(ve)}")
        except Exception as e:
            resultadoLabel.config(text=f"Erro inesperado: {e}")

    botaoConverter = ttk.Button(janela, text="Converter", command=converter)
    botaoConverter.pack(pady=15)

    janela.mainloop()

iniciarInterface()
