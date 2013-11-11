package Latte.Absyn; // Java Package generated by the BNF Converter.

public class BlockNode extends Block {
  public final ListStmt liststmt_;

  public BlockNode(ListStmt p1) { liststmt_ = p1; }

  public <R,A> R accept(Latte.Absyn.Block.Visitor<R,A> v, A arg) { return v.visit(this, arg); }

  public boolean equals(Object o) {
    if (this == o) return true;
    if (o instanceof Latte.Absyn.BlockNode) {
      Latte.Absyn.BlockNode x = (Latte.Absyn.BlockNode)o;
      return this.liststmt_.equals(x.liststmt_);
    }
    return false;
  }

  public int hashCode() {
    return this.liststmt_.hashCode();
  }


}
