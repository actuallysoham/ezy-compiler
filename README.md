# ezy-compiler
PLDI Course Project


## Grammar

```
<prog> := <vardecls> <procdecls> begin <stmtlist> end
<vardecls> := <vardecl> <verdecls> | 
<vardecl> := var <varlist> ;
<varlist> := id <varlist> | id
<procdecls> := <procdecl> <procdecls> |
<procdecl> := proc id(<paramlist>) <vardecls> <stmtlist>
<paramlist> := <tparamlist> | 
<tparamlist> := <param> , <tparamlist> | <param>
<param> := <mode> id
<mode> := in | out | inout
<stmtlist> := <pstmt> <stmtlist> | <pstmt>
<pstmt> := dlabel | <stmt> ;
<stmt> :=  <assign> | <condjump> | <jump> | <readstmt> | <printstmt>  | <callstmt> 
                                  | return | exit 
<assign> := id = <opd> <arithop> <opd> 
<condjump> : = if id cmpop id goto label
<jump> :=  goto label
<readstmt := read id
<printstmt> := print <printarg> | println 
<printarg> := id | string 
<callstmt> := call id(<arglist>)
<arglist> := <targlist> |
<targlist> :=  id <targlist> | id
<cmpop> := < | > | <= | >= | = | <>

<arithop> := + | - | * | / 
<opd> :=  id | num
```