############################################################################
Working files for 2015 edition of the Berkeley Practical Neuroimaging course
############################################################################

See http://practical-neuroimaging.github.com

This repository has files for the exercises during the class.

See the ``LICENSE`` file in each directory for copyright and licensing.

*************************************************
Making exercise notebooks from solution notebooks
*************************************************

We usually write the exercise notebooks as solutions first, and then use an
automated tool to strip out the solutions and generate the exercise notebook.

This involves some kludgy markup to the code comments starting each code cell.

See:

* ``day12/smoothing_solutions.ipynb``
* ``day12/smoothing.ipynb``

for an example. I generated ``day12/smoothing.ipynb`` automatically from
``day12/smoothing_solutions.ipynb`` with::

    cd day12
    ../tools/unsolve_nb.py smoothing_solutions.ipynb smoothing.ipynb

``unsolve_nb.py`` always leaves comments at the top of a code call, and will
also remove any code from a code cell unless the first comment in the cell
starts with ``# -``.  So, ``unsolve_nb.py`` will leave the top comments but
remove all the code in a cell like this::

    # fwhm2sigma
    # Maybe some some comments here
    def fwhm2sigma(fwhm):
        return fwhm / np.sqrt(8 * np.log(2))

It will leave all the cell (code and comments) in a cell like this::

    # - get middle line from middle slice
    mid_line = mid_slice[:, 25]
    plt.plot(mid_line)

So, the procedure for writing an exercise notebook is usually:

* write ``some_exercises_solutions.ipynb``, putting ``# -`` comments for cells
  where you want the students to have the comments and code, and ``# ``
  comments at the top of other cells to give students a clue how to do the
  exercise;
* when done, save ``some_exercises_solutions.ipynb`` and run
  ``../tools/unsolve_nb.py some_exercises_solutions.ipynb
  some_exercises.ipynb``;
* read through ``some_exercises.ipynb`` to check the result is what you
  expect;
* commit both ``some_exercises_solutions.ipynb`` and ``some_exercises.ipynb``
  to the repository;
* make all edits to ``some_exercises_solutions.ipynb`` and regenerate
  ``some_exercises.ipynb`` for your edits.
