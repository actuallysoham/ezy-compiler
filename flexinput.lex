
DIGIT       [0-9]
NUM         {DIGIT}{DIGIT}*
U_LETTER    [A-Z]
L_LETTER    [a-z]
UNDERSCORE  "_"
ID          ({U_LETTER}|{L_LETTER})({UNDERSCORE}|{U_LETTER}|{L_LETTER})*
STRING      "{.}"
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
CMP_OP      < | > | <= | >= | = | <>
ARITH_OP    + | - | * | /

OPD         {ID} | {NUM}

ASSIGN      {ID} = {OPD} {ARITH_OP} {OPD}
CONDJUMP    {IF_KW} {ID} {CMP_OP} {ID} {GOTO_KW} {NUM}
JUMP        {GOTO_KW} {NUM}
READSTMT    {READ_KW} {ID}
PRINTSTMT   {PRINT_KW} {PRINTARG} | PRINTLN_KW
PRINTARG    {ID} | {STRING}
CALLSTMT    {CALL_KW} {ID}"("{ARGLIST}")"
ARGLIST     {TARGLIST} | [:blank:]
TARGLIST    {ID} {TARGLIST} | {ID}

PROCDECL    {PROC_KW} {ID} "(" ")"
PARAMLIST   {TPARAMLIST} | [:blank:]
TPARAMLIST  {PARAM}, {TPARAMLIST} | {PARAM}
PARAM       {MODE} {ID}
MODE        {IN_KW} | {OUT_KW} | {INOUT_KW}
STMTLIST    {PSTMT} {STMTLIST} | {PSTMT}
PSTMT       {DLABEL} | {STMT} ";"
STMT        {ASSIGN} | {CONDJUMP} | {JUMP} | {READSTMT} | {PRINTSTMT} | {CALLSTMT} | {RET_KW} | {EXIT_KW}

 


%%



%%