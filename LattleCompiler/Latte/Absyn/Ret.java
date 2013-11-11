package Latte.Absyn; // Java Package generated by the BNF Converter.

public class Ret extends Stmt {
  public final Expr expr_;

  public Ret(Expr p1) { expr_ = p1; }

  public <R,A> R accept(Latte.Absyn.Stmt.Visitor<R,A> v, A arg) { return v.visit(this, arg); }

  public boolean equals(Object o) {
    if (this == o) return true;
    if (o instanceof Latte.Absyn.Ret) {
      Latte.Absyn.Ret x = (Latte.Absyn.Ret)o;
      return this.expr_.equals(x.expr_);
    }
    return false;
  }

  public int hashCode() {
    return this.expr_.hashCode();
  }


}
