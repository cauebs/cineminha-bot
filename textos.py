from telegram import Emoji

start_text = '''*Olá! Envie sua localização para começar* (ela não será compartilhada com ninguém)

Você também pode usar o comando /local. Exemplos:
/local _Trindade Florianópolis_
/local _São José SC_'''

local_atualizado_text = Emoji.ROUND_PUSHPIN+''' *Localização atualizada!*
Você pode mudá-la a qualquer momento compartilhando uma localização ou com o comando /local'''

local_vazio_text = Emoji.BLACK_QUESTION_MARK_ORNAMENT+''' *Favor inserir alguma localização.* Exemplos:
/local _Trindade Florianópolis_
/local _São José SC_'''

pesquisar_text = '''Me envie qualquer coisa para pesquisar:'''

local_nao_definido = Emoji.BLACK_QUESTION_MARK_ORNAMENT+''' Primeiro defina o local com /local ou enviando uma localização!'''

help_text = '''• Use os botões abaixo para listar cinemas ou filmes.
• Envie uma mensagem a qualquer momento para pesquisar
• Atualize o seu local enviando uma localização ou enviando /local _seu-local-aqui_

Caso tenha qualquer dúvida, crítica ou sugestão, venha falar comigo! - @cauebs'''