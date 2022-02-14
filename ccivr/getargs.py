import argparse
import os

def get_path():
    
    parser = argparse.ArgumentParser(
        description='Extracts cisNats from data of gene sets.'
        )

    parser.add_argument('input',
        help='the path of the CSV file to read'
        )

    parser.add_argument('-o', '--output',
        help=
            'the path of the directory to save results, '
            'if not specified, files would be stored in the same location as input file.'
        )

    args = parser.parse_args()

    input_file = os.path.abspath(args.input)
    
    if args.output:
        output_dir = os.path.abspath(args.output)
    else:
        output_dir = os.path.dirname(input_file)

    os.makedirs(os.path.join(output_dir, 'ccivr_output'), exist_ok=True)

    output_file_table = os.path.join(output_dir, 'ccivr_output', 'Table.csv')
    output_file_summary = os.path.join(output_dir, 'ccivr_output', 'Summary.csv')

    class Paths:
        def __init__(self,input,output:list):
            self.input = input
            self.output = output

    paths = Paths(
        input = input_file, 
        output = [output_file_table, output_file_summary]
        )

    return paths