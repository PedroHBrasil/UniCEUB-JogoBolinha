
from typing import Text
from graphics import GraphWin, Point, Rectangle
from src.jogo.elementos.barra import Barra
from src.jogo.elementos.bola import Bola
from src.jogo.jogador.jogador import Jogador
from src.jogo.elementos.campo import Campo
from src.jogo.elementos.placar import Placar
from src.menu.menu import Menu
import time

from src.ranking.ranking import Ranking


class Jogo:

    jogador_esquerda: Jogador
    jogador_direita: Jogador
    bola: Bola
    barra_esquerda: Barra
    barra_direita: Barra
    placar: Placar


    def __init__(self, janela: GraphWin) -> None:
        self.jogador_esquerda = Jogador(janela,"esquerda")
        self.jogador_direita = Jogador(janela, "direita")
        self.bola = Bola()
        self.barra_esquerda = Barra(velocidade_y= 40, cor= 'pink')
        self.barra_direita = Barra(velocidade_y= 40, cor= 'purple')
        self.placar = Placar(janela)
    

    def rodar(self, janela: GraphWin) -> None:
        """_summary_

        Args:
            janela (GraphWin): Janela na qual o programa está sendo
            executado.
        """

        # TODO Chamar o método "self.__definir_jogadores" para
        # TODO definição dos jogadores

        self.__definir_jogadores(janela)

        # TODO Chamar o método "self.__desenhar" para desenhar o
        # TODO jogo completo (desenhar campo e placar).

        self.__desenhar(janela, desenhar_campo= True, desenhar_placar= True);


        # Loop do jogo
        nome_vencedor = ""
        sair = False
        partida_encerrada = False

        while not partida_encerrada:

            # TODO Chamar o método "self.__desenhar" para desenhar o
            # TODO jogo em seu estado atual.
            self.__desenhar(janela, desenhar_campo= False, desenhar_placar= False)
            self.bola.incrementar_posicao()
            self.bola.apagar_desenho()

            # TODO verificar colisão entre bola e paredes/barras usando
            # TODO o método "self.bola.verificar_colisao"


            # TODO caso haja colisão com uma das barras:
            # ? atualizar velocidade da bola?

            # TODO Verificar se houve pontuação avaliando-se a
            # TODO intersecção da bola com as barras de pontuação.
            # ? Pode ser uma boa travar a movimentação das barras em
            # ? caso de pontuação.
            # ! Resetar a bola apenas quando a bola sair da tela!

            # TODO Caso haja pontuação:
            # TODO chamar método
            # TODO "self.jogador_{lado}.incrementar_pontuacao" para o
            # TODO jogador que pontuou.
            # TODO Atualizar placar com base nas pontuacoes.
            # TODO Setar variável para redesenhar o placar.
            # ? Travar movimentação das barras através de uma variável
            # ? booleana?
            # TODO modificar parâmetros dos elementos (velocidade da
            # TODO bola, tamanho da barra, etc).
            # TODO avaliar se o jogo terminou, verificando se algum dos
            # TODO jogadores atingiu a pontuação máxima. registrar o
            # TODO nome do jogador vencedor em nome_vencedor. Setar
            # TODO partida_encerrada = True.

            # TODO Avaliar teclas pressionadas:

            # TODO atualizar posições das respectivas barras caso "Up",
            # TODO "Down", "w" ou "s".
            # ! Pode ser necessário utilizar multithreading para se
            # ! permitir que ambos os jogadores movam as barras ao
            # ! mesmo tempo. Assim, essa última parte do código deveria
            # ! ser retirada desse loop, fazendo um while loop e uma
            # ! thread para cada jogador. Haveriam então 3 threads:
            # ! principal, comando do jogador da esquerda e comando do
            # ! jogador da direita.

            tecla = janela.checkKey()

            Movimentar = {
                "up": self.barra_direita.subir,
                "down": self.barra_direita.descer,
                "w": self.barra_esquerda.subir,
                "s":  self.barra_esquerda.descer,
            }

            if tecla.lower() in Movimentar:
                Movimentar[tecla.lower()](janela)

            if self.placar.pontuacao_esquerda == 10:
                partida_encerrada = True

            if self.placar.pontuacao_direita == 10:
                partida_encerrada = True

            if partida_encerrada: 
                self.bola.apagar_desenho()
                self.barra_esquerda.apagar_desenho()
                self.barra_direita.apagar_desenho()
                self.placar.apagar_placar_jogo()
                janela.getMouse()
                ranking = Ranking()
                ranking.rodar(janela)


                nome_vencedor = "1"

            if tecla == 'Escape':
                self.bola.apagar_desenho()
                self.barra_esquerda.apagar_desenho()
                self.barra_direita.apagar_desenho()
                self.placar.apagar_placar_jogo()
                menu = Menu()
                menu.rodar(janela, True)
                if menu.sair:
                    return True
                self.barra_esquerda.desenhar(janela)
                self.barra_direita.desenhar(janela)
                self.placar.desenhar(janela)

            if self.placar.pontuacao_direita == 10:
                partida_encerrada = True
                nome_vencedor = "2"

            # TODO Inicializar menu com parâmetro "em_jogo" = True em
            # TODO caso de "escape". Setar variável sair = menu.sair.
            # TODO caso contiuar, chamar o método "self.__desenhar"
            # TODO para desenhar o jogo completo (desenhar campo e
            # TODO placar).
            sair = False
            #break

        return sair, nome_vencedor

    def __definir_jogadores(self, janela: GraphWin) -> None:
        """Define os jogadores que jogarão a partida atual.

        Args:
            janela (GraphWin): Janela na qual o programa está sendo
            executado.
        """
        self.jogador_esquerda.rodar(janela)
        self.jogador_direita.rodar(janela)

    def __desenhar(
            self,
            janela: GraphWin,
            desenhar_campo: bool = False,
            desenhar_placar: bool = False
            ) -> None:
        """Desenha o jogo conforme seu estado atual.

        Args:
            janela (GraphWin): Janela na qual o programa está sendo
            executado.
            desenhar_campo (bool): Indica se o campo deve ser
            desenhado.
            desenhar_placar (bool): Indica se o placar deve ser
            desenhado.
        """

        campo = Campo(janela)

        if desenhar_campo: 
            campo.desenhar_margens(janela)
            self.barra_direita.posicao_inicial_dir(janela)
            self.barra_direita.desenhar(janela)
            self.barra_esquerda.posicao_inicial_esq(janela)
            self.barra_esquerda.desenhar(janela)
            self.bola.reset_bolinha(janela)
            self.bola.desenhar(janela)
        if desenhar_placar:
            self.placar.apagar_placar_jogo()
            self.placar.desenhar(janela)
        self.bola.apagar_desenho()
        


        self.bola.desenhar(janela)

        jogador_pontuou = self.bola.verificar_colisao(self.barra_esquerda, self.barra_direita, janela)

        if jogador_pontuou == 'ponto_esq': 
            self.placar.soma_ponto_player_esq(janela)
            self.placar.apagar_placar_jogo()
            self.placar.desenhar(janela)

            self.barra_esquerda.alterar_altura(janela, -20)
            self.barra_direita.alterar_altura(janela, 20)

        if jogador_pontuou == 'ponto_dir': 
            self.placar.soma_ponto_player_dir(janela)
            self.placar.apagar_placar_jogo()
            self.placar.desenhar(janela)

            self.barra_esquerda.alterar_altura(janela, 20)
            self.barra_direita.alterar_altura(janela, -20)

        # TODO caso desenhar_campo:
        # TODO limpar desenho
        # TODO desenhar campo
        # TODO desenhar paredes (self)
        # TODO desenhar zonas de pontuação (self)

        # TODO caso desenhar_placar
        # TODO limpar placar (self.jogador_{lado}.pontuacao)
        # TODO desenhar placar (self.jogador_{lado}.pontuacao)

        # TODO limpar barras (self)
        # TODO desenhar barras (self)

        # TODO limpar bola (self)
        # TODO desenhar bola (self)
        #janela.getMouse()
        time.sleep(0.06)

        pass
