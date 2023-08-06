! This file is part of QLKNN-fortran
! You should have received the QLKNN-fortran LICENSE in the root of the project
module teardown_mpi
  use qlknn_types
#ifdef MPI
  use mpi
#endif
contains
  subroutine teardown
#if defined(LLI) && defined(__INTEL_COMPILER)
    integer(lli) my_world_rank
#else
    integer(li) my_world_rank
#endif
#ifdef MPI
#if defined(LLI) && defined(__INTEL_COMPILER)
    integer(lli) mpi_ierr, world_size
#else
    integer(li) mpi_ierr, world_size
#endif
#endif

#ifdef MPI
    call MPI_COMM_RANK(MPI_COMM_WORLD, my_world_rank, mpi_ierr)
#else
    my_world_rank = 0
#endif
    write(*, '(A, I3)') 'Byebye from rank ', int(my_world_rank, li)

#ifdef MPI
    call MPI_FINALIZE(mpi_ierr)
#endif

  end subroutine teardown
end module teardown_mpi
