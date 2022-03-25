import pandas as pn
import glob
import os

output_path= ("C:/Users/Genet/OneDrive - UGent/New_COSS_Analysis/COSS_rescored_NIST2020/")


paths_ =[]
paths_.append("C:/Users/Genet/OneDrive - UGent/New_COSS_Analysis/COSS_results_NIST2020")
# paths_.append("C:/Users/Genet/OneDrive - UGent/New_COSS_Analysis")
# paths_.append("C:/Users/Genet/OneDrive - UGent/New_COSS_Analysis")

pathnum=0;
for path_ in paths_:
    resultFiles = glob.glob(path_ + "/*.tab")
    pathnum += 1;
    for file_ in resultFiles:
        file_name = os.path.basename(file_)
        file_name = os.path.splitext(file_name)[0]
        df = pn.read_csv(file_,  sep='\t')


        df.rename(columns={"Title": "id", 'Scan No.': 'ScanNr', 'Library': 'label', 'Sequence': 'Peptide', 'Prec. Mass': 'precMass', 'Protein': 'Proteins', 'ChargeLib': 'Charge'}, inplace=True)

        # df.loc[df['label']== 1, 'label'] = 1
        df.loc[df['label'] == 0, 'label'] = -1

        df['Proteins'] = df['Proteins'].str.split('|').str[1] #activate for NIST library results and diactivate for MassIVE
        # df['Proteins'] = 'P68032' #deactivate for NIST and activate for MassIVE

        # df['id'] = df['id'].str.split(' ').str[0] + ' ' + 'Mass:' + df['precMass'].map(str)
        # df['id'] = df['id'] + ' ' + 'Mass:' + df['precMass'].map(str)

        df['id']=df['id'].str.replace('TITLE=', '')

        cols=['id', 'label', 'ScanNr', 'RetentionT', 'precMass', 'ChargeQuery', 'Score', 'CosineSim', 'MSE_Int','MSE_MZ', 'spearman_corr', 'pearson_corr',  'pearson_log2_corr', 'Score_2nd','Score_3rd','#MatchedPeaksQueryFraction', '#MatchedPeaksLibFraction','SumMatchedIntQueryFraction', 'SumMatchedIntLibFraction', 'Peptide','Proteins']  #all features
        df_temp = df[cols]
        df_temp.to_csv(output_path + 'all_features/pin_files_5' + '/PIN_' + file_name +'.tab', encoding='utf-8', sep='\t', index=False, header=True)


        print(file_ + " completed")
