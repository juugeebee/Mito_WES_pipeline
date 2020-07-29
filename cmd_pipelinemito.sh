#!/bin/bash

# Author: Julie BOGOIN

source ~/miniconda3/etc/profile.d/conda.sh
conda activate pipmitoDijon_env

data=$PWD
ref='/media/Data1/jbogoin/ref/fa_hg38/hg38_GenDev'

echo ""
echo "PIPELINE MITO start"
echo ""

rm -Rf pipelinemito_output/

if ls *.fastq.gz;

then
    
    # echo "noms des fastq:" 
    # echo "conversion des majuscules en minuscules + format .R1/R2.fastq.gz:"
    
    # for file in *.fastq.gz;
    # do
    #     new=`echo $file |tr '[:upper:]' '[:lower:]'`;
    #     newbee=`echo $new | sed -e "s/_r/.R/g"`;
    #     newbeebee=` echo $newbee | sed -e "s/_001//g"`;
    #     echo "transformation $file => $newbeebee";
    #     mv -i "$file" "$newbeebee"
    # done

    cd ~/pipelinemito;
    echo ""
    
    sudo docker load -i pipelinemitov1.tar;
    
    echo ""
    echo "Run en cours d'analyse:"
    echo "$data"
    echo ""

    sudo docker run -v $data:/data:rw -v $ref:/mitopipeline:ro\
    --env THREAD=6\
    --env REFNAME=hg38_GenDev.fa pipelinemitov1;

    echo "Deplacement des fastq vers le répertoire racine";
    cd $data

    fastq=`ls -R -1 | grep -E "fastq.gz"` 

    for seq in $fastq;
    do
        sudo mv `find . -name $seq` .; 
    done

    mkdir $data/pipelinemito_output

    echo "Deplacement des fichiers de resultats vers /pipelinemito_output";
    mv *.tsv pipelinemito_output
    mv *.failed pipelinemito_output
    mv *.log pipelinemito_output    
    mv sample.list.txt pipelinemito_output

    conda deactivate
    conda activate results_cnv

    python ~/Mito_WES_pipeline/results_mito.py

    conda deactivate

    echo "";
    echo "PIPELINE MITO job done!";
    echo "";

else

    echo "Il n'y a pas de fastq dans ce répertoire!"
    echo ""
    echo "PIPELINE MITO job not done!"
    echo ""

fi


