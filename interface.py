import tkinter as tk
from tkinter import messagebox
from conversor import converte_moeda



def iniciar_interface():
    janela = tk.Tk()
    janela.title("Conversor de Moedas")
    janela.geometry("400x400")

    tk.Label(janela, text="Valor:").grid(row=0, column=0, padx=10, pady=10)
    entrada_valor = tk.Entry(janela)
    entrada_valor.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(janela, text="De (ex: USD):").grid(row=1, column=0, padx=10, pady=10)
    entrada_de = tk.Entry(janela)
    entrada_de.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(janela, text="Para (ex: BRL):").grid(row=2, column=0, padx=10, pady=10)
    entrada_para = tk.Entry(janela)
    entrada_para.grid(row=2, column=1, padx=10, pady=10)

    def acao_converter():
        try:
            valor = float(entrada_valor.get())
            moeda_de = entrada_de.get().upper()
            moeda_para = entrada_para.get().upper()
            resultado = converte_moeda(valor, moeda_de, moeda_para)
            messagebox.showinfo("Resultado", f"{valor} {moeda_de} = {resultado:.2f} {moeda_para}")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    botao_converter = tk.Button(janela, text="Converter", command=acao_converter)
    botao_converter.grid(row=3, column=0, columnspan=2, pady=20)

    janela.mainloop()
