"""
Ejecuta todas las demos del proyecto (salida ASCII para consola Windows).
"""

from __future__ import annotations


def main() -> int:
    import formulas_clase_ma
    import ma_algebra_metricas
    import ma_edo
    import ma_integracion_extras
    import ma_interpolacion
    import ma_minimos_cuadrados
    import ma_optimizacion
    import ma_raices_avanzado

    modules = [
        ("formulas_clase_ma (nucleo)", formulas_clase_ma.demo),
        ("ma_interpolacion", ma_interpolacion.demo),
        ("ma_raices_avanzado", ma_raices_avanzado.demo),
        ("ma_edo", ma_edo.demo),
        ("ma_minimos_cuadrados", ma_minimos_cuadrados.demo),
        ("ma_algebra_metricas", ma_algebra_metricas.demo),
        ("ma_optimizacion", ma_optimizacion.demo),
        ("ma_integracion_extras", ma_integracion_extras.demo),
    ]

    for title, fn in modules:
        print("\n" + "=" * 60)
        print(title)
        print("=" * 60)
        fn()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
