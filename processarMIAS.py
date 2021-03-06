'''
Created on 18 Nov 2015

@author: leo
'''
import os

dadosPath = 'Dados-MIAS-imagens'
imagensPath = 'mamografias'
imagensBinarizadasPath = 'mamografiasBinarizadas'

dadosMIASDic = {}

duplicadas = []

import numpy as np

def extrairDados():
    with open(dadosPath, encoding='utf-8', newline='\n') as dadosMIAS:
        for dadosImagem in dadosMIAS:
            if dadosImagem.strip()[0] != '#':
                dadosImagem = dadosImagem.split()    
                if len(dadosImagem) == 7:    
                    if dadosMIASDic.get(dadosImagem[0] + ".pgm",None) is None:
                        dadosMIASDic[dadosImagem[0] + ".pgm"] = (dadosImagem[3],dadosImagem[4],dadosImagem[5],dadosImagem[6])
                    else:
                        print('imagem ', dadosImagem[0], "esta duplicada no MIAS")
                        duplicadas.append(dadosImagem[0] + ".pgm")
                
                
def processarTodas(parametros): 
    imagensFileNames = os.listdir(imagensPath)
    for imagemFileName in sorted(imagensFileNames):
        if dadosMIASDic.get(imagemFileName,None) is not None:
            if imagemFileName in duplicadas:
                print(imagemFileName,"na pasta esta duplicada e nao foi escolhida uma coordedada")
                 
            comandoString = './out %s %s %s %s %s %s' % (os.path.join(imagensPath,imagemFileName),\
                                                   os.path.join(imagensBinarizadasPath,imagemFileName +  dadosMIASDic[imagemFileName][0]),\
                                                   dadosMIASDic[imagemFileName][1],\
                                                   dadosMIASDic[imagemFileName][2],\
                                                   dadosMIASDic[imagemFileName][3],\
                                                   parametros)    
            print(comandoString)
            os.system(comandoString)


def testar(parametros):
    listaB = []
    listaM = []
    
    with open('saida.txt', encoding='utf-8', newline='\n') as saida:
        for linha in saida:
            linha = linha.strip().split()
            
            if linha[0][-1] == 'B':
                listaB.append(float(linha[1]))
            else:
                listaM.append(float(linha[1]))
            
    
    mediaB = np.mean(listaB)
    mediaM = np.mean(listaM)
       
    if mediaB <= mediaM:
        print("Media da DF dos benignos (%s) é menor ou igual a dos malignos (%s) com os parametros [%s]" % (mediaB,mediaM,parametros))
        return True
    else:
        print("Nao foi dessa vez",mediaB,mediaM)
        return False
    
def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step

def testarParametros():
    for limiarBinarizacao in drange(-0.1,1,0.1):
        for limiarLimpar2 in drange(-0.1,1,0.1):
            for limiarLimpar3 in drange(-0.1,1,0.1):
                parametros = ("%s %s %s" % (limiarBinarizacao,limiarLimpar2,limiarLimpar3))
#                 print(parametros)
                processarTodas(parametros)
                if testar(parametros):
#                     return
                    pass
                os.system('rm -f saida.txt')

if __name__ == "__main__":
    extrairDados()  
    os.system('make')
    
    parametrosTabela1 = "0.3 -1 -1"
    parametrosTabela2 = "-1 0.7 -1"
    parametrosTabela3 = "-1 -1 0.8"
    parametrosTabela4 = "0.3 0.7 0.8"
    
    p = parametrosTabela4
    
    processarTodas(p)
    testar(p)
    
    
    
    
    