import pickle
import time

def anterior(mat1, mat2, cursos, alunos):
    """ Retorna True se mat1 deve aparecer antes de mat2 e False se não.
    Critérios:
    1) nome do curso
    2) tipo
    3) (ano, semestre)
    4) nome do aluno
    5) matrícula
    """
    a1 = alunos[mat1]
    a2 = alunos[mat2]

    if a1[1] != a2[1]:
        return cursos[a1[1]] < cursos[a2[1]]

    if a1[2] != a2[2]:
        return a1[2] == "I"

    if a1[3] != a2[3]:
        return a1[3] > a2[3]

    if a1[0] != a2[0]:
        return a1[0] < a2[0]

    return mat1 < mat2

def msort(lista, cursos, alunos):
    if len(lista) > 1:
        meio = len(lista) // 2
        listaEsq = lista[:meio]
        listaDir = lista[meio:]

        msort(listaEsq, cursos, alunos)
        msort(listaDir, cursos, alunos)

        merge(lista, listaEsq, listaDir, cursos, alunos)

def merge(lista, listaEsq, listaDir, cursos, alunos):
    i = 0
    j = 0
    k = 0
    tamEsq = len(listaEsq)
    tamDir = len(listaDir)

    while i < tamEsq and j < tamDir:
        if anterior(listaEsq[i], listaDir[j], cursos, alunos):
            lista[k] = listaEsq[i]
            i += 1
        else:
            lista[k] = listaDir[j]
            j += 1
        k += 1

    if i < tamEsq:
        lista[k:] = listaEsq[i:]
    else:
        lista[k:] = listaDir[j:]

def linhaAluno(mat, alunos, notas):
    nome, curso, tipo, (ano, sem), respondeu = alunos[mat]

    if respondeu:
        situacao = "Ok"
    else:
        situacao = "Pendente"
    
    linha = (f"* {nome} - {mat} - {ano}/{sem} - {situacao}")

    if tipo == "C":
        if mat in notas:
            nota = notas[mat]
        else:
            nota = 0.0
        linha += (f" - {nota:.2f}")
    
    return linha

def gerarRelatorio(matriculas, cursos, alunos, notas, nome_arquivo):
    with open(nome_arquivo, "w", encoding="utf-8") as arq:
        cursoAtual = None
        tipoAtual = None

        for mat in matriculas:
            curso = alunos[mat][1]
            tipo = alunos[mat][2]

            if curso != cursoAtual:
                if cursoAtual is not None:
                    arq.write("\n")
                arq.write(f"Curso: {cursos[curso]}\n")
                cursoAtual = curso
                tipoAtual = None

            if tipo != tipoAtual:
                if tipo == "I":
                    arq.write("Ingressantes:\n")
                else:
                    arq.write("Concluintes:\n")
                tipoAtual = tipo

            arq.write(linhaAluno(mat, alunos, notas) + "\n")

def main():

    inicio = time.perf_counter()

    with open("entrada.bin", "rb") as arq:
        cursos = pickle.load(arq)
        alunos = pickle.load(arq)
        notas = pickle.load(arq)

    matriculas = list(alunos)

    msort(matriculas, cursos, alunos)

    gerarRelatorio(matriculas, cursos, alunos, notas, "saida.txt")

    fim = time.perf_counter()
    print(f"Tempo total: {fim - inicio:.3f} segundos")


main()