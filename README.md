# Tradutor Nuxt i18n
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)


### Como e o que é feito
Esse script em Python usa a `API do Google Cloud Translator` para traduzir arquivos no formarto do `Nuxt i18n`.

Assim que você executa o programa, você deve responder algumas perguntas para que o script seja configurado para o uso.

    ![Imagem](https://i.imgur.com/AfwwIl6.png)

#### Pré-requisitos
1.  Para usar este script execute os seguintes comandos para instalar as dependências
    - `pip install inquirer` 
    - `pip install pip install google-cloud-translate`
2. Entre no [Console de Google Cloud Platform](https://console.cloud.google.com/) e crie uma conta de serviços. Baixe o arquivo `.json` e mova-o para a pasta onde o script está.

#### Como usar
Execute o script com `python i18n-translator.py` e preencha as informações conforme for solicitado. O script traduzirá todos os objetos contidos no arquivo informado e os salvará de acordo com o formato `ISO-639-1` do código da língua.