import pandas as pn
import glob
import os

output_path= "C:/Users/compomics/OneDrive - UGent/New_COSS_Analysis/ReviewAnalysis/ms2pip_INputAndResult/kuster01277/kuster01277_result_massive/"

paths_ =[]
paths_.append("C:/Users/compomics/OneDrive - UGent/New_COSS_Analysis/ReviewAnalysis/ms2pip_INputAndResult/kuster01277/kuster01277_result_massive")

def generate_input():
    for path_ in paths_:
        resultFiles = glob.glob(path_ + "/*.tab")
        for file_ in resultFiles:
            file_name = os.path.basename(file_)
            file_name = os.path.splitext(file_name)[0]
            df = pn.read_csv(file_, sep='\t')
            df = df[df['Validation(FDR)'] <= 0.01]

            df.rename(columns={"Title": "spec_id", "Sequence" : "peptide", "Mods" : "modifications", "ChargeQuery" : "charge"}, inplace=True)

            temp_mods = []
            for indx, rows in df.iterrows():
                mod = rows['modifications']
                if (mod == '0' or mod==None):
                    temp_mods.append('-')
                else:
                    mods_list = []
                    mods_list = mod.split("/")
                    del mods_list[0]
                    ms = []
                    count = 0;
                    new_mod = ''
                    for m in mods_list:
                        ms = m.split(',')
                        mod_deeplc = ms[2]

                        if mod_deeplc == 'Deamidation':
                            mod_deeplc = 'Deamidated'
                        elif mod_deeplc == 'Carbamyl':
                            mod_deeplc = 'Carbamidomethyl'
                        elif mod_deeplc == 'CAM':
                            mod_deeplc = 'Carbamidomethyl'
                        elif mod_deeplc == 'Pyro-cmC':
                            mod_deeplc = 'Pyro-carbamidomethyl'
                        elif mod_deeplc == 'Pyro-glu':
                            mod_deeplc = 'Gln->pyro-Glu'
                        elif mod_deeplc == 'Pyro_glu':
                            mod_deeplc = 'Glu->pyro-Glu'

                        new_mod = new_mod + str(int(ms[0]) + 1) + '|' + mod_deeplc
                        count += 1
                        if (count < len(mods_list)):
                            new_mod = new_mod + '|'
                    temp_mods.append(new_mod)

            df['modifications'] = temp_mods

            df['peptide']=df['peptide'].str.split('_').str[0]
            df['charge'] = df['charge'].str.extract('(\d+)', expand=False)
            df['charge'] = df['charge'].astype(int)

            #aply string split when needed
            #df['id'] = df['id'].str.split('/').str[0]
            cols = ['spec_id', 'modifications', 'peptide', 'charge', 'Library']
            df = df[cols]
            df.to_csv(output_path + file_name +'.tab', encoding='utf-8', sep='\t', index=False)
            print(file_ + " completed")

generate_input();
