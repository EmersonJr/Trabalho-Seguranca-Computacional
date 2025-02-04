# Trabalho-Seguranca-Computacional
Trabalho 3 da Disciplina Segurança Computacional da Unb, semestre 2024.2.

## Descrição 
O trabalho consiste na elaboração e implementação de um gerador e verificador de assinaturas RSA em arquivos. As funcionalidades do projeto são separadas em 3 partes:
1. Geração de Chaves e Encriptação/Decriptação assimétrica RSA com OAEP (Optimal Asymmetric Encryption Padding)

2. Assinatura, calcular o Hash da mensagem, encriptar o hash obtido e formatar o resultado (caracteres especiais e informações para verificação em BASE64)

3. Verificação : Parsing do documento assinado e decifração da mensagem, decrifração da assinatura (hash) e comparação com hash do arquivo.

 ## Rodar o Trabalho
 Para rodar o trabalho, é necessário baixar as bibliotecas utilizadas. E rodar o comando:
 ``` shell
python main.py
```
<h2>💻 Autores</h2>

<table>
  <tr>
    <td align="center"><a href="https://github.com/isasisnando" target="_blank"><img style="border-radius: 50%;" src="https://github.com/isasisnando.png" width="100px;" alt="Isabela Souza"/><br /><sub><b>Isa Sousa</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/SalaLucas" target="_blank"><img style="border-radius: 50%;" src="https://github.com/SalaLucas.png" width="100px;" alt="Lucas Sala"/><br /><sub><b>Lucas Sala</b></sub></a><br /></td>
    <td align="center"><a href="https://github.com/EmersonJr" target="_blank"><img style="border-radius: 50%;" src="https://github.com/EmersonJr.png" width="100px;" alt="Emerson Junior"/><br /><sub><b>Emerson Junior</b></sub></a><br /></td>
</table>
