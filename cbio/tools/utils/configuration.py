"""
Docstring
"""

import os
import cbio


def get_init_paths():
    """
    Docstring
    """

    ngs_software_bin = os.getenv('BIN_BIOTOOLS')
    refgenomes = os.getenv('REFGENOMES')
    output_dir = os.getenv('OUTPUT_DIR')
    plasmid_ref = os.getenv('PLASMID_REF')

    init_conf = {
        'BIN_BIOTOOLS': ngs_software_bin,
        'REFGENOMES': refgenomes,
        'OUTPUT_DIR': output_dir,
        'PLASMID_REF': plasmid_ref,
        }

    if any(a is None for a in [ngs_software_bin, refgenomes, output_dir, plasmid_ref]):
        print('#[ERR]: One of the variables is not well set')
        for key in init_conf:
            print(key + ' -> "' + str(init_conf[key]) + '"')
        exit(1)

    return init_conf


def get_config():
    """
    Docstring
    """

    init_conf = get_init_paths()

    ngs_software_bin = init_conf['BIN_BIOTOOLS']
    plasmid_ref = init_conf['PLASMID_REF']
    output_dir = init_conf['OUTPUT_DIR']

    config = {}

    config['ref'] = {
        # Ref Genomes
        "GRCh38": os.path.join(init_conf['REFGENOMES'], 'hs38', 'hs38.fa'),
        "GRCh37": os.path.join(init_conf['REFGENOMES'], 'hs37d5', 'hs37d5.fa')
        }

    config['software'] = {}
    config['software']['paths'] = {
        "TRIMMOMATICPATH": os.path.join(ngs_software_bin, "trimmomatic.jar"),
        "BWAPATH": os.path.join(ngs_software_bin, 'bwa'),
        "SAMTOOLSPATH": os.path.join(ngs_software_bin, 'samtools'),
        "FREEBAYESPATH": os.path.join(ngs_software_bin, 'freebayes'),
        "FASTQCPATH": os.path.join(ngs_software_bin, 'fastqc'),
        "PICARDPATH": os.path.join(ngs_software_bin, 'picard.jar'),
        "ANNOVARPATH": os.path.join(ngs_software_bin, 'table_annovar.pl'),
        "BEDTOOLSPATH": os.path.join(ngs_software_bin, 'bedtools'),
        "SNPEFFPATH": os.path.join(ngs_software_bin, 'snpEff.jar'),
        "SNPSIFTPATH": os.path.join(ngs_software_bin, 'SnpSift.jar'),
        "TABIXPATH": os.path.join(ngs_software_bin, 'tabix'),
        "BGZIPPATH": os.path.join(ngs_software_bin, 'bgzip'),
        "ABRA": os.path.join(ngs_software_bin, 'abra-0.97.jar'),
        "CUTADAPT": os.path.join(ngs_software_bin, 'cutadapt'),
    }
    config['software']['data'] = {
        "PLASMID_REF": os.path.join(plasmid_ref, 'plasm_seq.fa'),
        "PLASMID_IDX": os.path.join(plasmid_ref, 'indexes.tsv'),
        "PLASMID_BED": os.path.join(plasmid_ref, 'regions.bed'),
        "TRIMMOMATIC_NEXTERA": os.path.join(ngs_software_bin, 'NexteraPE-PE.fa'),
    }

    config['dbs'] = {
        "ANNOVARINFO": os.path.join(ngs_software_bin, 'annov_humandb'),
        "IMEGENDB": os.path.join(ngs_software_bin, 'test.db')
    }

    config['outdir'] = output_dir

    # Check if sofware in config and references exist
    check_config_paths(config)

    config['software']['versions'] = get_version_of_software(ngs_software_bin)

    return config


def get_version_of_software(ngs_software_bin):

    output = cbio.utils.run_cmd('ls -l ' + ngs_software_bin, 1)
    software_versions = {}

    for line in output:
        if line == '':
            continue
        if line.startswith('total'):
            continue
        line = line.split()
        software_versions[line[8]] = ' '.join(line[5:])

    return(software_versions)



def check_config_paths(config):
    """
    Docstring
    """
    for software in config['software']['paths']:
        path = config['software']['paths'][software]
        if isinstance(path, str) and not os.path.lexists(path):
            print("Software " + software + " does not exists -> " + path)
            print("Exiting...")
            exit(1)

    for reference in config['ref']:
        path = config['ref'][reference]
        if isinstance(path, str) and not os.path.exists(path):
            print("#[WARN]: Reference " + reference + " does not exists -> " + path)

    for db in config['dbs']:
        path = config['dbs'][db]
        if isinstance(path, str) and not os.path.exists(path) and db != 'IMEGENDB':
            print("Database " + db + " does not exists -> " + path)
            print("Exiting...")
            exit(1)

    for data in config['software']['data']:
        path = config['software']['data'][data]
        if isinstance(path, str) and not os.path.exists(path):
            print("Data " + data + " does not exists -> " + path)
            print("Exiting...")
            exit(1)