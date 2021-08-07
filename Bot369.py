#Necessario
from selenium import webdriver
from unicodedata import normalize
from tensorflow.keras.models import load_model
import time, datetime,sqlite3,nltk,pickle,numpy as np,json,random
# Windows = 0 e Linux = 1
Windows_Linux_Drive = ["chromedriver.exe","/usr/bin/chromedriver"]
Linux_Chrome = "/usr/bin/chromium-browser"
#Horario de Funcionamento
horario = ["07:00","21:00"]
# Classes no WhatsApp Web
classes = {"ElementoUnicoJS":"_3BDr5",
            "Empresa":"LaFelicita",
            "EmpresaJS":"_1awRl copyable-text selectable-text",
            "FotoJS":"_3t3gU rlUm6 _1VzZY",
            "SairdaFotoJS":"hYtwT",
            "ContatoJS":"_1MZWu",
            "Numero1":"_3Tw1q",
            "NUmero2":"_1hI5g _1XH7x _1VzZY",
            "NovaMensagem":"VOr2j",
            "EnviarMensagem":"_2Ujuu",
            "UltimaMensagem":"_3MjzD"}
# caminhos para cada sistema
classesbot = {"modelo":['botdata\\LaFelicita.h5','botdata/LaFelicita.h5'],
            "intecoes":['intents.json','intents.json'],
            "palavras":['botdata\\palavras.LFT','botdata/palavras.LFT'],
            "classes":['botdata\\classes.LFT','botdata/classes.LFT']}
# Alterações futuras
# troca de lista por //div[@class='_1MZWu']//div[2]//span

class WhatBot():
    def __init__(self,Windows=True):
        if Windows:
            self.tp = 0
        else:
            self.tp = 1
        self.navegador = webdriver.Chrome(Windows_Linux_Drive[self.tp],options= self.__chrome_opcoes(Windows))
        self.navegador.get("https://web.whatsapp.com/")
        self.banco = WhatDataBase()
        self.chat = self.Chat_Bot(self)
        self.lista = self.lista_de_contatos(self)
        self.iniciar()
    def __chrome_opcoes(self,Windows):
        options = webdriver.ChromeOptions()
        if not Windows:
            options.binary_location = Linux_Chrome
            options.add_argument("--disable-extensions")
        options.add_experimental_option("detach", True)
        options.add_argument('user-data-dir=selenium')
        return options
    def __status_do_chat(self):
        global classes
        while True:
            try:
                self.navegador.execute_script(f"document.getElementsByClassName('{classes['FotoJS']}')[0].click()")
            except:
                continue
            else:
                break
        while True:
            try:
                time.sleep(2)
                if self.navegador.execute_script(f"return document.getElementsByClassName('{classes['EmpresaJS']}')[0].innerText") == classes["Empresa"]:
                    logado = True
                    print("WhatBot/__status_do_chat:Nome da Empresa Localizado")
                else:
                    logado = False
                    print("WhatBot/__status_do_chat:Nome da Empresa Não Localizado")
                self.navegador.execute_script(f"document.getElementsByClassName('{classes['SairdaFotoJS']}')[0].click()") 
            except:
                continue
            else:
                return logado 
    def iniciar(self):
        if self.__status_do_chat():
            while True:
                contatos = self.lista.gerenciador_de_contatos()
                nomes = {contat.numero:contat.ordem for contat in contatos.values()}
                if "Bot369" in nomes.keys():
                    for numero in contatos.values():
                        msg =  numero.verificar_mensagem()
                        if numero.humano and msg:
                            self.chat.iniciar(numero,msg)
                        contatos[nomes["Bot369"]].selecionar_numero()
                else:
                    time.sleep(1)

    
    class lista_de_contatos(object):
        def __init__(self,cl):
            self.what = cl
        def gerenciador_de_contatos(self):
            self.lista = dict()
            try:
                tamanho = int(self.what.navegador.execute_script("return document.querySelector('#pane-side > div:nth-child(1) > div > div').childElementCount"))
                self.lista = {contato.ordem: contato for contato in [self.contato(self.what,ordem) for ordem in range(1,tamanho+1)]}
            except:
                print("lista_de_contatos/gerenciador_de_contatos:Erro ao lista contatos")
            else:
                return self.lista
        
        class contato(object):
            def __init__(self,cl,ordem):
                self.what = cl
                self.html = self.what.navegador.find_element_by_xpath(f"//*[@id='pane-side']/div[1]/div/div/div[{ordem}]")
                self.ordem = ordem
                self.numero = self.__numero()
                self.humano = self.__humano()
            def __numero(self):
                try:
                    return str(self.html.find_element_by_xpath(f"//*[@id='pane-side']/div[1]/div/div/div[{self.ordem}]/div/div/div/div[2]/div[1]/div[1]").text)
                except:
                    print("lista_de_contatos/contato/__numero: erro ao encontrar nome do contato")
            def __humano(self):
                try:
                    temp = f"//*[@id='pane-side']/div[1]/div/div/div[{self.ordem}]/div/div/div/div[2]/div[1]/div[1]/span/span"
                    if self.what.navegador.find_element_by_xpath(temp).text:
                        return True
                except:
                    return False
            def banco_de_dados_status(self):
                if self.what.banco.encontrar(self.numero) == False:
                    x = datetime.datetime.now()
                    x = f"{x.hour}:{x.minute}"
                    self.what.banco.cadastrar(self.numero,x)
            def selecionar_numero(self):
                while True:
                    try:
                        self.what.navegador.find_element_by_xpath(f"//*[@id='pane-side']/div[1]/div/div/div[{self.ordem}]/div/div/div/div[2]/div[1]/div[1]/span").click()
                    except:
                        continue
                    else:
                        break
            def enviar_mensagem(self,msg):
                self.selecionar_numero()
                while True:
                    try:
                        self.what.navegador.find_element_by_xpath("//*[@id='main']/footer/div[1]/div[2]/div/div[2]").send_keys(f"{classes['Empresa']}: {msg}")
                    except:
                        continue
                    else:
                        self.what.navegador.find_element_by_xpath(f"//*[@id='main']/footer/div[1]/div[3]/button").click()
                        break
            def verificar_mensagem(self):
                try:
                    int(self.what.navegador.find_element_by_xpath(f"//*[@id='pane-side']/div[1]/div/div/div[{self.ordem}]/div/div/div/div[2]/div[2]/div[2]/span[1]/div/span").text)
                except:
                    return None
                else:
                    self.selecionar_numero()
                    if self.humano:
                        temp = f"//*[@id='pane-side']/div[1]/div/div/div[{self.ordem}]/div/div/div/div[2]/div[2]/div[1]/span/span"
                    else:
                        temp = f"//*[@id='pane-side']/div[1]/div/div/div[{self.ordem}]/div/div/div/div[2]/div[2]/div[1]/span/span[3]"
                    
                    while True:
                        
                        try: 
                            ultima = str(self.what.navegador.find_element_by_xpath(temp).text)
                            if classes["Empresa"].upper() in ultima.upper() :
                                return None
                            else:
                                return ultima
                        except:
                            continue
            def fase(self):
                while True:
                    try:
                        self.what.banco.cone.execute(f"select Fase from Rcts where Numero = '{self.numero}'")
                    except:
                        self.banco_de_dados_status()
                    else:
                        return self.what.banco.cone.fetchone()[0]     
    
    class Chat_Bot(object):
        def __init__(self,cl):
            self.what = cl
            self.bot = Bot_LaFelicita(self.what.tp)
            self.fase_lista = dict()
        def iniciar(self,contato,msg):
            self.limpando_fases()
            data = datetime.datetime.now()
            if not contato.numero in self.fase_lista:
                self.fase_lista[contato.numero] = [0,datetime.datetime.now() + datetime.timedelta(minutes=30)]
            if horario[0] < f"{data.hour}:{data.minute}" < horario[1]:
                resposta = self.bot.resposta(msg)
                fase = contato.fase()
                print(f"Contato: {contato.numero},msg: {msg},fase: {fase},resposta: {resposta}")
                if resposta[1] == "cardapio":
                    contato.enviar_mensagem(resposta[0])
                    self.__cardapio(contato)
                else:
                    if self.fase_lista[contato.numero][0] == 0:
                        self.__fase1(contato,resposta)
            else:
                contato.enviar_mensagem(f"A Loja esta Fora do horario de recebimento de pedidos, Favor entre em contato novamente no periodo de {horario[0]} até {horario[0]}")
        def __cardapio(self,contato):
            self.what.banco.Execute("select Id,Produto,Valor,Obs from Produtos")
            t = str()
            for v in self.what.banco.cone.fetchall():
                t += f"\nId: {v[0]},Produto: {str(v[1]).upper()},Preço: R${v[2]}{', obs: ' + v[3] if v[3] else ''}"
            contato.enviar_mensagem(t)  
        def __fase1(self,contato,resposta):
            pass
        def limpando_fases(self):
            try:
                temp = self.fase_lista.copy()
                self.fase_lista.clear()
                for numero in temp:
                    if temp[numero][1] > datetime.datetime.now():
                        self.fase_lista[numero] = temp[numero]
            except:
                pass


class WhatDataBase():
    def __init__(self):
        self.Ban = sqlite3.connect("WhatBot.db")
        self.cone = self.Ban.cursor() 
    def Execute(self,commad):
        self.cone.execute(commad)
        self.Ban.commit()   
    def encontrar(self,Numero):
        self.Execute(f"select [Numero] from Rcts where Numero = '{Numero}';")
        try:
            return self.cone.fetchone()[0] != None
        except:
            return False
    def ListadeTarefas(self):
        self.Execute("select * from LDT")
        return self.cone.fetchall()
    def ListadeTarefasDelete(self,ID):
        self.Execute(f"delete from LDT where ID = {ID};")
    def cadastrar(self,Numero,Data,Fase=0,Nova=0):
        self.Execute(f"insert into Rcts(Numero,Ultm,Fase,nvms) values ('{Numero}','{Data}',{Fase},{Nova});")
    def Fase(self,Numero,Fase):
        self.Execute(f"Update Rcts set Fase = {Fase} where Numero = '{Numero}''")  
    def NovaMensagem(self,Numero,nvms):
        self.Execute(f"Update Rcts set nvms = {nvms} where Numero = '{Numero}''")
    def mudar_fase(self,Numero,Fase):
        self.cone.execute(f"update Rcts set Fase = {Fase} where Numero = '{Numero}' ")
        self.cone.commit()

class Bot_LaFelicita():
    def __init__(self,tp):
        import Treinar_LaFelicita
        self.modelo = load_model(classesbot["modelo"][tp])
        self.intecoes = json.loads(open(classesbot["intecoes"][tp],encoding="utf-8").read())
        self.palavras = pickle.load(open(classesbot["palavras"][tp],'rb'))
        self.classes = pickle.load(open(classesbot["classes"][tp],'rb'))
        self.Stemmer = nltk.stem.RSLPStemmer()
    def resposta(self,msg):
        ints = self.comparar(msg)
        respost = self.lista_de_resposta(ints)
        return respost
    def limpando_frase(self,msg):
        w = normalize('NFKD', msg).encode('ASCII', 'ignore').decode('ASCII')
        return [self.Stemmer.stem(l).lower() for l in nltk.word_tokenize(w)] 
    def arco(self,msg):
        wds = self.limpando_frase(msg)
        mochila = [0]*len(self.palavras)
        for w in wds:
            for n,l in enumerate(self.palavras):
                if l == w:
                    mochila[n] = 1
        return(np.array(mochila))
    def comparar(self,msg):
        cl = self.arco(msg)

        res = self.modelo.predict(np.array([cl]))[0]
        margem_de_erro = 0.25
        resultado = [[i,r] for i,r in enumerate(res) if r>margem_de_erro]
        resultado.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in resultado:
            return_list.append({"intent": self.classes[r[0]], "probability": str(r[1])})
        return return_list
    def lista_de_resposta(self,ints):
            list_of_intents = self.intecoes['intents']
            if ints is not None and float(ints[0]['probability']) > 0.70:
                tag = ints[0]['intent']
                for i in list_of_intents:
                    if(i['tag']== tag):
                        result = random.choice(i['responses'])
                        break
                return [result,tag]
            else:
                tag = 'SemResposta'
                for i in list_of_intents:
                    if(i['tag']== tag): 
                        result = random.choice(i['responses'])
                        break
                return [result,tag]

WhatBot()