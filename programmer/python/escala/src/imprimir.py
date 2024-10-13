import os
import pandas as pd
from fpdf import FPDF

# Função para adicionar o cabeçalho no PDF
def adicionar_cabecalho(pdf, dados):
    local = f'{dados[3]} (24/72 h)'
    pdf.set_font('Arial', 'B', 10)
    pdf.cell(0, 5, 'DDC - Diretoria de Des. das Cidades', ln=True, align='C')
    pdf.cell(0, 5, 'GNR-4.2 - Gerencia Noroeste / Produção', ln=True, align='C')
    pdf.cell(0, 5, local, ln=True, align='C')
    pdf.image('dados/cedae.png', x=25, y=7, w=30, h=10)
    pdf.image('dados/rj.png', x=155, y=7, w=30, h=10)

# Função para calcular a largura das colunas com base no DataFrame
def calcular_largura_colunas(df):
    column_widths = []
    for column in df.columns:
        if column != 'Férias':  # Ignora a coluna "Férias"
            max_length = max(df[column].astype(str).map(len).max(), len(column))
            column_widths.append(max_length * 3.7)  # Ajusta a largura da célula
    return column_widths

# Função para calcular a largura total da tabela
def calcular_largura_total(column_widths):
    return sum(column_widths)

# Função para adicionar o cabeçalho da tabela no PDF (modificada)
def adicionar_cabecalho_tabela(pdf, df, column_widths):
    total_width = calcular_largura_total(column_widths)
    margem_esquerda = pdf.l_margin  # Margem esquerda
    largura_pagina = pdf.w - 2 * margem_esquerda  # Largura útil da página
    x_start = margem_esquerda + (largura_pagina - total_width) / 2  # Centraliza a tabela
    x_start = margem_esquerda + (largura_pagina - total_width) / 2  # Centraliza a tabela
    if x_start<1:
        x_start=1
    pdf.set_font('Arial', 'B', 10)
    pdf.set_x(x_start)
    for i, column in enumerate(df.columns):
        if column != 'Ferias':  # Ignora a coluna "Férias"
            pdf.cell(column_widths[i], 8, column, border=1, align='C')
    pdf.ln()

# Função para adicionar as linhas da tabela no PDF (modificada)
def adicionar_linhas_tabela(pdf, df, column_widths):
    total_width = calcular_largura_total(column_widths)
    margem_esquerda = pdf.l_margin  # Margem esquerda
    largura_pagina = pdf.w - 2 * margem_esquerda  # Largura útil da página
    x_start = margem_esquerda + (largura_pagina - total_width) / 2  # Centraliza a tabela

    if x_start<1:
        x_start=1
    pdf.set_font('Arial', '', 10)
    for _, row in df.iterrows():
        pdf.set_x(x_start)
        for i, item in enumerate(row):
            if df.columns[i] == 'Ferias':
                continue  # Ignora a coluna "Férias"
            aplicar_cor_condicional(pdf, i, row, item)
            if i == 3 and 'nan' in str(item):
                item = ""
            pdf.cell(column_widths[i], 7, str(item), border=1, align='C')
        pdf.ln()

# Função para adicionar observações no final do PDF
def adicionar_observacoes(pdf):
    pdf.set_text_color(100, 100, 100)
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 5, "", ln=True, align="L")
    pdf.cell(0, 5, "Observações:", ln=True, align="L")
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 5, 'Ferias: ', align="L")

# Função para aplicar cores com base nas condições
def aplicar_cor_condicional(pdf, i, row, item):
    if i == 2 and pd.notna(row.iloc[3]) and str(row.iloc[3]) != "0":
        pdf.set_text_color(0, 0, 150)  # Cor específica
    elif i == 1 and ('Sábado' in str(item) or 'Domingo' in str(item)):
        pdf.set_text_color(128, 0, 0)  # Cor para sábados e domingos
    else:
        pdf.set_text_color(0, 0, 0)  # Reseta para preto

# Função principal para gerar o PDF
def gerar_pdf(df, output):
    pdf = FPDF()
    pdf.add_page()

    adicionar_cabecalho(pdf, output)
    column_widths = calcular_largura_colunas(df)
    
    # Adicionar cabeçalho da tabela (centralizado)
    adicionar_cabecalho_tabela(pdf, df, column_widths)
    
    # Adicionar linhas da tabela (centralizado)
    adicionar_linhas_tabela(pdf, df, column_widths)
    
    adicionar_observacoes(pdf)

    pasta_destino = f'pdf/{output[1]}/{output[2]}'
    os.makedirs(pasta_destino, exist_ok=True)

    arquivo_saida = f'{pasta_destino}/{output[3]}.pdf'
    pdf.output(arquivo_saida)

    print(f"PDF gerado com sucesso: {arquivo_saida}")

# Função principal
def main(df, ano, mes, arq):
    obter = [0, ano, mes, arq]
    gerar_pdf(df, obter)

# Executar o programa
#if __name__ == "__main__":
    # Exemplo de DataFrame para teste
#    main()
