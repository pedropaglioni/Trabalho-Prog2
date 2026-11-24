import pickle


def anterior(mat1, mat2, cursos, alunos):
    """Retorna True se mat1 deve aparecer antes de mat2, e False caso contrário.

    Critérios, nesta ordem:
    1) nome do curso (crescente)
    2) tipo: ingressante ("I") antes de concluinte ("C")
    3) (ano, semestre) de ingresso, do mais recente para o mais antigo
    4) nome do aluno (crescente)
    5) matrícula (crescente)
    """
    a1 = alunos[mat1]
    a2 = alunos[mat2]

    # 1) Curso. Compara o código primeiro: se for igual, o nome também é igual
    #    (não existem dois cursos com o mesmo nome) e evitamos consultar 'cursos'.
    if a1[1] != a2[1]:
        return cursos[a1[1]] < cursos[a2[1]]

    # 2) Tipo. Aqui "I" vem antes de "C", o que é o contrário da ordem alfabética.
    if a1[2] != a2[2]:
        return a1[2] == "I"

    # 3) (ano, semestre). Tuplas são comparadas ano primeiro e depois semestre.
    #    Decrescente: o maior (mais recente) vem antes.
    if a1[3] != a2[3]:
        return a1[3] > a2[3]

    # 4) Nome do aluno.
    if a1[0] != a2[0]:
        return a1[0] < a2[0]

    # 5) Matrícula (única, então nunca há empate).
    return mat1 < mat2


def msort(l, cursos, alunos):
    if len(l) > 1:
        meio = len(l) // 2
        lEsq = l[:meio]
        lDir = l[meio:]

        msort(lEsq, cursos, alunos)
        msort(lDir, cursos, alunos)

        merge(l, lEsq, lDir, cursos, alunos)


def merge(l, lEsq, lDir, cursos, alunos):
    i = 0
    j = 0
    k = 0
    tamEsq = len(lEsq)
    tamDir = len(lDir)

    while i < tamEsq and j < tamDir:
        if anterior(lEsq[i], lDir[j], cursos, alunos):
            l[k] = lEsq[i]
            i += 1
        else:
            l[k] = lDir[j]
            j += 1
        k += 1

    # Só um dos lados ainda tem elementos: copia as sobras de uma vez.
    if i < tamEsq:
        l[k:] = lEsq[i:]
    else:
        l[k:] = lDir[j:]


def linha_aluno(mat, alunos, notas):
    nome, curso, tipo, (ano, sem), respondeu = alunos[mat]
    situacao = "Ok" if respondeu else "Pendente"
    linha = f"* {nome} - {mat} - {ano}/{sem} - {situacao}"
    if tipo == "C":
        linha += f" - {notas.get(mat, 0.0):.2f}"
    return linha


def gerar_relatorio(matriculas, cursos, alunos, notas, nome_arquivo):
    with open(nome_arquivo, "w", encoding="utf-8") as arq:
        curso_atual = None
        tipo_atual = None

        for mat in matriculas:
            curso = alunos[mat][1]
            tipo = alunos[mat][2]

            if curso != curso_atual:
                if curso_atual is not None:
                    arq.write("\n")  # linha em branco só entre cursos
                arq.write(f"Curso: {cursos[curso]}\n")
                curso_atual = curso
                tipo_atual = None

            if tipo != tipo_atual:
                arq.write("Ingressantes:\n" if tipo == "I" else "Concluintes:\n")
                tipo_atual = tipo

            arq.write(linha_aluno(mat, alunos, notas) + "\n")


def main():
    with open("entrada.bin", "rb") as arq:
        cursos = pickle.load(arq)
        alunos = pickle.load(arq)
        notas = pickle.load(arq)

    matriculas = list(alunos)

    msort(matriculas, cursos, alunos)

    gerar_relatorio(matriculas, cursos, alunos, notas, "saida.txt")


main()
