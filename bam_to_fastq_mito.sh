#!/bin/bash

# Author: Julie BOGOIN

source ~/miniconda3/etc/profile.d/conda.sh
conda activate fastq_bam_env

RUN_FOLDER=$PWD

echo ""
echo "bam_to_fastq_mito.sh start"
echo ""

for bam_name in *.dedup.bam; \

do SAMPLE=${bam_name%%.dedup.bam}; \

    samtools bam2fq $bam_name -@12 > $SAMPLE.fastq; 

    # split a single .fastq file of paired-end reads into two separated files
    # extracting reads ending with '/1' or '/2'
    cat $SAMPLE.fastq | grep '^@.*/1$' -A 3 --no-group-separator > ${SAMPLE}.R1.fastq;
    gzip ${SAMPLE}.R1.fastq;
    
    cat $SAMPLE.fastq | grep '^@.*/2$' -A 3 --no-group-separator > ${SAMPLE}.R2.fastq;
    gzip  ${SAMPLE}.R2.fastq;

    rm $SAMPLE.fastq;

done

echo "Creation d'un repertoire <nom du run>_fastq et deplacement des fastq"
mkdir $RUN_FOLDER'_fastq'
mv *.fastq.gz $RUN_FOLDER'_fastq'

echo ""
echo "bam_to_fastq_mito.sh job done!"
echo ""
