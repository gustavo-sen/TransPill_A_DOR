import java_cup.runtime.*;
import java.util.List;
import java.util.ArrayList;

%%

%class scanner
%unicode
%cup

// Definições de macros
DIGIT   = [0-9]
DIGITS  = {DIGIT}+
LETTER  = [a-zA-Z]
ID      = {LETTER}({LETTER}|{DIGIT})*  // não pode iniciar com número, mas pode conter letras e números depois
WS      = [ \t\r\n]+

%%

// Ignora espaços em branco
{WS}                      { /* nada */ }

// // Comentários de linha única
"entre nos"[^\n]*         { /* ignora comentário */ }

// // Comentários de múltiplas linhas
"/"([^]|(\+[^/]))"/"      { /* ignora comentário */ }

// Saudações (ignore case e espaços extras)
 "bom dia"      { return new Symbol(sym.BOM_DIA);   }
 "boa tarde"    { return new Symbol(sym.BOA_TARDE); }
 "boa noite"    { return new Symbol(sym.BOA_NOITE); }

// Palavras-chave
"veja bem"                      { return new Symbol(sym.IF); }
"olha só"                       { return new Symbol(sym.ELSE); }
"so faz"                        { return new Symbol(sym.WHILE); }
//"faz e conta, e o bixao mesmo"  { return new Symbol(sym.FOR); }
//"atmega"                        { return new Symbol(sym.RETURN); }
"bitcoin"                       { return new Symbol(sym.TRUE); }
"nao_bitcoin"                   { return new Symbol(sym.FALSE); }

// Delimitadores
", ta ligado?"                  { return new Symbol(sym.SEMI); }
", e digo mais,"                { return new Symbol(sym.COMMA); }
"{"                             { return new Symbol(sym.LBRACE); }
"}"                             { return new Symbol(sym.RBRACE); }

// Parênteses
"("                             { return new Symbol(sym.LPAREN); }
")"                             { return new Symbol(sym.RPAREN); }

// Operadores aritméticos
"maizi"                         { return new Symbol(sym.PLUS); }
"-"                             { return new Symbol(sym.MINUS); }   // operador unário e binário são iguais aqui
"veiz"                          { return new Symbol(sym.MUL); }
"mei"                           { return new Symbol(sym.DIV); }
// SUGESTAO PARA OPERADORES ARITIMETICOS
// ":)"                        { return new Symbol(sym.PLUS); }
// ":("                        { return new Symbol(sym.MINUS); }  
// "veiz"                        { return new Symbol(sym.MUL); }
// ":|"                         { return new Symbol(sym.DIV); }


// Operadores de comparação com dois caracteres (mais específicos primeiro)
"mais que uma ruma de"          { return new Symbol(sym.GE); }
"menos que uma ruma de"         { return new Symbol(sym.LE); }
"se for"                        { return new Symbol(sym.EQ); }
"pior que nao e"                { return new Symbol(sym.NE); }

// Operadores de comparação simples
"mais maior que"                { return new Symbol(sym.GT); }
"mais menor que"                { return new Symbol(sym.LT); }

"serasa"                        {return new Symbol(sym.UMINUS);} // quando o omi ta devendo -2 -3 etc

// Números: inteiros ou ponto flutuante
{DIGITS}"."{DIGITS}             { return new Symbol(sym.NUMBER, Double.parseDouble(yytext())); }
{DIGITS}                        { return new Symbol(sym.NUMBER, Double.parseDouble(yytext())); }

// Operador de atribuição
"eh"                            { return new Symbol(sym.ASSIGN); }

// Identificadores (que não sejam palavras-chave)
{ID}                            { return new Symbol(sym.ID, yytext()); }

// Qualquer outro caractere inválido causa erro
.                               { throw new Error("Caracter inválido: " + yytext()); }

