import java_cup.runtime.*;

%%

%class scanner
%unicode
%cup

// %{
//   // Métodos auxiliares para criar Symbols com linha e coluna
//   private Symbol new symbol(int type) {
//       return new new symbol(type, yyline, yycolumn);
//   }
//   private Symbol new symbol(int type, Object value) {
//       return new new symbol(type, yyline, yycolumn, value);
//   }
// %}

// Definições de macros
DIGIT   = [0-9]
DIGITS  = {DIGIT}+
LETTER  = [a-zA-Z]
ID      = {LETTER}({LETTER}|{DIGIT})*  // não pode iniciar com número, mas pode conter letras e números depois
WS      = [ \t\r\n]+

%%

// Ignora espaços em branco
{WS}                             { /* nada */ }

// Comentários de linha única
"entre nos".*                    { /* ignora comentário */ }

// Comentários de múltiplas linhas
"/*"([^*]|(\*+[^*/]))*"*/"      { /* ignora comentário */ }

// Palavras-chave
"veja bem"                     { return new symbol(sym.IF); }
"olha só"                      { return new symbol(sym.ELSE); }
"so faz"                       { return new symbol(sym.WHILE); }
"faz e conta, é o bixao mesmo" { return new symbol(sym.FOR); }
"atmega"                       { return new symbol(sym.RETURN); }
"bitcoin"                      { return new symbol(sym.TRUE); }
"nao_bitcoin"                  { return new symbol(sym.FALSE); }

// Delimitadores
",ta ligado?"                  { return new symbol(sym.SEMI); }
", e digo mais,"               { return new symbol(sym.COMMA); }
"{"                            { return new symbol(sym.LBRACE); }
"}"                            { return new symbol(sym.RBRACE); }

// Parênteses
"("                            { return new symbol(sym.LPAREN); }
")"                            { return new symbol(sym.RPAREN); }

// Operadores aritméticos
"maizi"                        { return new symbol(sym.PLUS); }
"menoz"                        { return new symbol(sym.MINUS); }   // operador unário e binário são iguais aqui
"veiz"                        { return new symbol(sym.MUL); }
"mei"                         { return new symbol(sym.DIV); }

// Operadores de comparação com dois caracteres (mais específicos primeiro)
"mais que uma ruma de"          { return new symbol(sym.GE); }
"menos que uma ruma de"         { return new symbol(sym.LE); }
"se for"                       { return new symbol(sym.EQ); }
"pior que nao e"               { return new symbol(sym.NE); }

// Operadores de comparação simples
"mais maior que"               { return new symbol(sym.GT); }
"mais menor que"              { return new symbol(sym.LT); }

// Números: inteiros ou ponto flutuante
{DIGITS}"."{DIGITS}             { return new symbol(sym.NUMBER, Double.parseDouble(yytext())); }
{DIGITS}                       { return new symbol(sym.NUMBER, Double.parseDouble(yytext())); }

// Operador de atribuição
"eh"                           { return new symbol(sym.ASSIGN); }

// Identificadores (que não sejam palavras-chave)
{ID}                           { return new symbol(sym.ID, yytext()); }

// Qualquer outro caractere inválido causa erro
.                             { throw new Error("Caracter inválido: " + yytext()); }
