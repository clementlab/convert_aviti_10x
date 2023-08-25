import argparse
import logging
import multiprocessing
import os
import subprocess

def prep_10x_from_aviti(input_r1_file, input_r2_file, sample_name, num_processes=None):
    """
    Prepares 10x data from Aviti for downstream processing
    :param input_r1_file: input read 1 file
    :param input_r2_file: input read 2 file
    :param sample_name: sample name
    :param num_processes: number of processes to use
    """
    
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    output_file_r1 = sample_name + "_S1_L001_R1_001.fastq.gz"
    output_file_r2 = sample_name + "_S1_L001_R2_001.fastq.gz"

    if num_processes is None:
        num_processes = multiprocessing.cpu_count()
    num_processes_unzip = max(1,int(num_processes*.25))
    num_processes_zip = max(1,int(num_processes - num_processes_unzip))

    logging.info('Converting R1 file ' + input_r1_file + ' to ' + output_file_r1 + ' using ' + str(num_processes_unzip) + ' unzip processes and ' + str(num_processes_zip) + ' zip processes')
    subprocess.call("pigz -p " + str(num_processes_unzip) + " -dc " + input_r1_file + " | sed '1~4s/,.* / /' | pigz -p " + str(num_processes_zip) + " > " + output_file_r1, shell=True)
    logging.info('Finished. Wrote ' + output_file_r1)

    logging.info('Converting R2 file ' + input_r2_file + ' to ' + output_file_r2 + ' using ' + str(num_processes_unzip) + ' unzip processes and ' + str(num_processes_zip) + ' zip processes')
    subprocess.call("pigz -p " + str(num_processes_unzip) + " -dc " + input_r2_file + " | sed '1~4s/,.* / /' | pigz -p " + str(num_processes_zip) + " > " + output_file_r2, shell=True)
    logging.info('Finished. Wrote ' + output_file_r2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prepares 10x data from Aviti for downstream processing")
    parser.add_argument("-r1", "--input_r1", help="input read 1 file", type=str, required=True)
    parser.add_argument("-r2", "--input_r2", help="input read 2 file", type=str, required=True)
    parser.add_argument("--sample_name", help="sample name", type=str, required=True)
    parser.add_argument("--max_processes", help="maximum processes to run on", type=int, default=None)

    args = parser.parse_args()

    # check for pigz program
    if not subprocess.call("which pigz", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0:
        raise Exception("Cannot find pigz program. Please install pigz (https://zlib.net/pigz/)")

    # check for sed program
    if not subprocess.call("which sed", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0:
        raise Exception("Cannot find sed program. Please install sed (https://www.gnu.org/software/sed/)")

    # check for input files
    if not os.path.exists(args.input_r1):
        raise Exception("Input R1 file " + str(args.input_r1) + " does not exist")

    if not os.path.exists(args.input_r2):
        raise Exception("Input R2 file " + str(args.input_r2) + " does not exist")

    if " " in args.sample_name:
        raise Exception("Sample_name (" + str(args.sample_name) + ") cannot contain spaces")

    prep_10x_from_aviti(args.input_r1, args.input_r2, args.sample_name, args.max_processes)

