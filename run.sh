#!/bin/bash

# Executa o script de limpeza (assumindo que é um script Bash)
source cleanup.sh

# Define os caminhos das bibliotecas
flex="lib/jflex-full-1.9.1.jar"
cup="lib/java-cup-11b.jar"
libs=".:lib/java-cup-11b.jar:lib/java-cup-11b-runtime.jar:lib/jflex-1.8.2.jar"

# Gera o analisador léxico com JFlex
java -jar "$flex" calc.flex

# Gera o parser com Java CUP
java -jar "$cup" -parser parser -symbols sym calc.cup

# Compila todos os arquivos .java com o classpath apropriado
javac -cp "$libs" *.java

# Executa a classe Main
java -cp "$libs" Main
