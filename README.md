# ACQUA-TIC: Monitoramento e Controle Remoto de Aquário

## Descrição do Projeto

O **ACQUA-TIC** é um projeto concebido para monitorar e controlar um aquário de 18 litros, proporcionando uma experiência de aquarismo inteligente. Utilizando um ESP32 conectado à rede WiFi doméstica, o sistema captura dados em tempo real, como temperatura e níveis de incidência de luz, além de imagens atualizadas do aquário. Os usuários podem gerenciar remotamente a lâmpada UV e o aquecedor através de um aplicativo Android, garantindo que o ambiente aquático esteja sempre nas condições ideais.

## Tecnologias Utilizadas

- **Hardware:**
  - ESP32: Microcontrolador com conectividade WiFi
  - Módulo Relé 5V: Para controlar a lâmpada UV e o aquecedor
  - Câmera OV7670: Captura de imagem do aquário
  - Sensor de Temperatura DS18B20: Monitoramento da temperatura da água
  - Sensor de Luminosidade BH1750: Medição da luz ambiente

- **Software:**
  - **AWS:** Utilização do EC2 para hospedar o servidor que processa as requisições.
  - **Flask:** Framework web para criar a API RESTful que interage com o ESP32 e o banco de dados.
  - **MongoDB Atlas:** Banco de dados NoSQL para armazenar os dados coletados e imagens do aquário.
  - **Kivy:** Framework Python para desenvolvimento do aplicativo mobile para Android.

## Estrutura do Projeto

A estrutura do projeto é organizada nas seguintes pastas:

- `database/`: Scripts para configuração do banco de dados.
- `esp32/`: Código para o microcontrolador ESP32.
- `mobile_app/`: Código do aplicativo Android, incluindo ícones e interfaces.
- `server/`: Código da aplicação Flask que gerencia os endpoints da API.

## Funcionalidades

1. **Captura de Dados:**
   - Medição de temperatura da água em tempo real.
   - Leitura do nível de luminosidade utilizando o BH1750.
   - Captura de imagens com a câmera a intervalos regulares.

2. **Controle Remoto:**
   - Habilitação/desabilitação da lâmpada UV.
   - Controle do aquecedor para manter a temperatura ideal do aquário.

3. **Visualização de Dados:**
   - Interface para visualização dos dados coletados e imagens no aplicativo Android.

## Instruções de Uso

1. **Configuração do ESP32:**
   - Carregue o código fornecido na pasta `esp32/` no ESP32 utilizando a IDE Arduino.
   - Certifique-se de que o microcontrolador esteja conectado à mesma rede WiFi do servidor AWS.

2. **Configuração do Servidor:**
   - Implementar a aplicação Flask na AWS EC2.
   - Configurar o MongoDB Atlas e conectar a aplicação ao banco de dados.

3. **Aplicativo Android:**
   - Instale o aplicativo desenvolvido com Kivy em um dispositivo Android.
   - Conecte-se à aplicação Flask para visualizar dados e controlar o aquário remotamente.
