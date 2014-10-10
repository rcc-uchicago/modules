# Module tagging and categorization

Simon had put in some work in categorizing available modules.  He created 
an inverted index of modules, grouped into various categories

    astrophysics: salt2,gadget,pluto,ramses,snana,cosmomc,fits,art,emcee
    climate: ccsm,cdo,eigenstraat,gcm
    ...

However, in our email exchanges thus far, we've been contemplating using a more
constrained list of categories (`bio, chem, dev, eng, geo, hpc, nlp, lib, num, phys, stat, util, viz`) for the proposed module yaml files, supplemented with a an open-ended list of tags:

    name: fftw3
    desc: "A C library for computing the discrete Fourier transform."
    module: fftw3/3.3+intel-12.1
    version: 3.3.3
    license: opensource
    category: [num, hpc]      # constrained list of relevant categories
    tags: [library, fft]      # open-ended list of relevant tags
    ...

So I thought I'd try supplementing Simon's inverted index with these
categories:

    phys|astrophysics: salt2,gadget,pluto,ramses,snana,cosmomc,fits,art,emcee

In other words, the format is now ...

    CATEGORIES|TAGS: MODULES

... where the categories and tags can be comma-separated lists:

    num,lib|python,numeric,library: matplotlib,scipy,numpy,healpy,theano

The little `parse.py` script just dumps out yaml entries for each module based
on this index:

    name: 
    desc:
    module: theano
    version:
    license:
    category: ['num', 'lib']
    tags: ['python', 'numeric', 'library']
    ...

