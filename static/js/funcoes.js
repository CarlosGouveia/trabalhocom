// Mascara para CPF

var opcoes = {onKeyPress: function(cpf, e, field, opcoes){
    mascara = '000.000.000-00';
    $('[name=cpf]').mask(mascara, opcoes);
}};
$('[name=cpf]').mask('000.000.000-00', opcoes);

// fim

// Mascara para telefone

var opcoes = {onKeyPress: function(telefone, e, field, opcoes){
    mascara = (telefone.length > 14)? '(00) 00000-0000' : '(00) 0000-00009';
    $('[name=telefone]').mask(mascara, opcoes);
}};
$('[name=telefone]').mask('(00) 0000-00009', opcoes);

// fim


// Mascara para telefone_contato

var opcoes = {onKeyPress: function(telefone, e, field, opcoes){
    mascara = (telefone.length > 14)? '(00) 00000-0000' : '(00) 0000-00009';
    $('[name=telefone_contato]').mask(mascara, opcoes);
}};
$('[name=telefone_contato]').mask('(00) 0000-00009', opcoes);

// fim

// Mascara para RG

// var maskrg = {onKeyPress: function(rg, e, field, maskrg){
//     mascara ='00.000.000';
//     $('[name=rg]').mask(mascara, maskrg);
// }};
// $('[name=rg]').mask('00.000.000', maskrg);

// fim

// Mascara para Data de Nascimento

var opcoes = {onKeyPress: function(dt_nasc, e, field, opcoes){
    mascara ='00/00/0000';
    $('[name=dt_nasc]').mask(mascara, opcoes);
}};
$('[name=dt_nasc]').mask('00/00/0000', opcoes);

// fim

// Mascara para valor

var opcoes = {onKeyPress: function(valor, e, field, opcoes){
    mascara ='00,00';
    $('[name=valoor]').mask(mascara, opcoes);
}};
$('[name=valoor]').mask('00,00', opcoes);

// fim


// Mascara para RG

var maskrg= {onKeyPress: function(rg, e, field, maskrg){
    if (rg.length > 12)
        mascara = '00.000.000-00';
    else if (rg.length > 11)
        mascara = '00.000.000-09';
    else
        mascara = '00.000.000-99';
    $('[name=rg]').mask(mascara, maskrg);
}};
$('[name=rg]').mask('00.000.000-99', maskrg);

// fim