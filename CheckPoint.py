import oracledb as orcl

# @Autor: def - Rafael Chaves - RM99643
# @Descrição: Limpa todos os caracteres deixando apenas os numéros
def toCleanCpf(cpf):
    # Remove qualquer caractere não numérico do CPF
    cpfClean = ''.join(filter(str.isdigit, cpf))
    return cpfClean



def alterar_registro(cursor):
    resp = 1
    while(resp != 0):
        print("0 - Sair")
        print("1 - Alterar o Professor")
        print("2 - Alterar o endereço do professor")
        opcao = int(input("Digite a sua opção (0-2): "))

        if(opcao == 0):
            resp = 0
        
        if(opcao == 1):
            lista_dados = []

            #Pegando o ID do professor
            id_professor = int(input("Digite o id do professor que deseja alterar: "))

            #Preparando o código que pega os dados
            query = f"""SELECT * FROM TB_PROFESSORES WHERE id = {id_professor}"""

            #Executando o código
            cursor.execute(query)
            
            #Pegando todos os resultados do código executado
            dados = cursor.fetchall()

            #Adicionando na lista
            for dado in dados:
                lista_dados.append(dado)

            if(len(lista_dados) == 0): #Se for vazio, não há nada o que fazer
                print("Não existe registros na tabela!")
            
            else:
                try:
                    #Pegando os novos valores
                    nome_professor = input("Nome: ")
                    cpf_professor = int(input("CPF: "))
                    idade_professor = int(input("Idade: "))
                    titualacao_max = input("Titulação: ")
                except ValueError:
                    print("Digite valores numéricos")
                except:
                    print("Erro de transação com o banco")
                else:
                    #Preparando o comando
                    alteracao = f"""UPDATE TB_PROFESSORES SET PROFESSOR_NOME = '{nome_professor}', PROFESSOR_CPF = {cpf_professor}, 
                                PROFESSOR_IDADE = {idade_professor}, PROFESSOR_TITULACAOMAX = '{titualacao_max}'"""
                    #Executando o comando
                    cursor.execute(alteracao)
                finally:
                    print("Professor alterado com sucesso!")

            resp = int(input("Deseja continuar (1-SIM/0-NÃO): "))

        if(opcao == 2):
            lista_dados_endereco = []

            #Pegando o ID do endereço
            id_endereco = int(input("Digite o id do endereço que deseja alterar: "))

            #Preparando o código que pega os dados
            query = f"""SELECT * FROM TB_ENDERECOS WHERE ENDERECO_ID = {id_endereco}"""

            #Executando o código
            cursor.execute(query)
            
            #Pegando os resultados
            enderecos = cursor.fetchall()

            #Adicionando-os na lista
            for endereco in enderecos:
                lista_dados_endereco.append(endereco)

            if(len(lista_dados_endereco) == 0): #Se for vazio, não há nada o que fazer
                print("Não há registros na tabela!")

            else:
                try:
                    #Pegando os novos valores
                    logradouro = input("Nome: ")
                    bairro = input("Bairro: ")
                    cidade = input("Cidade: ")
                    estado = input("Estado: ")
                    cep = input("CEP: ")
                except ValueError:
                    print("Digite valores numéricos")
                except:
                    print("Erro de transação com o banco")
                else:
                    #Preparando o comando
                    alteracao = f"""UPDATE TB_ENDERECOS SET ENDERECO_LOGRADOURO = '{logradouro}', ENDERECO_BAIRRO = '{bairro}', 
                                ENDERECO_CIDADE = '{cidade}', ENDERECO_ESTADO = '{estado}, ENDERECO_CEP = '{cep}'"""
                    #Executando o comando
                    cursor.execute(alteracao)
                finally:
                    print("Professor alterado com sucesso!")

            resp = int(input("Deseja continuar (1-SIM/0-NÃO): "))




# @Autor: def - Rafael Chaves - RM99643
# @Descrição: Método que deleta os dados no banco de dados Oracle 
def deleteRecord(script):
    while True:
        try:
            # Escolha(1-4) para decidir como que quer deletar os dados
            print("1 - Deseja deletar os dados referente ao Professor especifico?")
            print("2 - Deseja deletar os dados referente ao endereço do Professor?")
            print("3 - Deseja deletar todos os dados referente a uma conta de um professor?")
            print("4 - Deseja sair?")
            option = int(input("Digite a opção que deseja(1-4): "))

            # Solicitando CPF do Professor para que seja feita o delete com o filtro certo
            IcpfProfessor = input("Digite o CPF referente ao Professor que deseja deletar os dados: ")

            # Limpar o CPF removendo a pontuação e mantendo apenas os números
            cpf_professor = toCleanCpf(IcpfProfessor)

            # Verificar se o CPF possui 11 dígitos após a limpeza
            if len(cpf_professor) == 11:
                # Opção 1 - Deleta os dados do Professor escolhido
                if(option == 1):
                    # Verificar se o CPF possui 11 dígitos após a limpeza
                    if len(cpf_professor) == 11:
                        # Preparar o comando SQL de exclusão
                        scriptDelete = f"DELETE FROM TB_PROFESSORES WHERE PROFESSOR_CPF = {cpf_professor};"
                        
                        # Executar o comando de exclusão
                        script.execute(scriptDelete)

                        # Confirmar a transação
                        script.connection.commit()

                        # Print para confirmar a exclusão
                        print(f"Registro da tabela 'TB_PROFESSORES' excluído com sucesso.")
                    else:
                        # Se o cpf entrar errado
                        print(f"Cpf '{cpf_professor}' inválido!")

                # Opção 2 - Deleta os dados do Endereço escolhido
                elif (option == 2):
                    try:
                        # Preparar o comando SQL para consultar os endereços do professor com base no CPF
                        scriptSelect = f"""
                            SELECT P.PROFESSOR_CPF, E.ENDERECO_LOGRADOURO, E.ENDERECO_BAIRRO, E.ENDERECO_CIDADE, E.ENDERECO_ESTADO, E.ENDERECO_CEP FROM TB_PROFESSORES P
                            JOIN TB_ENDERECOS E 
                                ON P.PROFESSOR_ID = E.PROFESSOR_ID
                                WHERE P.PROFESSOR_CPF = '{cpf_professor}';
                        """
                        
                        # Executar o comando de seleção
                        script.execute(scriptSelect)
                        
                        # Pegar todos os endereços relacionados a esse CPF
                        enderecosProfessor = script.fetchall()
                        
                        if len(enderecosProfessor) != 0:
                            # Listar os endereços e permitir que o usuário escolha qual endereço excluir
                            print(f"Endereços relacionados a este CPF '{cpf_professor}': ")
                            for i, endereco in enumerate(enderecosProfessor):
                                print(f"{i + 1} - {endereco}")  # listar o(s) endereço(s) completo(s)

                            escolhaEndereco = int(input("Digite o número do endereço que deseja excluir: ")) - 1

                            if 0 <= escolhaEndereco < len(enderecosProfessor):
                                # Obter o ID do endereço selecionado
                                endereco_id = enderecosProfessor [escolhaEndereco] [0]

                                # Preparar o comando SQL de exclusão do endereço com base no ID
                                scriptDeleteEndereco = f"DELETE FROM ENDERECOS WHERE ENDERECO_ID = {endereco_id};"

                                # Executar o comando de exclusão
                                script.execute(scriptDeleteEndereco)

                                # Confirmar a transação
                                script.connection.commit()

                                print(f"Endereço excluído com sucesso.")
                            else:
                                print("Escolha de endereço inválida.")
                        else:
                            print(f"Nenhum endereço encontrado para o CPF: '{cpf_professor}'.")
                    except Exception as e:
                        print(f"Erro ao excluir registros: {e}")

                # Opção 3 - Deleta todos os dados do Professor e endereço escolhido
                elif (option == 3):
                    try:
                        # Preparar o comando SQL para consultar o Id do professor com base no CPF
                        scriptSearchId = f""" 
                            SELECT P.PROFESSOR_ID FROM TB_PROFESSORES P
                            JOIN TB_ENDERECOS E 
                                ON P.PROFESSOR_ID = E.PROFESSOR_ID
                                WHERE P.PROFESSOR_CPF = '{cpf_professor}';
                        """

                        # Executar o comando de exclusão
                        script.execute(scriptSearchId)
      
                        # Pegar o ID do professor
                        professor_id = script.fetchone()

                        if professor_id:
                            # Faz um Transactional para deletar todos os dados referente ao CPF selecionado
                            scriptDeleteAll = f"""
                                BEGIN
                                    EXECUTE IMMEDIATE 'ALTER TABLE TB_ENDERECOS DISABLE CONSTRAINT FK_tbProfessor';
                                    
                                    DELETE FROM TB_PROFESSORES
                                        WHERE PROFESSOR_ID = {scriptSearchId[0]};
                                    DELETE FROM TB_ENDERECOS
                                        WHERE PROFESSOR_ID = {scriptSearchId[0]};
                                        
                                    EXECUTE IMMEDIATE 'ALTER TABLE TB_ENDERECOS ENABLE CONSTRAINT FK_tbProfessor';
                                    COMMIT;
                                END;
                                /
                            """

                            script.execute(scriptDeleteAll)
                            print(f"Todos os dados referentes ao CPF {cpf_professor} foram excluídos com sucesso.")
                        else:
                            print(f"Não foi encontrado nenhum dado referente ao cpf: {cpf_professor}")
                    except Exception as e:
                        print(f"Erro ao excluir registros: {e}")
              
            else:
                # Se o cpf entrar errado
                print(f"Cpf '{cpf_professor}' inválido!")

            if (option == 4):
                print("Saindo...")
                break 
        
        except Exception as e:
            print(f"Erro ao excluir registros: {e}")


       

def conecta_BD():
    try:
        #conectar com o Servidor
        str_conect = orcl.makedsn("oracle.fiap.com.br", "1521", "ORCL")
        #efetuar a conexao com o usuario
        conect = orcl.connect(user="RM99173", password="240102", dsn=str_conect)

        #Criar as instrucoes para cada modulo
        inst_SQL = conect.cursor()
    except Exception as e:
        print("Erro: ", e)
        conexao = False
        inst_SQL = ""
        conn = ""
    else:
        conexao = True

    return(conexao,inst_SQL,conn)

def recuperar_todos_os_registros(cursor, nome_tabela):
    try:
        query = f"SELECT * FROM {nome_tabela}"
        cursor.execute(query)
        registros = cursor.fetchall()
        return registros
    except Exception as e:
        print(f"Erro ao buscar registros de {nome_tabela}: {e}")
        return []

def gerar_relatorio_completo(cursor):
    nomes_tabelas = ["TB_PROFESSORES", "TB_ENDERECOS"]

    for nome_tabela in nomes_tabelas:
        print(f"Registros na tabela '{nome_tabela}':")
        registros = recuperar_todos_os_registros(cursor, nome_tabela)

        if registros:
            for registro in registros:
                print(registro)
            print(f"Total de registros em '{nome_tabela}': {len(registros)}")
        else:
            print(f"Nenhum registro encontrado na tabela '{nome_tabela}'")
        print("---------------------------------------------------")


conexao, inst_SQL, conn = conecta_BD()

if conexao:
    gerar_relatorio_completo(inst_SQL)

    inst_SQL.close()
    conn.close()
else:
    print("Não foi possível estabelecer uma conexão com o banco de dados.")