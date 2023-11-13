import time
import socket
import random
import threading
import datetime
from datetime import timedelta
import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QPainter, QColor


class TelaPrincipal(QWidget):
    def __init__(self, numero, host, port):
        super().__init__()
        self.numero = numero
        self.host = host
        self.port = port
    
        self.initUI()


    def initUI(self):
        
        # Widgets
        self.msg_enviada_l = QLabel(f'Mensagem enviada:', self)
        self.msg_enviada = QLabel(f'8001: Oi', self)
        self.msg_recebida_l = QLabel(f'Mensagem recebida:', self)
        self.msg_recebida = QLabel(f'8002: Olá', self)
        self.numero_processo = QLabel(f'{self.numero}', self)
        self.botao_cancelar = QPushButton('X',self)
        
        self.setWindowTitle(f'Processo {self.port}')
        self.setGeometry(670, 100, 400, 300) #(X, Y, W, H)
        

        # Posicionar os widgets na tela
        self.msg_enviada_l.setGeometry(10,40,223,100)
        self.msg_enviada.setGeometry(10,100,160,100)
        self.msg_recebida_l.setGeometry(230,40,223,100)
        self.msg_recebida.setGeometry(230,100,160,100)
        self.numero_processo.setGeometry(10, 10, 50, 45)
        self.botao_cancelar.setGeometry(350, 10, 40, 30)

        #Estilização
        self.msg_enviada.setStyleSheet("background-color: rgb(255,255,255); color: black; border: 1px solid black; font-size: 20px;")
        self.msg_recebida.setStyleSheet("background-color: rgb(255,255,255); color: black; border: 1px solid black; font-size: 20px;")

        self.numero_processo.setStyleSheet("background-color: rgb(255,255,255); color: black; border: 1px solid black; border-radius: 12px; font-size: 20px;")
        self.numero_processo.setAlignment(QtCore.Qt.AlignCenter)

        self.botao_cancelar.setStyleSheet("background-color: red; color: black;")

        # Iniciando processo em uma thread separada
        self.processo = Processo(self.host,self.port)
        self.processo.start()

        #self.processo.sinal.connect(self.atualizar_tempo_interface)

        # Configurar layout
        self.botao_cancelar.clicked.connect(self.close)
    

class Processo(QThread):
    sinal = pyqtSignal(str)

    def __init__(self, host, port , parent=None,):
        super().__init__(parent)
        self.host = host
        self.port = port

    def run(self):
        HOST = self.host
        PORT = self.port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))


        while True:
            print(f'HOST: {self.host} PORT: {self.port}')
            time.sleep(5)

def abrir_telas():
    processos = []
    #Cria uma instancia da aplicação PyQt, necessária para configurar a interface gráfica e o loop de eventos
    app = QApplication(sys.argv)

    for i in range (2):
        HOST = f'127.0.0.{i+1}'
        PORT = 8000 + (i+1)
        processos.append({'host': HOST, 'port': PORT})

    # Cria 7 objetos TelaPrinciapal 
    telas = [TelaPrincipal(i+1, processos[i]['host'], processos[i]['port']) for i in range(2)]

    # Mostra as 7 telas
    for tela in telas:
        tela.show()

    # Inicia a aplicação PyQT
    sys.exit(app.exec_())

    
if __name__ == "__main__":
    abrir_telas()
    
