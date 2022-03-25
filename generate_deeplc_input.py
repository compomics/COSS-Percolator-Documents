import pandas as pd
import glob
import os

output_path = ("C:/Users/Genet/OneDrive - UGent/New_COSS_Analysis/COSS_results_NIST_old/din/kuster_01277")
paths_ =[]
# paths_.append("C:/Users/Genet/OneDrive - UGent/New_COSS_Analysis/COSS_results_NIST_old/kuster_01277")


for path_ in paths_:
    resultFiles = glob.glob(path_ + "/*.tab")

    for file_ in resultFiles:
        file_name = os.path.basename(file_)
        file_name = os.path.splitext(file_name)[0]
        df = pd.read_csv(file_,  sep='\t')
        
        # df = df[df['Validation(FDR)'] <= 0.01]
        # df = df[df['Library'] == 1]
        # df = df[['Title','Sequence', 'Mods', 'RetentionT']]

        df.rename(columns={"Sequence": "seq", "Mods": "modifications", "RetentionT": "tr"}, inplace=True)
        temp_mods=[]

        for indx, rows in df.iterrows():
            mod=rows['modifications']
            if(mod == '0'):
                temp_mods.append(mod)

            else:
                mods_list = []
                mods_list = mod.split("/")
                del mods_list[0]
                ms=[]
                count=0;
                new_mod=''
                for m in mods_list:
                    ms = m.split(',')
                    mod_deeplc=ms[2]
                    if mod_deeplc=='CAM':
                        mod_deeplc = 'Carbamidomethyl'
                    elif mod_deeplc == 'Pyro-cmC':
                        mod_deeplc = 'Pyro-carbamidomethyl'
                    elif mod_deeplc == 'Pyro-glu':
                        mod_deeplc = 'Pro->pyro-Glu'

                    new_mod= new_mod + ms[0] + '|' + mod_deeplc

                    count+=1
                    if(count<len(mods_list)):
                        new_mod = new_mod + '|'
                temp_mods.append(new_mod)
        df['modifications'] = temp_mods

        df.to_csv(output_path + 'dIN_predict' + file_name +'.csv', encoding='utf-8', index=False, header=True)
        # dfc.to_csv(output_path + 'dIN_calibrate' + file_name +'.csv', encoding='utf-8', index=False, header=True)
        print(file_ + " completed")
