! This file is part of QLKNN-fortran
! You should have received the QLKNN-fortran LICENSE in the root of the project
module setup_mpi
  use qlknn_types
#ifdef MPI
  use mpi
#endif
contains
  subroutine setup
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
      call MPI_INIT(mpi_ierr)
      call MPI_COMM_SIZE(MPI_COMM_WORLD, world_size, mpi_ierr)
      call MPI_COMM_RANK(MPI_COMM_WORLD, my_world_rank, mpi_ierr)
      if (int(my_world_rank, li) == 0_li) then
        print *, 'World size is         ', int(world_size, li)
      end if
      write(*, '(A, I3)') 'Hello world from rank ', int(my_world_rank, li)
#else
      my_world_rank = 0
#endif
    end subroutine setup
  end module setup_mpi
