package Latte;
import Latte.Absyn.*;
/** BNFC-Generated Composition Visitor
*/

public class ComposVisitor<A> implements
  Latte.Absyn.Program.Visitor<Latte.Absyn.Program,A>,
  Latte.Absyn.TopDef.Visitor<Latte.Absyn.TopDef,A>,
  Latte.Absyn.Arg.Visitor<Latte.Absyn.Arg,A>,
  Latte.Absyn.Block.Visitor<Latte.Absyn.Block,A>,
  Latte.Absyn.Stmt.Visitor<Latte.Absyn.Stmt,A>,
  Latte.Absyn.Item.Visitor<Latte.Absyn.Item,A>,
  Latte.Absyn.Type.Visitor<Latte.Absyn.Type,A>,
  Latte.Absyn.Expr.Visitor<Latte.Absyn.Expr,A>,
  Latte.Absyn.AddOp.Visitor<Latte.Absyn.AddOp,A>,
  Latte.Absyn.MulOp.Visitor<Latte.Absyn.MulOp,A>,
  Latte.Absyn.RelOp.Visitor<Latte.Absyn.RelOp,A>
{
/* Program */
    public Program visit(Latte.Absyn.ProgramNode p, A arg)
    {
      ListTopDef listtopdef_ = new ListTopDef();
      for (TopDef x : p.listtopdef_) {
        listtopdef_.add(x.accept(this,arg));
      }

      return new Latte.Absyn.ProgramNode(listtopdef_);
    }

/* TopDef */
    public TopDef visit(Latte.Absyn.FnDef p, A arg)
    {
      Type type_ = p.type_.accept(this, arg);
      String ident_ = p.ident_;
      ListArg listarg_ = new ListArg();
      for (Arg x : p.listarg_) {
        listarg_.add(x.accept(this,arg));
      }
      Block block_ = p.block_.accept(this, arg);

      return new Latte.Absyn.FnDef(type_, ident_, listarg_, block_);
    }

/* Arg */
    public Arg visit(Latte.Absyn.ArgNode p, A arg)
    {
      Type type_ = p.type_.accept(this, arg);
      String ident_ = p.ident_;

      return new Latte.Absyn.ArgNode(type_, ident_);
    }

/* Block */
    public Block visit(Latte.Absyn.BlockNode p, A arg)
    {
      ListStmt liststmt_ = new ListStmt();
      for (Stmt x : p.liststmt_) {
        liststmt_.add(x.accept(this,arg));
      }

      return new Latte.Absyn.BlockNode(liststmt_);
    }

/* Stmt */
    public Stmt visit(Latte.Absyn.Empty p, A arg)
    {

      return new Latte.Absyn.Empty();
    }
    public Stmt visit(Latte.Absyn.BStmt p, A arg)
    {
      Block block_ = p.block_.accept(this, arg);

      return new Latte.Absyn.BStmt(block_);
    }
    public Stmt visit(Latte.Absyn.Decl p, A arg)
    {
      Type type_ = p.type_.accept(this, arg);
      ListItem listitem_ = new ListItem();
      for (Item x : p.listitem_) {
        listitem_.add(x.accept(this,arg));
      }

      return new Latte.Absyn.Decl(type_, listitem_);
    }
    public Stmt visit(Latte.Absyn.Ass p, A arg)
    {
      String ident_ = p.ident_;
      Expr expr_ = p.expr_.accept(this, arg);

      return new Latte.Absyn.Ass(ident_, expr_);
    }
    public Stmt visit(Latte.Absyn.Incr p, A arg)
    {
      String ident_ = p.ident_;

      return new Latte.Absyn.Incr(ident_);
    }
    public Stmt visit(Latte.Absyn.Decr p, A arg)
    {
      String ident_ = p.ident_;

      return new Latte.Absyn.Decr(ident_);
    }
    public Stmt visit(Latte.Absyn.Ret p, A arg)
    {
      Expr expr_ = p.expr_.accept(this, arg);

      return new Latte.Absyn.Ret(expr_);
    }
    public Stmt visit(Latte.Absyn.VRet p, A arg)
    {

      return new Latte.Absyn.VRet();
    }
    public Stmt visit(Latte.Absyn.Cond p, A arg)
    {
      Expr expr_ = p.expr_.accept(this, arg);
      Stmt stmt_ = p.stmt_.accept(this, arg);

      return new Latte.Absyn.Cond(expr_, stmt_);
    }
    public Stmt visit(Latte.Absyn.CondElse p, A arg)
    {
      Expr expr_ = p.expr_.accept(this, arg);
      Stmt stmt_1 = p.stmt_1.accept(this, arg);
      Stmt stmt_2 = p.stmt_2.accept(this, arg);

      return new Latte.Absyn.CondElse(expr_, stmt_1, stmt_2);
    }
    public Stmt visit(Latte.Absyn.While p, A arg)
    {
      Expr expr_ = p.expr_.accept(this, arg);
      Stmt stmt_ = p.stmt_.accept(this, arg);

      return new Latte.Absyn.While(expr_, stmt_);
    }
    public Stmt visit(Latte.Absyn.SExp p, A arg)
    {
      Expr expr_ = p.expr_.accept(this, arg);

      return new Latte.Absyn.SExp(expr_);
    }

/* Item */
    public Item visit(Latte.Absyn.NoInit p, A arg)
    {
      String ident_ = p.ident_;

      return new Latte.Absyn.NoInit(ident_);
    }
    public Item visit(Latte.Absyn.Init p, A arg)
    {
      String ident_ = p.ident_;
      Expr expr_ = p.expr_.accept(this, arg);

      return new Latte.Absyn.Init(ident_, expr_);
    }

/* Type */
    public Type visit(Latte.Absyn.Int p, A arg)
    {

      return new Latte.Absyn.Int();
    }
    public Type visit(Latte.Absyn.Str p, A arg)
    {

      return new Latte.Absyn.Str();
    }
    public Type visit(Latte.Absyn.Bool p, A arg)
    {

      return new Latte.Absyn.Bool();
    }
    public Type visit(Latte.Absyn.Void p, A arg)
    {

      return new Latte.Absyn.Void();
    }
    public Type visit(Latte.Absyn.Fun p, A arg)
    {
      Type type_ = p.type_.accept(this, arg);
      ListType listtype_ = new ListType();
      for (Type x : p.listtype_) {
        listtype_.add(x.accept(this,arg));
      }

      return new Latte.Absyn.Fun(type_, listtype_);
    }

/* Expr */
    public Expr visit(Latte.Absyn.EVar p, A arg)
    {
      String ident_ = p.ident_;

      return new Latte.Absyn.EVar(ident_);
    }
    public Expr visit(Latte.Absyn.ELitInt p, A arg)
    {
      Integer integer_ = p.integer_;

      return new Latte.Absyn.ELitInt(integer_);
    }
    public Expr visit(Latte.Absyn.ELitTrue p, A arg)
    {

      return new Latte.Absyn.ELitTrue();
    }
    public Expr visit(Latte.Absyn.ELitFalse p, A arg)
    {

      return new Latte.Absyn.ELitFalse();
    }
    public Expr visit(Latte.Absyn.EApp p, A arg)
    {
      String ident_ = p.ident_;
      ListExpr listexpr_ = new ListExpr();
      for (Expr x : p.listexpr_) {
        listexpr_.add(x.accept(this,arg));
      }

      return new Latte.Absyn.EApp(ident_, listexpr_);
    }
    public Expr visit(Latte.Absyn.EString p, A arg)
    {
      String string_ = p.string_;

      return new Latte.Absyn.EString(string_);
    }
    public Expr visit(Latte.Absyn.Neg p, A arg)
    {
      Expr expr_ = p.expr_.accept(this, arg);

      return new Latte.Absyn.Neg(expr_);
    }
    public Expr visit(Latte.Absyn.Not p, A arg)
    {
      Expr expr_ = p.expr_.accept(this, arg);

      return new Latte.Absyn.Not(expr_);
    }
    public Expr visit(Latte.Absyn.EMul p, A arg)
    {
      Expr expr_1 = p.expr_1.accept(this, arg);
      MulOp mulop_ = p.mulop_.accept(this, arg);
      Expr expr_2 = p.expr_2.accept(this, arg);

      return new Latte.Absyn.EMul(expr_1, mulop_, expr_2);
    }
    public Expr visit(Latte.Absyn.EAdd p, A arg)
    {
      Expr expr_1 = p.expr_1.accept(this, arg);
      AddOp addop_ = p.addop_.accept(this, arg);
      Expr expr_2 = p.expr_2.accept(this, arg);

      return new Latte.Absyn.EAdd(expr_1, addop_, expr_2);
    }
    public Expr visit(Latte.Absyn.ERel p, A arg)
    {
      Expr expr_1 = p.expr_1.accept(this, arg);
      RelOp relop_ = p.relop_.accept(this, arg);
      Expr expr_2 = p.expr_2.accept(this, arg);

      return new Latte.Absyn.ERel(expr_1, relop_, expr_2);
    }
    public Expr visit(Latte.Absyn.EAnd p, A arg)
    {
      Expr expr_1 = p.expr_1.accept(this, arg);
      Expr expr_2 = p.expr_2.accept(this, arg);

      return new Latte.Absyn.EAnd(expr_1, expr_2);
    }
    public Expr visit(Latte.Absyn.EOr p, A arg)
    {
      Expr expr_1 = p.expr_1.accept(this, arg);
      Expr expr_2 = p.expr_2.accept(this, arg);

      return new Latte.Absyn.EOr(expr_1, expr_2);
    }

/* AddOp */
    public AddOp visit(Latte.Absyn.Plus p, A arg)
    {

      return new Latte.Absyn.Plus();
    }
    public AddOp visit(Latte.Absyn.Minus p, A arg)
    {

      return new Latte.Absyn.Minus();
    }

/* MulOp */
    public MulOp visit(Latte.Absyn.Times p, A arg)
    {

      return new Latte.Absyn.Times();
    }
    public MulOp visit(Latte.Absyn.Div p, A arg)
    {

      return new Latte.Absyn.Div();
    }
    public MulOp visit(Latte.Absyn.Mod p, A arg)
    {

      return new Latte.Absyn.Mod();
    }

/* RelOp */
    public RelOp visit(Latte.Absyn.LTH p, A arg)
    {

      return new Latte.Absyn.LTH();
    }
    public RelOp visit(Latte.Absyn.LE p, A arg)
    {

      return new Latte.Absyn.LE();
    }
    public RelOp visit(Latte.Absyn.GTH p, A arg)
    {

      return new Latte.Absyn.GTH();
    }
    public RelOp visit(Latte.Absyn.GE p, A arg)
    {

      return new Latte.Absyn.GE();
    }
    public RelOp visit(Latte.Absyn.EQU p, A arg)
    {

      return new Latte.Absyn.EQU();
    }
    public RelOp visit(Latte.Absyn.NE p, A arg)
    {

      return new Latte.Absyn.NE();
    }

}