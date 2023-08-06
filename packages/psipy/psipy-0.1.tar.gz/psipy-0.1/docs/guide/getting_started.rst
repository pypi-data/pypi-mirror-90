Getting started
===============

psipy is a package for loading and visualising the output of PSI's MAS model
runs. This page provides some narrative documentation that should get you up
and running with obtaining, loading, and visualising some model results.

Getting data
------------
The PSI `MHDWeb pages`_ give access to MAS model runs. The runs are indexed by
Carrington rotation, and for each Carrington rotation there are generally a
number of different runs, varying in the type model run and/or
the boundary conditions.

To load data with psipy you need to manually download the files you are
interested in to a directory on your computer.

.. _MHDWeb pages: http://www.predsci.com/mhdweb/data_access.php

Loading data
------------
psipy stores the output variables from a single MAS run in the
`MASOutput` object. To create one of these, specify the directory
which has all of the outputs ``.hdf`` files you want to load:

.. code-block:: python

    from psipy.model import MASOutput

    directory = '/path/to/files'
    mas_output = MASOutput(directory)

To see which variables have been loaded, we can look at the ``.variables``
attribute:

.. code-block:: python

    print(mas_output.variables)

This will print a list of the variables that have been loaded. Each individual
variable can then be accessed with square brackets, for example to get the
radial magnetic field component:

.. code-block:: python

    br = mas_output['br']

This will return a `Variable` object, which stores the underlying data as a
`xarray.DataArray` under the `Variable.data` property.

Data coordinates
----------------
The data stored in `Variable.data` contains the values of the data as a normal
array, and in addition stores the coordinates of each data point.

MAS model outputs are defined on a 3D grid of points on a spherical grid. The
coordinate names are ``'r', 'theta', 'phi'``. The coordinate values along each
dimension can be accessed using the ``r_coords, theta_coords, phi_coords``
properties, e.g.:

.. code-block:: python

  rvals = br.r_coords

Plotting data
-------------
`Variable` objects have methods to plot 2D slices of the data. These
methods are:

- `Variable.plot_phi_cut`
- `Variable.plot_equatorial_cut`
- `Variable.plot_radial_cut`

A typical use looks like this:

.. code-block:: python

  ax = plt.subplot(1, 1, 1, projection='polar')
  model['rho'].plot_phi_cut(index, ax=ax, ...)

and produces an output like this:

.. image:: /auto_examples/visualisation/images/sphx_glr_plot_visualising_mas_002.png
   :width: 600

For more examples of how to use these methods, see the
:ref:`sphx_glr_auto_examples` gallery.

There are also methods that can be used to plot contours of the data on top
of these 2D slices. As an example, this can be helpful for plotting the
heliospheric current sheet, by contouring :math:`B_{r} = 0`. These methods are

- `Variable.contour_phi_cut`
- `Variable.contour_equatorial_cut`
- `Variable.contour_radial_cut`

A typical use looks like this:

.. code-block:: python

  ax = plt.subplot(1, 1, 1, projection='polar')
  model['rho'].plot_phi_cut(index, ax=ax, ...)
  model['br'].contour_phi_cut(index, levels=[0], ax=ax, ...)

and produces outputs like this:

.. image:: /auto_examples/visualisation/images/sphx_glr_plot_visualising_mas_003.png
   :width: 600

For more examples of how to use these methods, see the
:ref:`sphx_glr_auto_examples` gallery.

Normalising data before plotting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Sometimes it is helpful to multiply data by an expected radial falloff, e.g.
multiplying the density by :math:`r^{2}`. This can be done using the
`Variable.radial_normalized` method, e.g.:

.. code-block:: python

  rho = mas_output['rho']
  rho_r_squared = rho.radial_normalized(2)
  rho_r_squared.plot_phi_cut(...)


Sampling data
-------------
Variable objects have a `Variable.sample_at_coords` method, to take a sample of
the 3D data cube along a 1D trajectory. This is helpful for flying a 'virtual
spacecraft' through the model, in order to compare model results with in-situ
measurements.

`sample_at_coords` requires arrays of longitude, latitude, and radial distance.
Given these coordinates, it uses linear interpolation to extract the values
of the variable at each of the coordinate points.

For an example of how all this works, see :ref:`sphx_glr_auto_examples_sampling_plot_in_situ_comparison.py`.
