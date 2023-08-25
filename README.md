# CONVERT_AVITI_10x

This script converts aviti files into a format that can be uploaded for 10x processing.

To run this script, first download it to your current directory using `wget`:

```
wget https://github.com/clementlab/convert_aviti_10x/raw/main/convert_aviti_10x.py
```

Next, run the script providing:
- -r1: input read 1 file
- -r2: input read 2 file
- --sample_name: sample name for output files
- --max_processes: (optionally) to control the number of processes used by the script. If this parameter is not set, all processes will be used.

For example:

```
python convert_aviti_10x.py -r1 test1.fq.gz -r2 test2.fq.gz --sample_name test
```

This command will produce the files "test_S1_L001_R1_001.fastq.gz" and "test_S1_L001_R2_001.fastq.gz".
