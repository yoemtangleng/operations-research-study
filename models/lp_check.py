"""
lp_check.py — 运筹学 LP 求解 / 验证工具（只用于核对手算结果，不替代手算过程）

用法（在其他脚本里）：
    from lp_check import solve_lp
    solve_lp(
        sense="max",                       # "max" 或 "min"
        c=[2, 3],                          # 目标函数系数
        constraints=[                      # (系数, 方向, 右端项, 说明)
            ([1, 2], "<=", 8,  "设备台时"),
            ([4, 0], "<=", 16, "银锭"),
            ([0, 4], "<=", 12, "金锭"),
        ],
        names=["x1", "x2"],
        bounds=None,                       # 默认全部 >= 0；自由变量写 (None, None)
        title="第一章 例1",
    )

依赖：scipy、numpy（pip install scipy numpy）
"""
from fractions import Fraction

import numpy as np
from scipy.optimize import linprog


def _frac(x, tol=1e-9):
    """把浮点数近似成分数，方便和手算的单纯形表对照。"""
    f = Fraction(x).limit_denominator(10000)
    return str(f) if abs(float(f) - x) < tol * max(1, abs(x)) else f"{x:.6g}"


def solve_lp(sense, c, constraints, names=None, bounds=None, title="", expect=None):
    n = len(c)
    names = names or [f"x{j+1}" for j in range(n)]
    sign = -1 if sense == "max" else 1           # linprog 只做 min

    A_ub, b_ub, A_eq, b_eq = [], [], [], []
    for coef, op, rhs, _ in constraints:
        if op == "<=":
            A_ub.append(coef); b_ub.append(rhs)
        elif op == ">=":
            A_ub.append([-a for a in coef]); b_ub.append(-rhs)
        elif op == "=":
            A_eq.append(coef); b_eq.append(rhs)
        else:
            raise ValueError(f"未知约束方向 {op}")

    res = linprog(
        c=[sign * cj for cj in c],
        A_ub=A_ub or None, b_ub=b_ub or None,
        A_eq=A_eq or None, b_eq=b_eq or None,
        bounds=bounds if bounds is not None else [(0, None)] * n,
        method="highs",
    )

    print("=" * 60)
    print(f"{title}  ({sense})")
    print("-" * 60)
    if res.status == 2:
        print("结果：无可行解（检查是否有相互矛盾的约束）")
        return res
    if res.status == 3:
        print("结果：无界解（检查是否漏了约束）")
        return res
    if res.status != 0:
        print("求解失败：", res.message)
        return res

    x = res.x
    z = sign * res.fun
    print("最优解：", ", ".join(f"{nm} = {_frac(v)}" for nm, v in zip(names, x)))
    print("最优值： z* =", _frac(z))

    # 代回原始约束逐条检查
    print("\n约束检查（代回原始约束）：")
    ok = True
    for coef, op, rhs, note in constraints:
        lhs = float(np.dot(coef, x))
        sat = {"<=": lhs <= rhs + 1e-7, ">=": lhs >= rhs - 1e-7, "=": abs(lhs - rhs) < 1e-7}[op]
        tight = "（紧约束）" if abs(lhs - rhs) < 1e-7 else ""
        ok &= sat
        print(f"  {'✓' if sat else '✗'} {note or ''}: 左端 = {_frac(lhs)} {op} {_frac(rhs)} {tight}")
    print("全部满足 ✓" if ok else "存在不满足的约束 ✗")

    if expect is not None:
        match = abs(z - expect) < 1e-6
        print(f"\n与手算/课件结果 z = {_frac(expect)} 对照：{'一致 ✓' if match else '不一致 ✗ —— 需要查原因'}")

    print("\n提示：求解器只告诉你'答案'，不告诉你多重最优解/退化等情况；"
          "这些仍要看最终单纯形表的检验数判断。")
    return res
