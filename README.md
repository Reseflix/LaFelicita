# Sobre
> Uma ferramenta para venda de bolo que utilizar Machine learning para verificar as intenções do usuario no chat
> projeto tambem foi adaptado para rodar no Raspberry pi (já que existe problemas com a biblioteca keras)
# Ferramentas
- python
- tensorflow/keras
- sqlite
- selenium e Web Whatsapp
# Status
Abandonado/Pausado: pretendo finalizar esse projeto porem somente quanto tiver um maior entendimento sobre Machine learning, pois era necessario entender as entidades de uma conversa por exemplo:
> Gostaria de um bolo de chocolate.
Nesse texto era necessario entender
- "Um": Refere-se a um Inteiro = 1.
- "Chocolate": tipo do produto
- "Bolo": item da categoria

Semelhante ao oque acontece com o watson assistant da IBM
porem as partes de intenções estão configuradas para entender quando o cliente gostaria de comprar um bolo.
# tensorflow/keras
Foi criado um array contento todas as palavras utilizadas em todas as intenções ao qual cada index do array correspondia a uma palavra.
