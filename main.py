import numpy as np
from src import equations, integration, variants, utils

def main():
    # Настройки
    variant_num = 6
    XTOL = 1e-8
    RTOL = 1e-8
    MAX_ITER = 100
    
    EPSABS = 1e-8
    EPSREL = 1e-8
 
    f, a_root, b_root, g, a_int, b_int, exact_integral = variants.get_variant(variant_num)
    
    print("\nЧасть А:")
    # 1. Проверка знаков
    print(f"f(a) = {f(a_root):.4f}, f(b) = {f(b_root):.4f}")
    
    # 2. Бисекция
    root_bis, res_bis, iter_bis, converged_bis = equations.bisection(
        f, a_root, b_root, xtol=XTOL, rtol=RTOL, max_iter=MAX_ITER
    )
    print(f"Бисекция: корень = {root_bis:.10f}, невязка = {res_bis:.2e}, итераций = {iter_bis}, сошлась = {converged_bis}")
    
    # 3. Brentq
    root_brent, res_brent, iter_brent = equations.scipy_brentq(
        f, a_root, b_root, xtol=XTOL, rtol=RTOL, max_iter=MAX_ITER
    )
    print(f"Brentq:   корень = {root_brent:.10f}, невязка = {res_brent:.2e}, итераций = {iter_brent}")
    
    # 4. Сравнение
    root_comparison = equations.compare_roots(
        root_bis, (root_bis, res_bis, iter_bis), 
        root_brent, (root_brent, res_brent, iter_brent)
    )
    print(f"Разность приближений: {root_comparison['difference_roots']:.2e}")
    
 
    print("\nЧасть В:")
    
    quad_val, quad_err = integration.scipy_quad(g, a_int, b_int, epsabs=EPSABS, epsrel=EPSREL)
    print(f"SciPy quad: {quad_val:.10f} (оценка ошибки: {quad_err:.2e})")
    if exact_integral:
        print(f"Точное значение: {exact_integral:.10f}")
    
    n_values = [50, 100, 200, 400]
    integration_results = {}
    
    print(f"\n{'n':<5} | {'T_n':<15} | {'|Tn - quad|':<15} | {'Факт. ошибка':<15}")
    print("-" * 60)
    
    for n in n_values:
        Tn = integration.composite_trapezoid(g, a_int, b_int, n)
        comp = integration.compare_integrals(Tn, quad_val, quad_err, exact_integral)
        
        integration_results[f"n_{n}"] = {
            "T_n": Tn,
            **comp
        }
        
        actual_err = comp.get("actual_error_Tn", float('nan'))
        print(f"{n:<5} | {Tn:.10f} | {comp['method_difference']:.2e} | {actual_err:.2e}")


    final_data = {
        "variant": variant_num,
        "parameters": {
            "xtol": XTOL, "rtol": RTOL, "max_iter": MAX_ITER,
            "epsabs": EPSABS, "epsrel": EPSREL
        },
        "part_a": root_comparison,
        "part_b": integration_results
    }
    
    utils.save_results_to_json(final_data, "results/results.json")
    utils.save_results_to_csv(integration_results, "results/integration_table.csv")

if __name__ == "__main__":
    main()