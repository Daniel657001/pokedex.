# Importar os módulos necessários
import tkinter as tk                      # Para criar a interface gráfica
from tkinter import messagebox            # Para mostrar mensagens de erro
from PIL import Image, ImageTk            # Para tratar e mostrar imagens
import requests                           # Para fazer pedidos HTTP à API
from io import BytesIO                    # Para tratar imagem recebida como fluxo de bytes

# Função que vai buscar os dados do Pokémon à API
def buscar_pokemon():
    nome = entry_nome.get().lower()  # Obter o texto inserido e converter para minúsculas
    url = f"https://pokeapi.co/api/v2/pokemon/{nome}"  # Construir URL para o pedido à API

    resposta = requests.get(url)  # Fazer o pedido GET
    if resposta.status_code == 200:  # Se a resposta for bem sucedida
        dados = resposta.json()  # Converter os dados da resposta para JSON

        # Obter e formatar o nome e os tipos do Pokémon
        nome_pokemon = dados['name'].capitalize()  # Capitalizar o nome
        tipos = ", ".join([tipo['type']['name'].capitalize() for tipo in dados['types']])  # Juntar os tipos
        label_info.config(text=f"Nome: {nome_pokemon}\nTipos: {tipos}")  # Atualizar o texto da label com as infos

        # Obter o URL da imagem do Pokémon (sprite frontal)
        img_url = dados['sprites']['front_default']
        if img_url:
            img_resposta = requests.get(img_url)  # Fazer o download da imagem
            img_data = Image.open(BytesIO(img_resposta.content))  # Abrir a imagem a partir dos bytes
            img_data = img_data.resize((300, 300), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img_data)  # Converter para formato compatível com tkinter
            label_imagem.config(image=img_tk)  # Atualizar o rótulo com a nova imagem
            label_imagem.image = img_tk  # Guardar referência para não ser apagada
        else:
            label_imagem.config(image='', text='Sem imagem disponível')
    else:
        # Se o Pokémon não for encontrado (erro 404, por exemplo)
        messagebox.showerror("Erro", "Pokémon não encontrado!")

# Criar a janela principal da aplicação
janela = tk.Tk()
janela.title("Pokédex")  # Título da janela
janela.geometry("500x600")
# Campo de entrada de texto para o nome do Pokémon
entry_nome = tk.Entry(font=("Arial", 14))
entry_nome.place(x=150, y=50)


#label's da pokedex (design)
label = tk.Label(janela, bg= "#FF0000")


label_ecra = tk.Label(janela, width=50, bg= "#808080")
label_ecra.place(x=90, y= 120)

label_ecra = tk.Label(janela,width=2, height=25, bg= "#808080")
label_ecra.place(x=90, y= 120)

label_ecra = tk.Label(janela, width=50, bg= "#808080")
label_ecra.place(x=91, y= 500)

label_ecra = tk.Label(janela,width=2, height=26, bg= "#808080")
label_ecra.place(x=440, y= 120)

# Botão para iniciar a busca
botao_buscar = tk.Button(janela, text="Buscar", command=buscar_pokemon)
botao_buscar.pack(pady=5)

# Label para mostrar a imagem do Pokémon
label_imagem = tk.Label(janela)
label_imagem.place(x=110, y=150)

# Label para mostrar informações como nome e tipo
label_info = tk.Label(janela, font=("Arial", 12), justify="left")
label_info.place(x=200, y=400)

# Iniciar o loop principal da aplicação (interface gráfica)
janela.mainloop()

