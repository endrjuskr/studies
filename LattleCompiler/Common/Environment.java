package Common;

import java.util.Arrays;
import java.util.LinkedHashMap;
import Latte.Absyn.*;
import Latte.Absyn.Void;
import Latte.Absyn.Int;

public class Environment {
	private LinkedHashMap<String, Type> envmap;
	
	public Environment() 
	{
		this.envmap = new LinkedHashMap<String, Type>();
		this.AddPredefinedMethods();
	}
	
	public Environment(LinkedHashMap<String, Type> envmap)
	{
		this.envmap = (LinkedHashMap<String, Type>)envmap.clone();
	}
	
	public Environment(Environment environment) {
	    this(environment.GetEnvMap());
	  }
	
	public LinkedHashMap<String, Type> GetEnvMap()
	{
		return this.envmap;
	}
	
	protected void AddPredefinedMethods()
	{
		ListType printIntListType = new ListType();
		printIntListType.add(new Int());
		envmap.put("printInt", new Fun(new Void(), printIntListType));
		ListType printStringListType = new ListType();
		printStringListType.add(new Str());
		envmap.put("printString", new Fun(new Void(), printStringListType));;
		envmap.put("error", new Fun(new Void(), new ListType()));
		envmap.put("readInt", new Fun(new Int(), new ListType()));
		envmap.put("readString", new Fun(new Str(), new ListType()));
	}
}

