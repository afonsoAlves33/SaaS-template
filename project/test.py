def usuario_dados(nome:str, idade: int, **kwargs):
    print(f"Nome: {nome}")
    print(f"Idade: {idade}")
    email = kwargs.get('email', 'Email não fornecido')
    bairro = kwargs.get('bairro', 'Bairro não fornecido')
    print(f"Email: {email}")
    print(f"Bairro: {bairro}")

usuario_dados(nome="afonso", idade=18, email="afonso@gmail.com", bairro="novo mundo")