<a name="readme-top"></a>

# PSR Aumented Reality Paint 

Desenvolvido por **Mateus Araujo e Rafael Mendes**, no âmbito da disciplina de **Programação de Sistemas Robóticos (PSR)**, este trabalho tem como objetivo a criação de um conjunto de aplicações que irão **permitir ao utilizador desenhar numa imagem movendo um objeto colorido em frente à câmara do portátil.** 

### Funcionamento

O programa **color_segmenter.py** serve para configurar os parâmetros da deteção de cor que serão depois utilizados pelo **ar_paint.py.** O **color_segmenter.py** recebe imagens continuamente da câmara do portátil. Depois, essas imagems são processadas de modo a segmentar os pixeis cuja cor esteja entre os **limites mínimo e máximo de R,G e B** establecidos.

Após regular os níveis de RGB para a captação da cor desejada o utilizador deve **pressionar a tela 'w'** para **salvar os parâmetros no formato de ficheiro JSON**.

O utilizador pode ainda usar a **tecla "q"** para indicar que quer **terminar o programa** sem efetuar a gravação do ficheiro JSON.

Por último, temos o script **ar_paint**, que é responsável por receber, obrigatóriamente, o ficheiro JSON gerado pelo **color_segmenter.py** e, opcionalmente, o utilizador poderá definir os modos de desenhos existentes, que serão explicados mais a frente.

### Teclas de atalho
Durante o desenho, o utilizador pode utilizar as seguintes teclas de atalho:
* Pressione 'r' para alterar a cor do lápis para vermelho
* Pressione 'g' para alterar a cor do lápis para verde
* Pressione 'b' para alterar a cor do lápis para azul
* Pressione '+' para aumentar o tamanho do lápis
* Pressione '-' para diminuir o tamanho do lápis
* Pressione 's' para desenhar um rectangulo
   * **Nota:** O desenho de um rectangulo é feito ao pressionar a tecla 's' e depois arrastar o objeto colorido ou rato, dependendo do modo, para o canto oposto do rectangulo que se pretende desenhar. Quando satisfeito, pressione 'f' para desenhar o retangulo.
* Pressione 'e' para desenhar um circulo
   * **Nota:** O desenho de um circulo é feito ao pressionar a tecla 'e' e depois arrastar o objeto colorido ou rato, dependendo do modo, para definir o raio do mesmo. Quando satisfeito, pressione 'f' para desenhar o circulo.
* **NO MODO PINTURA NUMERADA:**
   * Após satisfeito com a pintura realizada, o utilizador deve guardar a imagem clicando em 'w' e, em seguida:
      * Pressione 't' para fazer o cáculo de precisão de acerto da sua pintura comparada com a pintura final
* Pressione 'c' para limpar o quadro
* Pressione 'q' para sair do script

## Inicialização

Para o teste e boa utilização do código desenvolvido, o utilizador deve seguir os passos seguintes para obter uma cópia local do repositório e execução do mesmo.

### Pré-requesitos
* Python 3
* OpenCV
* Numpy
* Pillow

### Execução do código - Considerações
Na execução do programa, será necessário realizar a inicialização obrigatória do parâmetro **--json**, fornecendo um **ficheiro JSON** que possuirá os **limites RGB** que serão utilizados para a deteção do objeto colorido. 

**Modo de desenho existentes:**

1. **Modo Contínuo (Normal):** Modo em que o utilizador apenas necessita de fornecer o ficheiro JSON e desenhar utilizando o objeto e as teclas.
   ```py
   ./ar_paint.py -j <ficheiro JSON>
   ```

2. **Modo Use Shake Prevention:** Modo em que alivia o traço do desenho, permitindo ao utilizador mais controlo e precisão, não existindo também o desenho de certas linhas que resultam da movimentação muito rápida do objeto. O restante funcionamento é igual ao Modo Contínuo.
   ```py
   ./ar_paint.py -j <ficheiro JSON> -usp 
   ```

3. **Modo Use Mouse:** Modo em o mouse do utilizador pode ser utulizado para desenhar no quadro. O restante funcionamento é igual ao Modo Contínuo.
   ```py
   ./ar_paint.py -j <ficheiro JSON> -usp -m
   ```

4. **Modo Video Stream:** Modo em que o desenho acontece na câmera do utilizador. O restante funcionamento é igual ao Modo Contínuo. (Implementação não concluída)
   ```py
   ./ar_paint.py -j <ficheiro JSON> -v
   ```

5. **Modo Pintura Numerada:** Modo em que o utilizador deve desenhar uma pintura numérica, que será comparada com a pintura final. O restante funcionamento é igual ao Modo Contínuo.
   ```py
   ./ar_paint.py -j <ficheiro JSON> -n
   ```

## Contactos

* Mateus Araújo - mateus.araujo@ua.pt
* Rafael Mendes - mendes.rafael@ua.pt

Link do Projeto: https://github.com/maateusjo/PSR-Aumented-Reality-Paint
