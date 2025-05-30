import tkinter as tk                      # Para criar a interface gráfica
from tkinter import messagebox            # Para mostrar mensagens de erro
from PIL import Image, ImageTk            # Para tratar e mostrar imagens
import requests                           # Para fazer pedidos HTTP à API
from io import BytesIO                    # Para tratar imagem recebida como fluxo de bytes
import pygame                            # Para tocar sons
import tempfile                          # Para arquivo temporário
import os

# Inicializa o mixer do pygame
pygame.mixer.init()

# Variável global para guardar caminho do arquivo de som temporário
arquivo_som_temp = None

def buscar_pokemon():
    global arquivo_som_temp
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

        # Baixar o som para uso no botão
        poke_id = dados['id']
        som_url = f"https://raw.githubusercontent.com/PokeAPI/cries/main/cries/pokemon/latest/{poke_id}.ogg"

        try:
            som_resposta = requests.get(som_url)
            som_resposta.raise_for_status()

            # Remove o som antigo temporário se existir
            if arquivo_som_temp and os.path.exists(arquivo_som_temp):
                os.remove(arquivo_som_temp)

            # Salvar o som em arquivo temporário
            with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as tmp_file:
                tmp_file.write(som_resposta.content)
                arquivo_som_temp = tmp_file.name

            # Ativar botão de tocar som
            btn_tocar_som.config(state="normal")

        except Exception as e:
            print("Erro ao carregar som:", e)
            btn_tocar_som.config(state="disabled")

    else:
        # Se o Pokémon não for encontrado (erro 404, por exemplo)
        messagebox.showerror("Erro", "Pokémon não encontrado!")
        btn_tocar_som.config(state="disabled")
        label_info.config(text="")
        label_imagem.config(image='')

def tocar_som():
    global arquivo_som_temp
    if arquivo_som_temp:
        try:
            pygame.mixer.music.load(arquivo_som_temp)
            pygame.mixer.music.play()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível tocar o som:\n{e}")

# Criar a janela principal da aplicação
janela = tk.Tk()
janela.title("Pokédex")  # Título da janela
janela.geometry("500x600")
janela.configure(bg= "#FF0000")
# Campo de entrada de texto para o nome do Pokémon
entry_nome = tk.Entry(font=("Arial", 14))
entry_nome.place(x=120, y=50)


#label's da pokedex (design)
label = tk.Label(janela, bg= "#FF0000")


label_ecra = tk.Label(janela, width=50, bg= "#808080")
label_ecra.place(x=70, y= 120)
label_ecra = tk.Label(janela,width=2, height=25, bg= "#808080")
label_ecra.place(x=70, y= 120)

label_ecra = tk.Label(janela, width=52, bg= "#808080")
label_ecra.place(x=70, y= 500)

label_ecra = tk.Label(janela,width=2, height=26, bg= "#808080")
label_ecra.place(x=420, y= 120)


# Botão para iniciar a busca
botao_buscar = tk.Button(janela, text="Buscar", command=buscar_pokemon)
botao_buscar.pack(pady=5)

# Label para mostrar a imagem do Pokémon
label_imagem = tk.Label(janela, bg= "#FF0000")
label_imagem.place(x=110, y=150)

# Label para mostrar informações como nome e tipo
label_info = tk.Label(janela, font=("Arial", 12), justify="left", bg= "#FF0000")
label_info.place(x=200, y=525)

btn_tocar_som = tk.Button(janela, text="Tocar Som", font=("Arial", 16), bg="red", fg="white", command=tocar_som)
btn_tocar_som.pack(pady=10)


# Iniciar o loop principal da aplicação (interface gráfica)
janela.mainloop()
