set term svg enhanced
set logscale x
set xlabel "dt [s]"
set output "plot_timestep_RH.svg" 
set ylabel "RH_{max}"
plot "-" notitle
0.0010000000475 0.292470633984
0.00150000001304 0.284597814083
0.00200000009499 0.292899519205
0.00300000002608 0.314424484968
0.00400000018999 0.314759463072
0.00800000037998 0.31472954154
0.00999999977648 0.314807504416
0.019999999553 0.31526184082
0.0399999991059 0.315033644438
0.0799999982119 0.313343286514
0.10000000149 0.312413483858
0.20000000298 0.307238638401
0.40000000596 0.296731889248
0.800000011921 0.276054084301
1.0 0.267019957304

e
set output "plot_timestep_N.svg"
set ylabel "koncentracja koncowa [1/mg]"
plot "-" notitle
0.0010000000475 653.534118652
0.00150000001304 642.04888916
0.00200000009499 649.803344727
0.00300000002608 664.50189209
0.00400000018999 664.50189209
0.00800000037998 668.089355469
0.00999999977648 668.089355469
0.019999999553 668.089355469
0.0399999991059 675.156921387
0.0799999982119 675.156921387
0.10000000149 675.156921387
0.20000000298 678.634338379
0.40000000596 692.247680664
0.800000011921 695.56628418
1.0 695.56628418

e