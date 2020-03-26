from modules import fasta_parser as fp
import pprint

covid_prots = fp('/Users/liquidbrain/projects/Proteomics/sars-ncov-2019/coronavirus.fasta')

print(len(covid_prots))