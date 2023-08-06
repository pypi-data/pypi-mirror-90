*******************************
A look inside the extrapolation
*******************************

Frozen standard deviation extrapolation
=======================================

The parameter *target threshold*

.. plot::

    import examplecurves
    from arithmeticmeancurve import (
        ArithmeticMeanCurve, FrozenStdExtrapolation, VisualIterationTester
    )

    sample_curves = examplecurves.Static.create(family_name="horizontallinear1")
    extrapolates = FrozenStdExtrapolation(target_threshold=0.001)
    VisualIterationTester.plot_extrapolation_test(
        curves=sample_curves,
        extrapolates=extrapolates
    )


.. plot::

    import examplecurves
    from arithmeticmeancurve import (
        ArithmeticMeanCurve, FrozenStdExtrapolation, VisualIterationTester
    )

    sample_curves = examplecurves.Static.create(family_name="horizontallinear1")
    extrapolates = FrozenStdExtrapolation(target_threshold=0.0001)
    VisualIterationTester.plot_extrapolation_test(
        curves=sample_curves,
        extrapolates=extrapolates
    )