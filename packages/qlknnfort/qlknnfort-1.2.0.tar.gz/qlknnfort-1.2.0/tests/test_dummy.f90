! This file is part of QLKNN-fortran
! You should have received the QLKNN-fortran LICENSE in the root of the project
! Dummy test implementation
! Do not forget to add Makefile rules to fruit.make!
module test_dummy
#include "../src/core/preprocessor.inc"
  use fruit
  use fruit_util
#ifdef MPI
  use mpi
#endif
  implicit none
contains
  subroutine test_stuff
    use qlknn_types
    !use qlknn_random_modules
    implicit none
    integer :: weird_dummy_int
    integer :: verbosity
    integer(lli) :: dummy_int

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
    verbosity = 1
    if (verbosity >= 1) then
      write(*, *) 'I am test dummy and my world rank is', my_world_rank
    endif

    weird_dummy_int = 1
    dummy_int = 1
    if (my_world_rank == 0) then
      call assert_equals(INT(dummy_int), INT(weird_dummy_int),'Casted integer gives different value!')
    endif

  end subroutine test_stuff
end module test_dummy
