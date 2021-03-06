.. index::
    single: fftw3

.. _mdoc_fftw3:

------
fftw3_
------

name: fftw3

desc: A C library for computing the discrete Fourier transform.

module: fftw3/3.3+intel-12.1

version: 3.3.3

license: opensource

category: num,hpc

tags: library,fft

url: http://www.fftw.org

docs: http://www.fftw.org/fftw3_doc/

configuration: OpenMP, SSE, SSE2, AVX. Single, double, and long double precision.

usage: The FFTW3 library and include directories are automatically added to your compiler's search paths; you should be able to compile without specifying  the path manually.

Example:

.. code-block:: c

  #include <stdlib.h>
  #include <stdio.h>
  #include <fftw3.h>

  #define FFT_SIZE    1024

  int main( int argc, char *argv[] ) {
    fftw_plan p;
    fftw_complex in[FFT_SIZE], out[FFT_SIZE];

    /* create fftw plan, compute fft, and destroy plan */
    p = fftw_plan_dft_1d( fft_size, in, out, FFTW_FORWARD, FFTW_ESTIMATE );
    fftw_execute(p);
    fftw_destroy_plan(p);

    return 0;
  }

.. code-block:: bash
  
  module load fftw3/3.3
  icc source.c -lfftw3 -lm


In cases where a program's configuration requires you to specify the path, the environment variable `FFTW3_DIR` can be used.

.. code-block:: bash

  module load fftw3/3.3
  ./configure --with-fftw=$FFW3_DIR




.. _fftw3: http://www.fftw.org
