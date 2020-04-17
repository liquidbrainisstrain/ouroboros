from modules import fasta_parser as fp

covid_prots = fp('/Users/liquidbrain/projects/Proteomics/sars-ncov-2019/coronavirus.fasta')

print(len(covid_prots))