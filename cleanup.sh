#!/bin/bash

# Remove parser.java se existir
[ -f parser.java ] && rm parser.java

# Remove sym.java se existir
[ -f sym.java ] && rm sym.java

# Remove scanner.java se existir
[ -f scanner.java ] && rm scanner.java  

# Remove todos os arquivos .class recursivamente
find . -name "*.class" -type f -delete
