# SdS / Jôna RPG

Bem vindo a SdS / Jôna RPG (ainda não tenho um nome bom o suficiente para esse
sistema). Esse é um sistema de RPG adaptado de D&D 5e para o universo de O
Senhor das Sombras (o meu universo de RPG).

Nesse universo, todas as criaturas possuem algum tipo de familiaridade com a
magia e todos sabem como utilizar pelo menos alguns pequenos truques mágicos.
Por conta disso, todas as classes utilizam **mana**, e todas as classes sabem
conjurar magia. Além disso, todo personagem pertence a uma Ordem/Escola mágica,
que geralmente é uma Escola elemental, como Ar, Fogo, Terra... Cada Ordem possui
as próprias magias que ela sabe conjurar (e.g. a Ordem da Água é mais focada em
cura e buffs).

Por fim, há algumas outras modificações e coisas novas que eu estou adicionando
com o tempo e você pode obter mais informações lendo o livro de regras.

## Sobre o Repositório

O repositório está dividido em duas pastas principais.

A primeira é a pasta de `Regras`, que contém PDFs com as regras adaptadas e com
as magias adaptadas (pois toda magia agora gasta mana). Dentro dessa pasta, há
os arquivos `rules.pdf` e `Spells.pdf`. Além deles, há também os arquivos fonte
desses PDFs, escritos em LaTeX.

A segunda pasta é a `Magias`, onde estão todas as magias adaptadas até então e
também alguns arquivos de script que ajudam no dia-a-dia. As magias em si estão
dentro de `Magias/data`, onde cada magia é um arquivo `.json`. Esses arquivos
são lidos em Python utilizando a biblioteca `pandas` utilizando os arquivos
Python dentro de `Magias/dfs`. Então, os arquivos dentro de `Magias/spell` podem
ser utilizados para mostrar esses dados de formas diversas, como utilizando um
`notebook` `Jupyter` ou então exportá-las para um arquivo `.tex` e `.pdf`. Em
particular, o arquivo `export_filtered_spells.py` é um arquivo script `python`
que pode ser rodado para criar esses arquivos `.pdf` de maneira facilitada.

Para executá-lo, você precisa ter o `Python` instalado no seu computador e as
bibliotecas listadas no arquivo `requirements.txt`. Para instalá-las usando o
python, você pode usar um `package manager` (e.g. o `pip`):

```bash
pip install -r requirements.txt
```

E depois, basta executar o script:

```
python ./Magias/export_filtered_spells.py --help
```

Ao executar o `--help`, o script mostrará todos os comandos disponíveis para
utilizá-lo. Caso você ache que algo pode ser acrescentado, basta me enviar um
PR. =)
