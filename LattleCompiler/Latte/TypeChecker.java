package Latte;

import Latte.Absyn.TopDef;

public class TypeChecker
{
	private Latte.Absyn.ProgramNode root;
	
	public TypeChecker(Latte.Absyn.Program root)
	{
		this.root = (Latte.Absyn.ProgramNode)root;
	}

	public void CheckTypes()
	{
		for (TopDef topDefNode : root.listtopdef_) 
		{
			
		}
	}
}
