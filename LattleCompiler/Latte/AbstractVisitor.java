package Latte;
import Latte.Absyn.*;
/** BNFC-Generated Abstract Visitor */
public class AbstractVisitor<R,A> implements AllVisitor<R,A> {
/* Program */
    public R visit(Latte.Absyn.ProgramNode p, A arg) { return visitDefault(p, arg); }
    public R visitDefault(Latte.Absyn.Program p, A arg) {
      throw new IllegalArgumentException(this.getClass().getName() + ": " + p);
    }
/* TopDef */
    public R visit(Latte.Absyn.FnDef p, A arg) { return visitDefault(p, arg); }
    public R visitDefault(Latte.Absyn.TopDef p, A arg) {
      throw new IllegalArgumentException(this.getClass().getName() + ": " + p);
    }
/* Arg */
    public R visit(Latte.Absyn.ArgNode p, A arg) { return visitDefault(p, arg); }
    public R visitDefault(Latte.Absyn.Arg p, A arg) {
      throw new IllegalArgumentException(this.getClass().getName() + ": " + p);
    }
/* Block */
    public R visit(Latte.Absyn.BlockNode p, A arg) { return visitDefault(p, arg); }
    public R visitDefault(Latte.Absyn.Block p, A arg) {
      throw new IllegalArgumentException(this.getClass().getName() + ": " + p);
    }
/* Stmt */
    public R visit(Latte.Absyn.Empty p, A arg) { return visitDefault(p, arg); }
    public R visit(Latte.Absyn.BStmt p, A arg) { return visitDefault(p, arg); }
    public R visit(Latte.Absyn.Decl p, A arg) { return visitDefault(p, arg); }
    public R visit(Latte.Absyn.Ass p, A arg) { return visitDefault(p, arg); }
    public R visit(Latte.Absyn.Incr p, A arg) { return visitDefault(p, arg); }
    public R visit(Latte.Absyn.Decr p, A arg) { return visitDefault(p, arg); }
    public R visit(Latte.Absyn.Ret p, A arg) { return visitDefault(p, arg); }
    public R visit(Latte.Absyn.VRet p, A arg) { return visitDefault(p, arg); }
    public R visit(Latte.Absyn.Cond p, A arg) { return visitDefault(p, arg); }
    public R visit(Latte.Absyn.CondElse p, A arg) { return visitDefault(p, arg); }
    public R visit(Latte.Absyn.While p, A arg) { return visitDefault(p, arg); }
    public R visit(Latte.Absyn.SExp p, A arg) { return visitDefault(p, arg); }
    public R visitDefault(Latte.Absyn.Stmt p, A arg) {
      throw new IllegalArgumentException(this.getClass().getName() + ": " + p);
    }
/* Item */
    public R visit(Latte.Absyn.NoInit p, A arg) { return visitDefault(p, arg); }
    public R visit(Latte.Absyn.Init p, A arg) { return visitDefault(p, arg); }
    public R visitDefault(Latte.Absyn.Item p, A arg) {
      throw new IllegalArgumentException(this.getClass().getName() + ": " + p);
    }
/* Type */
    public R visit(Latte.Absyn.Int p, A arg) { return visitDefault(p, arg); }
    public R visit(Latte.Absyn.Str p, A arg) { return visitDefault(p, arg); }
    public R visit(Latte.Absyn.Bool p, A arg) { return visitDefault(p, arg); }
    public R visit(Latte.Absyn.Void p, A arg) { return visitDefault(p, arg); }
    public R visit(Latte.Absyn.Fun p, A arg) { return visitDefault(p, arg); }
    public R visitDefault(Latte.Absyn.Type p, A arg) {
      throw new IllegalArgumentException(this.getClass().getName() + ": " + p);
    }
/* Expr */
    public R visit(Latte.Absyn.EVar p, A arg) { return visitDefault(p, arg); }
    public R visit(Latte.Absyn.ELitInt p, A arg) { return visitDefault(p, arg); }
    public R visit(Latte.Absyn.ELitTrue p, A arg) { return visitDefault(p, arg); }
    public R visit(Latte.Absyn.ELitFalse p, A arg) { return visitDefault(p, arg); }
    public R visit(Latte.Absyn.EApp p, A arg) { return visitDefault(p, arg); }
    public R visit(Latte.Absyn.EString p, A arg) { return visitDefault(p, arg); }

    public R visit(Latte.Absyn.Neg p, A arg) { return visitDefault(p, arg); }
    public R visit(Latte.Absyn.Not p, A arg) { return visitDefault(p, arg); }

    public R visit(Latte.Absyn.EMul p, A arg) { return visitDefault(p, arg); }

    public R visit(Latte.Absyn.EAdd p, A arg) { return visitDefault(p, arg); }

    public R visit(Latte.Absyn.ERel p, A arg) { return visitDefault(p, arg); }

    public R visit(Latte.Absyn.EAnd p, A arg) { return visitDefault(p, arg); }

    public R visit(Latte.Absyn.EOr p, A arg) { return visitDefault(p, arg); }

    public R visitDefault(Latte.Absyn.Expr p, A arg) {
      throw new IllegalArgumentException(this.getClass().getName() + ": " + p);
    }
/* AddOp */
    public R visit(Latte.Absyn.Plus p, A arg) { return visitDefault(p, arg); }
    public R visit(Latte.Absyn.Minus p, A arg) { return visitDefault(p, arg); }
    public R visitDefault(Latte.Absyn.AddOp p, A arg) {
      throw new IllegalArgumentException(this.getClass().getName() + ": " + p);
    }
/* MulOp */
    public R visit(Latte.Absyn.Times p, A arg) { return visitDefault(p, arg); }
    public R visit(Latte.Absyn.Div p, A arg) { return visitDefault(p, arg); }
    public R visit(Latte.Absyn.Mod p, A arg) { return visitDefault(p, arg); }
    public R visitDefault(Latte.Absyn.MulOp p, A arg) {
      throw new IllegalArgumentException(this.getClass().getName() + ": " + p);
    }
/* RelOp */
    public R visit(Latte.Absyn.LTH p, A arg) { return visitDefault(p, arg); }
    public R visit(Latte.Absyn.LE p, A arg) { return visitDefault(p, arg); }
    public R visit(Latte.Absyn.GTH p, A arg) { return visitDefault(p, arg); }
    public R visit(Latte.Absyn.GE p, A arg) { return visitDefault(p, arg); }
    public R visit(Latte.Absyn.EQU p, A arg) { return visitDefault(p, arg); }
    public R visit(Latte.Absyn.NE p, A arg) { return visitDefault(p, arg); }
    public R visitDefault(Latte.Absyn.RelOp p, A arg) {
      throw new IllegalArgumentException(this.getClass().getName() + ": " + p);
    }

}
