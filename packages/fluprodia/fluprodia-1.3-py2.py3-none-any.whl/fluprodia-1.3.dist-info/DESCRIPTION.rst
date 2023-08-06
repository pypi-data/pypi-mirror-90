=======================
Fluid Property Diagrams
=======================

Create custom and beautiful Fluid Property Diagrams with fluprodia. The package
implements fluid property data from CoolProp [1]_. Plotting is handled by
matplotlib [2]_, all calculations are performed with numpy [3]_.
The list of fluids available can be found at
`CoolProp <http://www.coolprop.org/fluid_properties/PurePseudoPure.html#list-of-fluids>`_.

fluprodia is licensed under the MIT software license.



Installation and Usage
======================

.. code-block:: bash

    pip install fluprodia

.. code-block:: python

    from fluprodia import FluidPropertyDiagram

    diagram = FluidPropertyDiagram(fluid='H2O')
    diagram.set_unit_system(T='°C', h='kJ/kg', p='bar')
    diagram.calc_isolines()
    diagram.set_limits(x_min=0, x_max=8000, y_min=0, y_max=700)
    diagram.draw_isolines(diagram_type='Ts')
    diagram.save('Ts_diagram_H2O.svg')
    diagram.save('Ts_diagram_H2O.png', dpi=300)

.. figure:: docs/reference/_images/Ts_diagram_H2O.png
    :align: center

.. code-block:: python

    diagram = FluidPropertyDiagram(fluid='NH3')
    diagram.set_unit_system(T='°C', h='kJ/kg', p='bar')
    diagram.calc_isolines()
    diagram.set_limits(x_min=0, x_max=2000, y_min=1e-1, y_max=2e2)
    diagram.draw_isolines(diagram_type='logph')
    diagram.save('logph_diagram_NH3.png', dpi=300)
    diagram.save('logph_diagram_NH3.svg')

.. figure:: docs/reference/_images/logph_diagram_NH3.png
    :align: center

Documentation
=============

For further examples and usage please refer to the online documentation at
https://fluprodia.readthedocs.io/en/latest/.

Citation
========

Every version of fluprodia is archived at zenodo. You can cite the latest or
a specific version. For citation info and more details please go to the
`zenodo entry <https://zenodo.org/record/3795771>`_ of fluprodia.

References
==========

This software depends on the packages CoolProp, matplolib and numpy.

.. [1] Bell, I., Wronski, J., Quoilin, S. and Lemort, V., 2014. Pure and Pseudo-pure Fluid Thermophysical Property Evaluation and the Open-Source Thermophysical Property Library CoolProp. *Industrial & Engineering Chemistry Research*, 53(6), pp. 2498-2508.
.. [2] Hunter, J., 2007. Matplotlib: A 2D Graphics Environment. *Computing in Science & Engineering*, 9(3), pp. 90-95.
.. [3] van der Walt, S., Colbert, S. and Varoquaux, G., 2011. The NumPy Array: A Structure for Efficient Numerical Computation. *Computing in Science & Engineering*, 13(2), pp. 22-30.


Changelog
=========

v1.3 (January, 7, 2021)
-----------------------

* Reduce the number of datappoints for isolines to 200 for faster performance.

v1.2 (December, 8, 2020)
------------------------

* Fix minimum volume value for iterators.

v1.1 (November, 10, 2020)
-------------------------

* Change the iterator for isobaric, isenthalpic and isentropic to specific volume.
* Adjust individual isoline plotting iterators and isolines accordingly.

v1.0 (November, 8, 2020)
------------------------

* Add method to calculate datapoints of individual isolines and isolike lines.

v0.1.2 (October, 2, 2020)
-------------------------

* Minor bug fixes for isochoric drawing.
* Change in default values for isobarics.

v0.1.1 (May, 13, 2020)
----------------------

* Catch exceptions in calculation of minimum specific volume for default
  isoline generation.
* Allow Python 3.8 usage.

v0.1.0 (May, 6, 2020)
---------------------

* First release on PyPI.


