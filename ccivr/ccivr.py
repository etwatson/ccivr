from webbrowser import get
import pandas as pd
import os
from ccivr.getargs import get_path
import ccivr.exception as e

def find_cisnats(df0,df1,filter):
    '''
    Finds cisNats of genes on one strand from those on the other strand.
    df0 and df1 are the sets of information about genes on different strands.
    One finding process is composed by following steps.
        1. Picking up one target gene from df0.
        2. Extracting its cisNats from df1.
            1) Chromosomal selection
            2) Locational selection
        3. The target gene and its extracted cisNats are to be stored as a pair in another DataFrame.
    This process is applied for every genes in df0.

    Arguments:
        df0 (DataFrame): contains genes which can be target genes.
        df1 (DataFrame): contains genes which can be a cisNats of target genes.
        filter (str): Criteria for locational extracting, specified in the definition of extract_one_type_cisnats().
    '''
    cols = df0.columns

    dict_pairs ={}
    counter = 0
 
    df1_chr_map = dict(list(df1.groupby('Chr')))

    for i in range(df0.shape[0]):

        # Chromosomal selection
        chr_i = df0.at[i,'Chr']
        s0 = df0.at[i,'Start']
        e0 = df0.at[i,'End']

        if chr_i not in df1_chr_map.keys():
            continue
        
        extrby_chr = df1_chr_map[chr_i]

        # Locational selection
        s1 = extrby_chr.Start
        e1 = extrby_chr.End
        
        extrby_st_ed = extrby_chr[eval(filter)]
        
        # Forming a pair
        if len(extrby_st_ed.index) != 0:

            gene_target = pd.DataFrame(df0.iloc[i]).T.reset_index(drop=True)
            gene_cisnats = extrby_st_ed.reset_index(drop=True).rename(columns=lambda x: '_' + x)

            pairs = pd.concat([gene_target, gene_cisnats], axis =1)
            pairs[cols] = pairs[cols].fillna(method = 'ffill')

            for j in range(pairs.shape[0]):
                dict_pairs[counter] = pairs.iloc[j]
                
                counter += 1

    result = pd.DataFrame.from_dict(dict_pairs, orient='index')
    return result


def extract_one_type_cisnats(cntype, genes_plus, genes_minus):
    '''
    Gives find_cisnats() necessory arguments and run it so that all cisNats pair of intended type can be extracted.
    The arguments "filter" is chosen depending on "cntype".
    find_cisnats() is to be run twice ; plus-to-minus extracting and minus-to-plus extracting.

    Arguments:
        cntype (str): the type of cisNats to extract. "EB" / "FO" / "HH" / "TT" 
        genes_plus (DataFrame): the sets of information about genes on the plus strand.
        genes_minus (DataFrame): the sets of information about genes on the minus strand.
    '''
    
    # Criteria for locational extracting
    FILTER_PLUS_MINUS= {
        "EB":"(s1 >= s0) & (e1 <= e0)",
        "FO":"(s1 <= s0) & (e1 >= e0)",
        "HH":"(s1 < s0) & (e1 >= s0) & (e1 <= e0)",
        "TT":"(s1 >= s0) & (s1 <= e0) & (e1 > e0)",
        }
    
    FILTER_MINUS_PLUS= {
        "EB":"(s1 >= s0) & (e1 <= e0)",
        "FO":"(s1 <= s0) & (e1 >= e0)",
        "HH":"(s1 >= s0) & (s1 <= e0) & (e1 > e0)",
        "TT":"(s1 < s0) & (e1 >= s0) & (e1 <= e0)",
        }

    print(cntype)

    # Plus-to-minus extracting
    print('Plus-to-minus extracting')
    cnpairs1 = find_cisnats(
        df0 = genes_plus,
        df1 = genes_minus,
        filter = FILTER_PLUS_MINUS[cntype]
        )

    # Minus-to-plus extracting
    print('Minus-to-plus extracting')
    cnpairs2 = find_cisnats(
        df0 = genes_minus,
        df1 = genes_plus,
        filter = FILTER_MINUS_PLUS[cntype]
        )

    cnpairs_combined = pd.concat([cnpairs1,cnpairs2], axis=0)
    cnpairs_combined['Type'] = cntype

    return cnpairs_combined


def write_summary(df, total):
    '''
    Counts genes which have any cisNats and culculates their ratio to All genes.
    Assembles the culcuration results as a summary.

    Arguments:
        df (DataFrame): Assembly of extracted cisNats pair.
        total (int): The total number of all genes.
    '''
    result = pd.DataFrame(columns = ['count','rate'])

    result.at['Total genes','count'] = total

    count_all = df['id'].nunique()
    rate_all = '{:.2%}'.format(count_all/total)

    result.at['genes with cis-Nats','count'] = count_all
    result.at['genes with cis-Nats','rate'] = rate_all

    cntype_list = ['EB','FO','HH','TT']
    cntype_map = dict(list(df.groupby('Type')))
    
    for cntype in cntype_list:

        if cntype not in cntype_map.keys():
            result.at[cntype,'count'] = 0
            result.at[cntype,'rate'] = '0.00%'

        else:
            each_type_df = cntype_map[cntype]

            count = each_type_df['id'].nunique()
            rate = '{:.2%}'.format(count/total)

            result.at[cntype,'count'] = count
            result.at[cntype,'rate'] = rate

    return result


def print_summary(df):

    str_summary = (
        '< Result >' + '\n'
        'total genes : ' + str(df.iat[0,0]) + '\n'
        'genes with cisNats : ' + str(df.iat[1,0]) + ' [' + str(df.iat[1,1]) + ']' + '\n'
        '     EB : ' + str(df.iat[2,0]) + ' [' + str(df.iat[2,1]) + ']' + '\n'
        '     FO : ' + str(df.iat[3,0]) + ' [' + str(df.iat[3,1]) + ']' + '\n'
        '     HH : ' + str(df.iat[4,0]) + ' [' + str(df.iat[4,1]) + ']' + '\n'
        '     TT : ' + str(df.iat[5,0]) + ' [' + str(df.iat[5,1]) + ']'
        )
    print(str_summary)


def main():

    paths = get_path()

    print('Reading ' + paths.input)
    df = pd.read_csv(paths.input, header=0)

    e.item_check(df.columns)

    genes_total = df['id'].nunique()
    
    # Dividing df into two groups, minus (-) or plus (+) strand
    df_plus=df.query('Strand == "+"').reset_index(drop=True)
    df_minus=df.query('Strand == "-"').reset_index(drop=True)

    # Extracting four types of cisNats
    result_eb = extract_one_type_cisnats('EB', df_plus, df_minus)
    result_fo = extract_one_type_cisnats('FO', df_plus, df_minus)
    result_hh = extract_one_type_cisnats('HH', df_plus, df_minus)
    result_tt = extract_one_type_cisnats('TT', df_plus, df_minus)

    table = pd.concat([result_eb,result_fo,result_hh,result_tt], axis=0)

    summary = write_summary(table,genes_total)
    print_summary(summary)

    # Making a new directory and output the results
    os.makedirs(os.path.join(paths.output, 'ccivr_output'), exist_ok=True)
    ccivr_output = os.path.join(paths.output, 'ccivr_output')

    output_table = os.path.join(ccivr_output, 'Table.csv')
    output_summary = os.path.join(ccivr_output, 'Summary.csv')

    print('Writing the table to ' + output_table)
    table.to_csv(output_table, index=False)
    print('Writing the summary to ' + output_summary)
    summary.to_csv(output_summary, index=True)


if __name__ == '__main__':
    main()
