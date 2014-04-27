# -*- coding:utf-8 -*-
'''
@author:: Bruno Zeraik
'''

user_label = 'Usuário'
password_label = 'Senha'


error_messages = {
    'required': u'Este campo é obrigatório.',
    'max_length': u'Este campo tem que ter no máximo %(limit_value)s caracteres.',
    'min_length': u'Este campo tem que ter no mínimo %(limit_value)s caracteres.',
    'invalid_choice': u'Opção inválida selecionada.',
    'can_not_remove_all': u'Não foi possível excluir nenhum dos itens selecionados.',
    'can_not_remove': u'Não foi possível excluir alguns dos itens selecionados: %s.',
    'can_not_remove_error': u'A exclusão dos itens selecionados não foi concluída.',
    'select_one': u'Nenhum item foi selecionado.',
    'invalid_param': u'Valor do %s nulo ou inválido.',
    'invalid': u'%s inválido ou não cadastrado.',
    'default_error': u'Falha ao acessar a fonte de dados.',
    'not_registered': u'Este registro não está cadastrado.',
    'can_not_hide_all': u'Não foi possível ocultar nenhum dos itens selecionados.',
    'can_not_hide': u'Não foi possível ocultar alguns dos itens selecionados: %s.',
    'can_not_hide_error': u'A ocultação dos itens selecionados não foi concluída.',
    'duplicated': u'Já existe um %s cadastrado com as mesmas características.',
    'can_not_remove': u'Não foi possível excluir algum(ns) item(ns).',
    'http_error': u'Erro ao realizar requisição REST com o SERVICE.',
    'http_error': u'Erro ao realizar requisição REST com o SERVICE.',
    'no_permission': u'Usuário não autorizado para acessar/executar esta operação. ',
    'communication_error': u'Erro ao realizar comunicação com o serviço %s.',
    '404': u'Página não encontrada.',
    '500': u'Ocorreu um erro interno. Por favor contate o administrador do sistema.',
    'min_length_search': u'É necessário informar no mínimo %s caracteres para realizar a busca.',
    'max_length_search': u'É necessário informar no máximo %s caracteres para realizar a busca.',
}

success_messages = {
    'success_remove': u'Todos os itens selecionados foram removidos com sucesso.',
    'success_hide': u'Todos os itens selecionados foram ocultados com sucesso.',
    'success_insert': u'Cadastro realizado com sucesso.',
    'success_edit': u'Edição realizada com sucesso.',
    'success_remove_single': u'Remoção realizada com sucesso.',
}


user_messages = {
    'invalid_user': u'Usuário inválido ou não cadastrado.',
    'invalid_pass': u'Senha inválida.',
    'invalid_user_or_pass': u'Usuário e/ou senha inválida.',
    'inactive_user': u'Usuário inativo ou excluído.',
    'duplicated_username': u'Já existe um usuário cadastrado com o valor "%s".',
    'not_authenticated': u'Usuário não autenticado.',
    'ldap_offline': u'O LDAP não está disponível, não será possível realizer login com um usuário do LDAP.',

    'success_link': u'Usuário vinculado a um contato com sucesso.',
    'error_link': u'Não foi possível vincular o contato ao usuário.',
    'already_linked': u'Seu usuário já está vinculado a algum contato.',
    'someone_is_already_linked': u'O usuário %s já está vinculado ao contato %s.',
    'success_create_and_link': u'O contato foi criado e vinculado ao usuário com sucesso.',
    'edit_profile_not_available': u'Esta funcionalidade só estará disponível após o vínculo do seu usuário com este contato for aprovado.',

    'invalid_basic_header': u'Cabeçalho básico inválido.',
    'invalid_token_header': u'Cabeçalho de token inválido.',
    'invalid_token': u'Token inválido.',

    'not_vinculed_contact': u'O usuário logado não está mais vinculado a um contato.',

    'invalid_confirm_password': u'Confirmação de senha incorreta.',
}
