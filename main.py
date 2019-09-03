import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Formiga:
    # Método construtor
    def __init__(self, fov, x, y):
        self.fov = fov
        self.posicao = [x, y]
        self.movimentos = ['esq', 'dir', 'cima', 'baixo', 'esq-cima', 'esq-baixo', 'dir-cima', 'dir-baixo']
        self.carregando = False

    # Função de movimento da formiga
    def mover(self):
        escolha = np.random.choice(self.movimentos)
        if escolha == 'esq':
            if self.posicao[0] > 0:
                self.posicao[0] -= 1
        elif escolha == 'dir':
            if self.posicao[0] < N-1:
                self.posicao[0] += 1
        elif escolha == 'cima':
            if self.posicao[1] > 0:
                self.posicao[1] -= 1
        elif escolha == 'baixo':
            if self.posicao[1] < N-1:
                self.posicao[1] += 1
        elif escolha == 'esq-cima':
            if self.posicao[0] > 0 and self.posicao[1] > 0:
                self.posicao[0] -= 1
                self.posicao[1] -= 1
        elif escolha == 'esq-baixo':
            if self.posicao[0] > 0 and self.posicao[1] < N-1:
                self.posicao[0] -= 1
                self.posicao[1] += 1
        elif escolha == 'dir-cima':
            if self.posicao[0] < N-1 and self.posicao[1] > 0:
                self.posicao[0] += 1
                self.posicao[1] -= 1
        elif escolha == 'dir-baixo':
            if self.posicao[0] < N-1 and self.posicao[1] < N-1:
                self.posicao[0] += 1
                self.posicao[1] += 1
        else:
            print('[!]Debug - Erro Movimentação[!]')
    def dist(self, x1, y1, x2, y2):
        return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    # Função que calcula a densidade da região interna do FOV da formiga
    def densidade_fov(self):
        global matriz
        x_inicial = max(0, self.posicao[0] - self.fov)
        x_final = min(N-1, self.posicao[0] + self.fov)
        y_inicial = max(0, self.posicao[1] - self.fov)
        y_final = min(N-1, self.posicao[1] + self.fov)
        somatorio = 0.0
        for x in range(x_inicial, x_final + 1):
            for y in range(y_inicial, y_final + 1):
                if matriz[x][y] == 1.0:
                    somatorio += (1.0 - self.dist(self.posicao[0], self.posicao[1], x, y) / ALPHA)

        somatorio = float(somatorio) / self.fov**2
        #somatorio = float(somatorio) / float(abs(x_inicial - x_final) * abs(x_inicial - x_final)/2.0)**2

        #print(somatorio)
        return max(0, somatorio)

    # Função que realiza as ações da formiga
    def agir(self):
        global matriz
        # Caso esteja carregando
        if self.carregando:
            # Caso carregando e se depara com espaço vazio
            if matriz[self.posicao[0], self.posicao[1]] == 0.0:
                prob_largar = (self.densidade_fov() / (k2 + self.densidade_fov())) ** 2
                if np.random.rand() < prob_largar:
                    self.carregando = False
                    matriz[self.posicao[0], self.posicao[1]] = 1.0
        # Caso não esteja carregando
        else:
            # Caso não carregando e se depara com uma formiga morta
            if matriz[self.posicao[0], self.posicao[1]] == 1.0:
                prob_pegar = (k1 / (k1 + self.densidade_fov())) ** 2
                if np.random.rand() < prob_pegar:
                    self.carregando = True
                    matriz[self.posicao[0], self.posicao[1]] = 0.0

        self.mover()

N = 100 # Dimensões da matriz
QNT_FORMIGAS = int((N*N)/25) # Número de agentes (formigas)
FOV_PADRAO = 3 # Raio do FOV padrão dos agentes
STEPS = 2500 # Número de iterações
ALPHA = 4.0 # Alpha usado na função de densidade
GAMMA = 0.15 # Probabilidade de cada ponto possuiruma formiga morta
k1, k2 = 1.0 , 1.0 # Definindo k1 e k2

matriz = np.zeros((N, N)) # Inicializando a matriz com zeros
for x in range(N):
    for y in range(N):
        if np.random.rand() < GAMMA:
            matriz[x][y] = 1.0

formigas = []
for _ in range(QNT_FORMIGAS):
    formigas.append(Formiga(FOV_PADRAO, int(np.random.randint(0, N)), int(np.random.randint(0, N)))) # !!!FUTURO IMPLEMENTAR FORMIGAS NAO COLIDINDO!!!

# Imprimindo posições iniciais DEBUG
'''for fmg in formigas:
    print(fmg.posicao)'''

plt.matshow(matriz)
plt.savefig('inicial.png', dpi=200)

'''def update(data):
    global formigas
    global matriz
    for fmg in formigas:
        fmg.agir()
    mat.set_data(matriz)
    return mat'''


# Animando o processo (ALTO CUSTO)
'''fig, ax = plt.subplots()
mat = ax.matshow(matriz)
plt.colorbar(mat)
ani = animation.FuncAnimation(fig, update, STEPS, interval=0, repeat=False)
#plt.show()
#Writer = animation.writers['ffmpeg']
#writer = Writer(fps=60, metadata=dict(artist='Me'), bitrate=1800)
ani.save('ant_colony.mp4', fps=int(STEPS/15), dpi=175)
'''

for i in range(STEPS):
    for fmg in formigas:
        fmg.agir()

    if (i + 1) % 100 == 0:
        print("Iteração %d/%d" % (i+1, STEPS))

plt.matshow(matriz)
plt.savefig('final.png', dpi=200)
