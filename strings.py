from telegram import Emoji

lang = {
"pt-br":["Dublado", "Legendado"],
"en":["Dubbed", "Subtitled"]}

start = {
"pt-br":'''*Olá! Envie sua localização para começar* (ela não será compartilhada com ninguém)\n
Você também pode usar o comando /local. Exemplos:
/local _Trindade Florianópolis_
/local _São José SC_''',
"en":'''*Hello! Send me your location to start* (it won't be shared with anyone)\n
You can also use /local followed by your zip code, address or anything else, eg.:
/local _Mountain View, CA_
/local _11213_
/local _Rue Cler, Paris_'''}

command = {
"pt-br":["filmes", "cinemas", "ajuda"],
"en":["movies", "theaters", "help"]}

buttons = {
"pt-br":[Emoji.CLAPPER_BOARD+" Listar filmes",
Emoji.MOVIE_CAMERA+" Listar cinemas",
Emoji.ROUND_PUSHPIN+" Atualizar localização",
Emoji.BLACK_QUESTION_MARK_ORNAMENT+" Ajuda"],
"en":[Emoji.CLAPPER_BOARD+" List movies",
Emoji.MOVIE_CAMERA+" List theaters",
Emoji.ROUND_PUSHPIN+" Update location",
Emoji.BLACK_QUESTION_MARK_ORNAMENT+" Help"]}

no_results = {
"pt-br":'*Não foi encontrado nenhum resultado.*\nTente outra coisa ou atualize sua localização',
"en":'*The search returned no results.*\nTry something else or update your location'}

results = {
"pt-br":'Selecione um para mais informações:',
"en":'Select one for more information:'}

loc_undefined = {
"pt-br":Emoji.BLACK_QUESTION_MARK_ORNAMENT+' Primeiro defina o local com /local ou enviando uma localização!',
"en":Emoji.BLACK_QUESTION_MARK_ORNAMENT+' First you need to either share a location or set one via /local'}

loc_updated = {
"pt-br":Emoji.ROUND_PUSHPIN+''' *Localização atualizada!*
Você pode mudá-la a qualquer momento compartilhando uma localização ou com o comando /local''',
"en":Emoji.ROUND_PUSHPIN+''' *Location updated!*
You can change it at any moment by sharing a location or using the /local command'''}

loc_empty = {
"pt-br":Emoji.BLACK_QUESTION_MARK_ORNAMENT+''' *Favor inserir alguma localização.* Exemplos:
/local _Trindade Florianópolis_
/local _São José SC_''',
"en":Emoji.BLACK_QUESTION_MARK_ORNAMENT+''' *Please, type in a location after /local.* Examples:
/local _Mountain View, CA_
/local _11213_
/local _Rue Cler, Paris_'''}

share = {"pt-br":"Compartilhar","en":"Share"}

help = {
"pt-br":'''• Use os botões abaixo para listar cinemas ou filmes.
• Envie uma mensagem a qualquer momento para pesquisar
• Atualize o seu local enviando uma localização ou enviando /local _seu-local-aqui_\n
Caso tenha qualquer dúvida, crítica ou sugestão, venha falar comigo! - @cauebs''',
"en":'''• Use the buttons below to navigate
• Send me a message at any moment to search
• Update your location whenever you want by sharing a location or via /local\n
In case you have any questions, suggestions or complaints, please come talk to me @cauebs'''}
