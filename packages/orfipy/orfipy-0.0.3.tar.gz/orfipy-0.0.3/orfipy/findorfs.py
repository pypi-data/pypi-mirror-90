#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 20:01:56 2020

@author: usingh
"""
import os
import sys
import time
import multiprocessing
from contextlib import closing
import gc
#import pyximport; pyximport.install()
import orfipy_core as oc
import subprocess
import orfipy.utils as ut
import pyfastx
from orfipy import _long_seq_bytes
from orfipy import _long_limit


_total_seqs=0 #track total processed seqs
#rev comp
orig = "ACTG"
comp = "TGAC"
transtab = str.maketrans(orig, comp)
def revcomp(seq):
        return seq.translate(transtab)[::-1]


def worker_map(arglist):
    """
    start worker
    """
    #call orf function
    #poolargs contains [thisseq,thisseq_rc,thisname,minlen,maxlen,strand,starts,stops,include_stop, partial3, partial5, outputs,tmpdir]
    res=oc.start_search(*arglist[:-1])
    
    #directly write res to files
    
    #first open file streams to write the results
    #arglist[-2] is the list of output types
    #for all true values in arglist[-2] open a files in tmp dir and write results
    file_streams=()
    
    for x in range(len(arglist[-2])):
        if arglist[-2][x]:
            #open stream in tmpdir
            file_streams+=(open(os.path.join(arglist[-1],arglist[2]+'.orfipytmp_'+str(x)),'w'),)
        else:
            file_streams+=(None,)
    
    #write results to tmp dir
    write_results_single(res,file_streams)
    
    del res
    gc.collect()


def start_map(poolargs,procs):
    """
    Suitable for large sequences with a large number of ORF e.g. genomes
    Low IO overhead

    Parameters
    ----------
    poolargs : list
        Arguments passed to oc.start_search.
    procs : int
        Num procs.

    Returns
    -------
    None.

    """
    pool=multiprocessing.Pool(processes=procs)
    pool.map(worker_map,poolargs)
    pool.close()
    pool.join()


def worker_imap(arglist):
    """
    start worker
    """
    #poolargs contains [thisseq,thisseq_rc,thisname,minlen,maxlen,strand,starts,stops, table, include_stop, partial3, partial5, outputs,tmpdir]
    #call orf function
    #res=oc.start_search(arglist[0],arglist[1],arglist[2],arglist[3],arglist[4],arglist[5],arglist[6],arglist[7])
    #pass all but last argument
    res=oc.start_search(*arglist[:-1])
    return res
    
def start_imap_unordered(poolargs,procs):
    """
    Suitable for smaller sequences with a less number of ORF e.g. transcriptomes

    Parameters
    ----------
    poolargs : list
        Arguments passed to oc.start_search.
    procs : int
        Num procs.

    Returns
    -------
    None.

    """
    with closing( multiprocessing.Pool(procs) ) as p:
        results_inner = p.imap_unordered(worker_imap, poolargs, 100)
   
    #return results
    return results_inner

    

def start_multiprocs(seqs, 
                     minlen, 
                     maxlen, 
                     procs,
                     chunk_size, 
                     strand, 
                     starts,
                     stops, 
                     table,include_stop,
                     partial3,
                     partial5,
                     bw_stops,
                     file_streams,
                     tmpdir):
    """
    

    Parameters
    ----------
    seqs : Fastx object
        A Fastx object.
    minlen : int
        min len of ORFs.
    maxlen : int
        Max len of ORFs.
    procs : int
        Num procs.
    chunk_size : dounle
        Chunk size in MB.
    strand : char
        Strand to use (b)oth, (f)wd or (r)ev.
    starts : list
        List of start codons.
    stops : list
        List of stop codons.
    table : dict
        translation tab.
    include_stop : bool
        Include stop in results.
    partial3 : bool
        report ORF without stop codon.
    partial5 : bool
        report ORF without start codon.
    bw_stops : bool
        Orfs defined as between stops.
    file_streams : list
        List of file streams for outputting the results.
    tmpdir : str
        Out directory.

    Returns
    -------
    None.

    """
    
    #outputs
    outputs=[]
    for f in file_streams:
        if f:
            outputs.append(True)
        else:
            outputs.append(False)
    #process = psutil.Process(os.getpid())
    #poolargs contain data to be passed to mp workers
    poolargs=[]
    #Use a memory limit to roughly limit memory usage to  order of _MEMLIMIT
    #this is helpful in making code run on low mwmory systems and with python 3.8 and lower if data is more than 2GB in size
    _MEMLIMIT=chunk_size*1000000 #convert MB to bytes
    #total bytes read in memory
    total_read_bytes=0
    #all read bytes
    cummulative_read_bytes=0
    long_seqs=False
    process_long=False
    
    #process sequences in fasta file
    #seqs is FastaWrapper object
    #for s in seqs.keys:
    for name, seq, *rest in seqs:
        global _total_seqs
        _total_seqs+=1
        #print(name, seq)
        thisname=name
        thisseq=seq
        #print(type(seq))
        #thisseq=seqs.get_seq(s)
        #ignore if seq is < minlen
        if len(thisseq)<minlen:
            continue
        #add bytes read
        this_read=len(thisseq.encode('utf-8'))
        thisseq_rc=None
        if strand == 'b' or strand =='r':
            #thisseq_rc=seqs.get_seq(s,rc=True)
            thisseq_rc=revcomp(thisseq)
            #add bytes read of rev_com seq
            this_read=this_read*2
        
        #add read bytes to total_read_bytes
        total_read_bytes+=this_read
        cummulative_read_bytes+=this_read
        
        #add to poolargs; if limit is reached this will be reset
        poolargs.append([thisseq,thisseq_rc,thisname,minlen,maxlen,strand,starts,stops, table, include_stop, partial3, partial5, bw_stops, outputs,tmpdir])
        
        """
        If a long sequence is read e.g. chromosome
        """
        if this_read >= _long_seq_bytes: 
            long_seqs=True
            #if more than _long_limit long seqs are read, process them
            if len(poolargs)>=_long_limit:
                process_long=True
        
        """
        if total_read_bytes is more than memory limit, perform search
        or identify if the sequences are very large
        """
        if total_read_bytes+1000000 >= _MEMLIMIT or process_long:
            print('Processing {0:d} bytes'.format(cummulative_read_bytes), end="\r", flush=True,file=sys.stderr)
            #process seqs that were added to poolargs
            
            # find ORFs in currently read data
            """
            if num seq in chunk size are less --> larger seqs; call star_map
            start_map does serial process and is slow so that will limit memory usage for large sequences.
            For smaller seqs (requires less memory) start_imap_unordered does parallel processing and writing to file. it is faster and
            """
            if long_seqs:
                #results are written to temp files by each worker
                start_map(poolargs,procs)
            else:            
                #call imap unorderd for multiple smaller seqs
                results=start_imap_unordered(poolargs, procs)
                #collect and write these results
                write_results_multiple(results,file_streams)
                            
            #perform GC
            #del results_inner
            del poolargs
            gc.collect()
            #create empty list
            poolargs=[]
            #reset total read bytes for next batch
            total_read_bytes=0
            long_seqs=False
            process_long=False
            
        
    #after loop poolargs contains seq; process these 
    if len(poolargs) > 0:
        print('Processing {0:d} bytes'.format(cummulative_read_bytes), end="\r", flush=True,file=sys.stderr)
        if long_seqs:
            #results are written to temp files by each worker
            start_map(poolargs,procs)
        else:            
            results=start_imap_unordered(poolargs, procs)
            #collect and write these results
            write_results_multiple(results,file_streams)
        #perform GC
        del poolargs
        gc.collect()
        #create empty list
        poolargs=[]
        #reset total read bytes for next batch
        total_read_bytes=0
    
    print()
    

def worker_single(seqs,minlen,maxlen,strand,starts,stops,table,include_stop,partial3,partial5,bw_stops,file_streams,tmp):
    """
    Compute ORFs using single thread

    Parameters
    ----------
    seqs : Fastx object
        A Fastx object.
    minlen : int
        min len of ORFs.
    maxlen : int
        Max len of ORFs.
    strand : char
        Strand to use (b)oth, (f)wd or (r)ev.
    starts : list
        List of start codons.
    stops : list
        List of stop codons.
    table : dict
        translation tab.
    include_stop : bool
        Include stop in results.
    partial3 : bool
        report ORF without stop codon.
    partial5 : bool
        report ORF without start codon.
    bw_stops : bool
        Orfs defined as between stops.
    file_streams : list
        List of file streams for outputting the results.
    tmpdir : str
        Out directory.

    Returns
    -------
    None.

    """
   
    ut.print_notification('orfipy single-mode')
    #outputs
    outputs=[]
    for f in file_streams:
        if f:
            outputs.append(True)
        else:
            outputs.append(False)
    #results=[]
    for name, seq, *rest in seqs:
        global _total_seqs
        _total_seqs+=1
        #print(name, seq)
        thisname=name
        thisseq=seq
        #ignore if seq is < minlen
        if len(thisseq)<minlen:
            continue
        thisseq_rc=None
        if strand == 'b' or strand =='r':
            thisseq_rc=revcomp(thisseq)
        
        res=oc.start_search(thisseq,thisseq_rc,thisname,minlen,maxlen,strand,starts,stops,table, include_stop, partial3, partial5, bw_stops,outputs)
        
        write_results_single(res, file_streams)


def write_results_single(results,file_streams):
    """
    Write result to file_stream

    Parameters
    ----------
    results : list
        List containing results in different formats.
    file_streams : List
        A list of file objects to write results.

    Returns
    -------
    None.

    """
    #results is a list on n lists. each n lists contain a string; file_streams contain n streams to write n lists
    
    all_none=True
    for i in range(len(file_streams)):
        if file_streams[i]:
            if results[i]:
                file_streams[i].write(results[i]+'\n')
            all_none=False
    #no output file specified, print bed results
    if all_none and results[0]:
        print(results[0])

def write_results_multiple(results,file_streams):
    """
    write results from multiple seqs

    Parameters
    ----------
    results : list containing list of results
        DESCRIPTION.
    file_streams : list
        A list of file objects to write results.

    Returns
    -------
    None.

    """
    #results is a generator; each item in result is a list of n lists.
    #file_streams contain n file_streams for each list in a result item
    #print(results)
    for reslist in results:
        write_results_single(reslist, file_streams)
    return
    
    
def init_result_files(fileslist,tmp=""):
    """
    Open files and return objects to use later

    Parameters
    ----------
    fileslist : TYPE
        DESCRIPTION.
    tmp : TYPE, optional
        DESCRIPTION. The default is "".

    Returns
    -------
    fstreams : list
        List of file objects.

    """
    #create outdir
    create_outdir(fileslist,tmp)
    #create empty files to append later
    fstreams=()
    for f in fileslist:
        if f:
            fstreams=fstreams+(open(os.path.join(tmp, f),'w'),)
        else:
            fstreams=fstreams+(None,)
    return fstreams


def create_outdir(outlist,outdir):
    """
    crete out dir

    Parameters
    ----------
    outlist : TYPE
        DESCRIPTION.
    outdir : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    for f in outlist:
        if f:
            if not os.path.exists(outdir):
                os.makedirs(outdir)
            return

def close_result_files(fstreams):
    """
    Close all the files after writing results

    Parameters
    ----------
    fstreams : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    for f in fstreams:
        if f:
            f.close()
    
def concat_resultfiles(fstreams,outdir):
    """
    Merge any temporary files, if created. uses subprocess and shell
    """
    #os.chdir(outdir)    
    for f in fstreams:
        if f:
            thisfilename=f.name
            x=fstreams.index(f)
            
            cmd='cat '+outdir+'/*.orfipytmp_'+str(x)+' >> '+thisfilename
            proc = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            out,err = proc.communicate()
            
            cmd='rm '+outdir+'/*.orfipytmp_'+str(x)
            proc = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            out,err = proc.communicate()


def filter_bed_longest(bedfile):
    """
    Extract longest ORF per seq

    Parameters
    ----------
    bedfile : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    res={}
    with open(bedfile) as f:
        for ind, l in enumerate(f):
            temp=l.split('\t')
            thisname=temp[0]
            thislen=int(temp[3].split(';')[2].split('=')[-1])
            if thisname in res:
                prevlen=res[thisname][0]
                if thislen > prevlen:
                    res[thisname]=[thislen,l]
            else:
                res[thisname]=[thislen,l]
    
    #write to file
    outfile=os.path.splitext(bedfile)[0]+"_longest"+os.path.splitext(bedfile)[1]
    f=open(outfile,'w')
    for k in res.keys():
        f.write(res[k][1])
    f.close()

def group_bed_frame(bedfile):
    """
    Group ORF by frames

    Parameters
    ----------
    bedfile : in bed file
        DESCRIPTION.

    Returns
    -------
    streams : TYPE
        DESCRIPTION.

    """
    basename=os.path.splitext(bedfile)[0]
    ext=os.path.splitext(bedfile)[1]
    fp1=open(basename+"_+1"+ext,'w')
    fp2=open(basename+"_+2"+ext,'w')
    fp3=open(basename+"_+3"+ext,'w')
    fp4=open(basename+"_-1"+ext,'w')
    fp5=open(basename+"_-2"+ext,'w')
    fp6=open(basename+"_-3"+ext,'w')
    streams={"1":fp1,"2":fp2,"3":fp3,"-1":fp4,"-2":fp5,"-3":fp6}
    with open(bedfile) as f:
        for ind, l in enumerate(f):
            thisframe=l.split('\t')[3].split(';')[3].split('=')[-1]
            streams[thisframe].write(l)
    for k in streams.keys():
        streams[k].close()
    return streams
        
    
    
def group_by_frame_length(bed,bed12,longest,byframe):
    """
    Gruoup file by longest length and frame

    Parameters
    ----------
    bed : str
        path to bed file.
    bed12 : str
        path to bed12.
    longest : bool
        report longest ORF per seq.
    byframe : bool
        report ORFs by frame.

    Returns
    -------
    None.

    """
    if longest:
        filter_bed_longest(bed)
    if byframe:
        files_frame=group_bed_frame(bed)
        if longest:
            for k in files_frame.keys():
                filter_bed_longest(files_frame[k].name)
            

    

    
##########main################
def main(infasta,
         minlen,
         maxlen,
         procs,
         single_mode,
         chunk_size,
         strand,
         starts,
         stops,
         table,
         include_stop,
         partial3,
         partial5,
         bw_stops,
         longest,
         byframe,
         bed12,
         bed,
         dna,
         rna,
         pep,
         outdir,
         logr):
    """
    

    Parameters
    ----------
    infasta : str
        The input file.
    minlen : int
        Min len of ORFs
    maxlen : int
        Max len of ORFs
    procs : int
        Threads to use
    single_mode : bool
        Use single thread
    chunk_size : float
        Chunk size in MB
    strand : char
        Strand to fint ORF. b--> both f--> fwd r --> reverse
    starts : List
        Start codons to search ORF
    stops : List
        Stop codons to search ORF
    table : dict
        Transclation table.
    include_stop : bool
        Include stop codon in ORF coordinate and sequence.
    partial3 : bool
        Report ORFs without stop codon.
    partial5 : bool
        Report ORFs without start codon.
    bw_stops : bool
        Find ORFs defined by between start and Stop.
    longest : bool
        Report longest ORFs in each sequence.
    byframe : bool
        Report ORFs by frames.
    bed12 : bool
        Output ORFs to bed12.
    bed : bool
        Output ORFs to bed.
    dna : bool
        Output ORFs as nucleotide .fasta.
    rna : bool
        Output ORFs as rna .fasta.
    pep : bool
        Output ORFs as peptide .fasta..
    outdir : str
        Output directory.
    logr : logger
        logging object to log mesages.

    Returns
    -------
    None.

    """
    
    
    ##start time
    start = time.time()
    
    file_streams=init_result_files((bed12, bed, dna, rna, pep),tmp=outdir)    
    
    
    #read fasta/fastq file  
    seqs=pyfastx.Fastx(infasta)
    
    if single_mode:
        
        worker_single(seqs,
                      minlen,
                      maxlen,
                      strand,
                      starts,
                      stops,
                      table,
                      include_stop,
                      partial3,
                      partial5,
                      bw_stops,
                      file_streams,
                      outdir)
        duration = time.time() - start
    else:
        start_multiprocs(seqs, 
                         minlen,
                         maxlen,
                         procs,
                         chunk_size,
                         strand,
                         starts,
                         stops,
                         table, 
                         include_stop,
                         partial3,
                         partial5,
                         bw_stops,
                         file_streams,
                         outdir)
        duration = time.time() - start
             
               
    
    close_result_files(file_streams)
    #print("Concat...",file=sys.stderr)
    concat_resultfiles(file_streams,outdir)
    
    #after writing all files, write additional file for longest and bystrand
    if longest or byframe:
        bedfile=os.path.join(outdir,bed)
        bed12file=''
        if bed12:
           bed12file=os.path.join(outdir,bed12)
        group_by_frame_length(bedfile,bed12file,longest,byframe)
        
    #print("Processed {0:d} sequences in {1:.2f} seconds".format(len(seqs.keys),duration),file=sys.stderr)
    ut.print_success("Processed {0:d} sequences in {1:.2f} seconds".format(_total_seqs,duration))
    logr.info("Processed {0:d} sequences in {1:.2f} seconds".format(_total_seqs,duration))
    logr.info("END")


if __name__ == '__main__':
    main()
