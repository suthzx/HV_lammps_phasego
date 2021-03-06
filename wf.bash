#!/bin/bash
#SBATCH -J lammps
#SBATCH -p cpu
#SBATCH -N 1
#SBATCH --ntasks-per-node=1
#SBATCH -o out
#SBATCH -e err

#ENV
module purge
module load compiler/intel/2017.5.239
# module load mpi/hpcx/2.4.1/intel-2017.5.239
module load apps/lammps/7Aug19/hpcx-2.4.1-intel2017

# run with user-intel package to accelerat
python lammps_workflow-part2.py
