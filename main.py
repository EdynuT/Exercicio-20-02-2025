import json
import os

ARQUIVO_TAREFAS = 'tarefas.json'

base_de_tarefas = {}

def carregar_tarefas():
    global base_de_tarefas
    if os.path.exists(ARQUIVO_TAREFAS):
        with open(ARQUIVO_TAREFAS, 'r') as arquivo:
            try:
                base_de_tarefas = json.load(arquivo)
            except json.JSONDecodeError:
                print('Erro ao ler o arquivo')
                base_de_tarefas = {}

def salvar_tarefas():
    with open(ARQUIVO_TAREFAS, 'w') as arquivo:
        json.dump(base_de_tarefas, arquivo, indent=4)

def obter_novo_codigo():
    if base_de_tarefas:
        return max(int(codigo) for codigo in base_de_tarefas.keys()) + 1
    return 1

def criar_tarefa(nome_usuario, prioridade, descricao_tarefa):
    codigo = str(obter_novo_codigo())
    tarefa = {
        "codigo": codigo,
        "nome_usuario": nome_usuario,
        "nivel_prioridade": int(prioridade),
        "descricao_tarefa": descricao_tarefa,
        "status": "pendente"
    }
    base_de_tarefas[codigo] = tarefa
    print(f"A tarefa do(a) usuário(a) {nome_usuario} foi criada com sucesso!")
    salvar_tarefas()

def buscar_tarefa_codigo(codigo):
    return base_de_tarefas.get(codigo, None)

def buscar_tarefa_descricao(descricao):
    return [tarefa for tarefa in base_de_tarefas.values() if descricao in tarefa['descricao_tarefa']]

def remover_tarefa(codigo):
    if codigo in base_de_tarefas:
        del base_de_tarefas[codigo]
        salvar_tarefas()
        print("Tarefa removida com sucesso!")
    else:
        print("Tarefa não encontrada.")

def listar_tarefas_prioridade():
    for codigo in base_de_tarefas:
        print(f"Código: {codigo} - {base_de_tarefas[codigo]}")

def mostrar_estatisticas():
    total = len(base_de_tarefas)
    pendentes = sum(1 for t in base_de_tarefas.values() if t['status'] == 'pendente')
    finalizadas = total - pendentes
    print(f"Total de tarefas: {total}\nPendentes: {pendentes}\nFinalizadas: {finalizadas}")

def limpar_tarefas():
    global base_de_tarefas
    base_de_tarefas = {}
    salvar_tarefas()
    print("Todas as tarefas foram removidas.")

def menu_principal():
    carregar_tarefas()
    while True:
        print('''\nMenu de Tarefas\n
1- Criar nova tarefa.
2- Buscar tarefa.
3- Listar todas as tarefas por prioridade.
4- Remover tarefa finalizada.
5- Mostrar estatísticas das tarefas.
6- Limpar todas as tarefas.
7- Sair.\n''')
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            nome = input("Digite o nome do usuário: ")
            prioridade = input("Digite o nível de prioridade da tarefa: ")
            descricao = input("Digite a descrição da tarefa: ")
            criar_tarefa(nome, prioridade, descricao)
        elif opcao == "2":
            codigo = input("Digite o código da tarefa: ")
            tarefa = buscar_tarefa_codigo(codigo)
            if tarefa:
                print(f"Tarefa encontrada: {tarefa}")
            else:
                print("Tarefa não encontrada.")
        elif opcao == "3":
            listar_tarefas_prioridade()
        elif opcao == "4":
            codigo = input("Digite o código da tarefa a remover: ")
            remover_tarefa(codigo)
        elif opcao == "5":
            mostrar_estatisticas()
        elif opcao == "6":
            limpar_tarefas()
        elif opcao == "7":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

menu_principal()
