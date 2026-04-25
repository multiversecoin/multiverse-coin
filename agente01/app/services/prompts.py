"""Prompts for LLM text generation — reusable and auditable."""

SYSTEM_PROMPT = """Você é um engenheiro técnico especializado em serviços subaquáticos.
Você escreve relatórios técnicos formais, objetivos e precisos.

REGRAS OBRIGATÓRIAS:
- NUNCA invente dados que não foram fornecidos.
- Se um dado estiver ausente, use "NÃO INFORMADO".
- Use linguagem técnica formal, frases curtas e claras.
- Sem exagero, sem floreio, sem achismos.
- Não cite normas específicas se não foram fornecidas.
- Termos padrão quando aplicável: corrosão, bioincrustação, incrustação, trinca, deformação, obstrução, anodo, pintura deteriorada, desgaste, limpeza realizada.
"""

PROMPT_INTRODUCAO = """Com base nos dados abaixo, escreva a seção INTRODUÇÃO do relatório técnico.
A introdução deve contextualizar o serviço prestado, o cliente e o local.

Dados da operação:
- Cliente: {cliente}
- Navio: {navio}
- IMO: {imo}
- Local: {local}
- Porto: {porto}
- Data: {data_operacao}
- Tipo de serviço: {tipo_servico}
- Descrição: {descricao_servico}

Escreva de forma técnica, formal e objetiva. Máximo 3 parágrafos."""

PROMPT_METODOLOGIA = """Com base nos dados abaixo, escreva a seção METODOLOGIA EXECUTADA.

Tipo de serviço: {tipo_servico}
Áreas inspecionadas: {areas}
Equipamentos utilizados: {equipamentos}
Condições operacionais:
- Visibilidade: {visibilidade}
- Correnteza: {correnteza}
- Maré: {mare}
- Observações: {obs_condicoes}

Descreva a metodologia de forma técnica e objetiva. Máximo 4 parágrafos."""

PROMPT_ACHADOS = """Com base nas evidências e observações abaixo, escreva a seção DIAGNÓSTICO / ACHADOS TÉCNICOS.

Áreas inspecionadas: {areas}
Observações de campo: {observacoes_campo}
Observações dos operadores nas evidências:
{observacoes_evidencias}

REGRAS:
- Não afirme defeitos se não houver evidência ou observação do operador.
- Use "NÃO INFORMADO" se faltar dados.
- Se houver pendências, liste em seção separada.
Máximo 5 parágrafos."""

PROMPT_CONCLUSAO = """Com base nos dados abaixo, escreva a seção CONCLUSÃO do relatório.

Tipo de serviço: {tipo_servico}
Áreas inspecionadas: {areas}
Achados principais: {achados_resumo}
Observações de campo: {observacoes_campo}

Escreva uma conclusão técnica, objetiva e formal. Máximo 3 parágrafos."""

PROMPT_RECOMENDACOES = """Com base nos dados abaixo, escreva a seção RECOMENDAÇÕES TÉCNICAS.

Tipo de serviço: {tipo_servico}
Achados principais: {achados_resumo}
Recomendações iniciais do campo: {recomendacoes_iniciais}

Liste recomendações técnicas objetivas e acionáveis. Use formato de lista numerada."""

PROMPT_LEGENDA = """Gere uma legenda técnica curta e formal para esta fotografia de inspeção subaquática.

Área: {area}
Tags: {tags}
Observação do operador: {observacao}

REGRAS:
- Legenda curta e objetiva.
- Nunca inventar defeitos não descritos.
- Se não houver contexto suficiente, use: "Registro fotográfico da área inspecionada."
- Use termos padrão quando aplicável: corrosão, bioincrustação, incrustação, trinca, deformação, obstrução, anodo, pintura deteriorada, desgaste, limpeza realizada.

Retorne APENAS a legenda, sem aspas."""
