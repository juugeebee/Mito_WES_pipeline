#!/bin/bash

source ~/miniconda3/etc/profile.d/conda.sh
conda activate gatk_env

RUN_FOLDER=$PWD

echo ""
echo "bam_to_fastq_mito.sh start"
echo ""

for bam_name in *.dedup.bam; \

do SAMPLE=${bam_name%%.dedup.bam}; \

gatk SamToFastq -I $bam_name -F $SAMPLE.R1.fastq.gz -F2 $SAMPLE.R2.fastq.gz;

done

echo "Creation d'un repertoire <nom du run>_fastq et deplacement des fastq"
mkdir $RUN_FOLDER'_fastq'
mv *.fastq.gz $RUN_FOLDER'_fastq'

echo ""
echo "bam_to_fastq_mito.sh job done!"
echo ""
