
DIGIT       [0-9]
NUM         {DIGIT}{DIGIT}*
U_LETTER    [A-Z]
L_LETTER    [a-z]
UNDERSCORE  "_"
ID          ({U_LETTER}|{L_LETTER})({UNDERSCORE}|{U_LETTER}|{L_LETTER})*
SYMB        ! | @ | # | $ | % | ^ | & | [ | ] | "{" | "}" | ? | ' | :
VALID_CHARS [A-Z] | [a-z] | [ ] | [\t] | [0-9] | {CMP_OP} | {ARITH_OP} | {OPEN_PAR} | {CLOSE_PAR} | {SYMB}
STRING      {QUOTES} {VALID_CHARS}* {QUOTES}
BEGIN_KW    begin
END_KW      end
VAR_KW      var
PROC_KW     proc
IN_KW       in
OUT_KW      out
INOUT_KW    inout
RET_KW      return
EXIT_KW     exit
IF_KW       if
GOTO_KW     goto
READ_KW     read
PRINT_KW    print
PRINTLN_KW  println
CALL_KW     call
EQUALS      =
CMP_OP      < | > | <= | >= | {EQUALS} | <>
ARITH_OP    + | - | * | /
QUOTES      "
OPEN_PAR    "("
CLOSE_PAR   ")"
SEMICOL     ";"
COMMA       ","

OPD         {ID} | {NUM}

ASSIGN      {ID} {EQUALS} {OPD} {ARITH_OP} {OPD}
CONDJUMP    {IF_KW} {ID} {CMP_OP} {ID} {GOTO_KW} {NUM}
JUMP        {GOTO_KW} {NUM}
READSTMT    {READ_KW} {ID}
PRINTSTMT   {PRINT_KW} {PRINTARG} | {PRINTLN_KW}
PRINTARG    {ID} | {STRING}
CALLSTMT    {CALL_KW} {ID}{OPEN_PAR}{ARGLIST}{CLOSE_PAR}
ARGLIST     {TARGLIST} | [:blank:]
TARGLIST    {ID} {TARGLIST} | {ID}


PROG        {VARDECLS} {PROCDECLS} {BEGIN_KW} {STMTLIST} {END_KW}
VARDECLS    {VARDECL} {VARDECLS} | [:blank:]
VARDECL     {VAR_KW} {VARLIST} {SEMICOL}
VARLIST     {ID} {VARLIST} | {ID}
PROCDECLS   {PROCDECL} {PROCDECLS} | [:blank:]
PROCDECL    {PROC_KW} {ID}{OPEN_PAR{VARDECLS}{CLOSE_PAR}{STMTLIST}
PARAMLIST   {TPARAMLIST} | [:blank:]
TPARAMLIST  {PARAM}{COMMA} {TPARAMLIST} | {PARAM}
PARAM       {MODE} {ID}
MODE        {IN_KW} | {OUT_KW} | {INOUT_KW}
STMTLIST    {PSTMT} {STMTLIST} | {PSTMT}
PSTMT       {DLABEL} | {STMT} {SEMICOL}
STMT        {ASSIGN} | {CONDJUMP} | {JUMP} | {READSTMT} | {PRINTSTMT} | {CALLSTMT} | {RET_KW} | {EXIT_KW}

 


%%

{ASSIGN} printf("(ASSIGN, %s)", yytext);


%%

main() {
    printf("write ur stmt: \n");
    yylex();
}